# coding: utf8
from __future__ import print_function, absolute_import

import mimetypes

import click
import re
import os
from six import iteritems
from fds import GalaxyFDSClient, FDSClientConfiguration, GalaxyFDSClientException
from fds.auth import Common
from fds.model.fds_object_metadata import FDSObjectMetadata
from cloudpretrain.config import default_config
from cloudpretrain.utils.colors import success, info
from cloudpretrain.utils import to_str


if default_config.validate():
    fds_client = GalaxyFDSClient(
        access_key=default_config.access_key,
        access_secret=default_config.secret_key,
        config=FDSClientConfiguration(
            endpoint=default_config.fds_endpoint,
            enable_cdn_for_upload=False,
            enable_cdn_for_download=False,
        ),
    )
else:
    fds_client = None


def to_fds_uri(bucket_name, object_name):
    return "fds://{}/{}".format(bucket_name, object_name)


def to_mount_uri(object_name):
    return "/{}/{}".format(default_config.fds_bucket, object_name)


def to_default_mount_uri(object_name):
    return "/fds/{}".format(object_name)
    

class FileSystemNode(object):

    def __init__(self, name):
        self.name = name
        self.children = {}

    def tree_lines(self, fill_string=""):
        for i, (name, child) in enumerate(iteritems(self.children)):
            if i == len(self.children)-1:
                yield fill_string + "└── " + name
                next_fill_string = fill_string + "    "
            else:
                yield fill_string + "├── " + name
                next_fill_string = fill_string + "│   "
            for j, line in enumerate(child.tree_lines(next_fill_string)):
                yield line


class FileSystemTree(object):

    def __init__(self):
        self.root = FileSystemNode("")

    @staticmethod
    def split(path):
        if "/" in path:
            dirname, rest = path.split("/", 1)
        else:
            dirname, rest = path, None
        return dirname, rest

    def add_path(self, path):
        parent = self.root
        while path:
            dirname, rest = self.split(path)
            if dirname:
                if dirname not in parent.children:
                    node = FileSystemNode(dirname)
                    parent.children[dirname] = node
                parent = parent.children[dirname]
            path = rest

    def tree_lines(self, prefix="workspace"):
        node = self.root
        click.echo(prefix)
        while prefix:
            dirname, rest = self.split(prefix)
            if dirname not in node.children:
                raise ValueError("Prefix {} is invalid.".format(prefix))
            node = node.children[dirname]
            prefix = rest
        return node.tree_lines()


def listing_generator(bucket_name, prefix, delimiter="/"):
    try:
        listing = fds_client.list_objects(bucket_name, prefix, delimiter=delimiter)
        yield listing
        while True:
            if listing.is_truncated:
                listing = fds_client.list_next_batch_of_objects(listing)
                yield listing
            else:
                break
    except GalaxyFDSClientException as e:
        pass


def remove_dir(bucket_name, prefix, prompt=False, preview=False):
    objects = fds_client.list_all_objects(bucket_name, prefix, delimiter="")
    tree = FileSystemTree()
    is_empty = True
    for obj in objects:
        is_empty = False
        if preview:
            tree.add_path(obj.object_name)
        else:
            prompt_string = "Deleting " + obj.object_name
            confirmed = True
            if prompt:
                confirmed = click.confirm(prompt_string)
            if confirmed:
                fds_client.delete_object(bucket_name, obj.object_name)
    if not is_empty and preview:
        for line in tree.tree_lines(prefix):
            click.echo(line)
    return not is_empty


def upload_file_to_fds(bucket_name, file, dest, overwrite=False):
    if fds_client.does_object_exists(bucket_name, dest):
        if overwrite:
            fds_client.delete_object(bucket_name, dest)
        else:
            return
    mimetype = mimetypes.guess_type(file)[0]
    metadata = FDSObjectMetadata()
    if mimetype is not None:
        metadata.add_header(Common.CONTENT_TYPE, mimetype)
    with open(file, "rb") as data:
        return fds_client.put_object(bucket_name, dest, data, metadata=metadata)


def write_contents_to_fds(bucket_name, content, dest, overwrite=False):
    if fds_client.does_object_exists(bucket_name, dest):
        if overwrite:
            fds_client.delete_object(bucket_name, dest)
        else:
            return

    return fds_client.put_object(bucket_name, dest, content)


def copy_objects(src_bucket_name, tgt_bucket_name, src_file, tgt_file):
    if fds_client.does_object_exists(tgt_bucket_name, tgt_file):
        return
        
    fds_client.copy_object(src_bucket_name, src_file, tgt_bucket_name, tgt_file)


def copy_folder(src_bucket_name, dst_bucket_name, src_folder, tgt_folder):
    if not src_folder.endswith("/"):
        src_folder += "/"

    # if fds_client.does_object_exists(dst_bucket_name, tgt_folder):
    #     return
    
    for listing in listing_generator(src_bucket_name, src_folder, ""):
        for obj in listing.objects:
            file_name = os.path.split(obj.object_name)[1]

            tgt_file_name = os.path.join(tgt_folder, file_name)
            
            if not fds_client.does_object_exists(dst_bucket_name, tgt_file_name):
                fds_client.copy_object(src_bucket_name, obj.object_name, dst_bucket_name, tgt_file_name)


def check_object_exists(bucket_name, directory):
    try:
        return fds_client.does_object_exists(bucket_name, directory)
    except GalaxyFDSClientException as e:
        print(e.message)
        return False


def list_files(bucket_name, directory):
    file_names = []

    for listing in listing_generator(bucket_name, directory):
        for common_prefix in listing.common_prefixes:
            try:
                _, name = os.path.split(os.path.split(common_prefix)[0])
                file_names.append(name)

            except GalaxyFDSClientException as ex:
                continue
    
    return file_names


def copy_to_serve_dir(bucket_name, export_dir, serve_dir):
    if not export_dir.endswith("/"):
        export_dir += "/"
    if not serve_dir.endswith("/"):
        serve_dir += "/"
    export_version_dir = None
    best_export_version = None
    for listing in listing_generator(bucket_name, export_dir):
        for common_prefix in listing.common_prefixes:
            # common_prefix: workspace/task_name/model/export/best_exporter/1573473604/
            _, basename = os.path.split(os.path.split(common_prefix)[0])
            if basename.isdigit():
                export_version = int(basename)
                if not best_export_version:
                    best_export_version = export_version
                elif export_version > best_export_version:
                    best_export_version = export_version
    if best_export_version:
        export_version_dir = "{}{}/".format(export_dir, best_export_version)

    if export_version_dir:
        dest_dir = serve_dir + "1/"
        for listing in listing_generator(bucket_name, export_version_dir, ""):
            for obj in listing.objects:
                dest_object_name = re.sub(export_version_dir + r"(.*)", dest_dir + r"\g<1>", obj.object_name)
                print("Copy {} to {}...".format(obj.object_name, dest_object_name))
                fds_client.copy_object(bucket_name, obj.object_name, bucket_name, dest_object_name)
    return export_version_dir


def download_if_exists(bucket_name, object_name, output_dir):
    _, filename = os.path.split(object_name)
    output_file = os.path.join(output_dir, filename)
    if filename and os.path.exists(output_dir):
        if fds_client.does_object_exists(bucket_name, object_name):
            print("Downloading from fds://{}/{} to {}".format(bucket_name, object_name, output_file))
            fds_client.download_object(bucket_name, object_name, output_file)
            return output_file


def _get_max_steps(dirs):
    """get max steps by parsing step from basename of dirs."""
    max_steps = None
    max_steps_basename = None
    for d in dirs:
        # subdir example: workspace/task_name/model/ckpt_export/best_exporter/5000/
        # subdir example: workspace/task_name/model/step_1000/
        _, basename = os.path.split(os.path.split(d)[0])
        digits = re.search("([0-9]+)", basename)
        if digits:
            steps = int(digits.group(1))
            if max_steps is None or steps > max_steps:
                max_steps = steps
                max_steps_basename = basename
    return max_steps, max_steps_basename


def get_best_ckpt_path(bucket_name, best_ckpt_dir, tfstyle=True):
    """
    get best checkpoint path from directory best_ckpt_dir.
    in tensorflow case, the best_ckpt_dir may contains subdir named by steps like:
        best_ckpt_dir/1000, best_ckpt_dir/2000, ...
    in paddle-paddle case, the best_ckpt_dir may contains subdir named by steps like:
        best_ckpt_dir/step_1000, best_ckpt_dir/step_2000, ...
    then, it will find the subdir with the largest steps.
    if tfstyle is True, returned value will be like: best_ckpt_dir/3000/model.ckpt-3000
    otherwise, returned value will be like: best_ckpt_dir/step_3000/
    (without model.ckpt-{steps} suffix)
    """
    if not best_ckpt_dir.endswith("/"):
        best_ckpt_dir += "/"
    dirs = []
    for listing in listing_generator(bucket_name, best_ckpt_dir):
        for common_prefix in listing.common_prefixes:
            dirs.append(common_prefix)
    max_steps, max_steps_basename = _get_max_steps(dirs)
    if max_steps is not None:
        if tfstyle:
            return os.path.join(best_ckpt_dir, max_steps_basename, "model.ckpt-{}".format(max_steps))
        else:
            return os.path.join(best_ckpt_dir, max_steps_basename)


def get_ckpt_filename(bucket_name, ckpt_dir):
    if not ckpt_dir.endswith("/"):
        ckpt_dir += "/"

    files = []
    for listing in listing_generator(bucket_name, ckpt_dir):
        for obj in listing.objects:

            _,name = os.path.split(obj.object_name)
            files.append(name)
    
    for fl in files:
        if ".meta" in fl:
            return fl.replace(".meta", "")
    
    return None


class PretrainedModel(object):

    _public_bucket = "cloud-pretrain"
    _file_list = [
        "vocab.txt",
        "bert_model.ckpt.meta",
        "bert_model.ckpt.index",
        "bert_model.ckpt.data-00000-of-00001",
        "bert_config.json"
    ]

    def __init__(self, model_name, private_bucket):
        self.model_name = model_name
        self.private_bucket = private_bucket

    def exists(self, public=True):
        bucket = self._public_bucket if public else self.private_bucket
        for f in self._file_list:
            object_name = "pretrained_models/{}/{}".format(self.model_name, f)
            if not fds_client.does_object_exists(bucket, object_name):
                return False, object_name
        return True, None

    def copy_to_private(self):
        for f in self._file_list:
            object_name = "pretrained_models/{}/{}".format(self.model_name, f)
            fds_client.copy_object(self._public_bucket, object_name, self.private_bucket, object_name)


def check_and_copy_pretrained_models(base_model):
    """ Firstly check whether the base_model exists in private bucket.
    If not, copy the base_model data in public bucket into private bucket.
    """
    base_model_uri = "pretrained_models/{}/".format(base_model)
    # first check private pretrained model
    private = False
    for listing in listing_generator(default_config.fds_bucket, base_model_uri):
        for common_prefix in listing.common_prefixes:
            if common_prefix == base_model_uri:
                click.echo(success("Private pretrained model {} exists in {}".format(
                    base_model, to_fds_uri(default_config.fds_bucket, base_model_uri))))
                private = True
                break
    # copy pretrained model to bucket
    if not private:
        # copy_objects("cloud-pretrain", default_config.fds_bucket, base_model_uri)
        copy_folder("cloud-pretrain", default_config.fds_bucket, base_model_uri, base_model_uri)


def load_object(bucket_name, object_name):
    """
    Load object into built-in string from FDS.
    If PY3, it returns unicode. Otherwise returns bytes.
    """
    config_object = fds_client.get_object(bucket_name, object_name)
    content = b""
    for bts in config_object.stream:
        content += bts
    content = to_str(content)
    return content


def download_object_with_progress_bar(bucket_name, object_name, data_file, offset=0, length=-1):
    """
    Copied from download_object method of FDS sdk, but added progress bar using tqdm library.
    """
    import sys, six
    from tqdm import tqdm
    CHUNK_SIZE = 4096
    fds_object = fds_client.get_object(bucket_name=bucket_name,
                                       object_name=object_name,
                                       position=offset,
                                       stream=True,
                                       size=CHUNK_SIZE)

    length_left = length
    if length_left == -1:
        length_left = six.PY3 and sys.maxsize or sys.maxint
        object_size = fds_object.summary.size
        num_chunks = object_size / CHUNK_SIZE
    else:
        num_chunks = length_left / CHUNK_SIZE
    try:
        if data_file:
            with open(data_file, "wb") as f:
                for chunk in tqdm(fds_object.stream, total=num_chunks):
                    l = min(length_left, len(chunk))
                    f.write(chunk[0:l])
                    length_left -= l
                    if length_left <= 0:
                        break
        else:
            for chunk in tqdm(fds_object.stream, total=num_chunks):
                l = min(length_left, len(chunk))
                if six.PY3:
                    sys.stdout.buffer.write(chunk[0:l])
                else:
                    sys.stdout.write(chunk[0:l])
                length_left -= l
                if length_left <= 0:
                    break
            sys.stdout.flush()
    finally:
        fds_object.stream.close()


if __name__ == "__main__":
    print(copy_to_serve_dir("cloud-pretrain", "workspace/bert-demo/export/", "workspace/bert-demo/serve/"))

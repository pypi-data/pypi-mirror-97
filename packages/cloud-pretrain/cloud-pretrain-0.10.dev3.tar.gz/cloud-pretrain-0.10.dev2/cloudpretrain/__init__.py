import re


def validate_package_version(package_version):
    """ Should be format like 0.5 or 0.1.dev0 or 0.5.post1 """
    match = re.match(r"^[0-9]+\.[0-9]+(\.(dev|post)[0-9]+)?$", package_version)
    if match is None:
        raise ValueError("Invalid package version.")
    return True


__version__ = '0.10.dev2'
validate_package_version(__version__)
__bert_image_version__ = "0.10.dev2"
__ernie_image_version__ = "0.2"
__bert_perftest_image_version = "1.4.7"

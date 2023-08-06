from setuptools import setup, find_packages
from cloudpretrain import __version__

setup(
    name='cloud-pretrain',
    python_requires='>=3.6.0',
    version=__version__,
    description="internal tool for Xiaomi AI-LAB with NLP pretrain",
    author="Xiaomi AI-LAB NLP-APP",
    author_email='zhaoqun3@xiaomi.com',
    packages=find_packages(exclude=("bert", "cloudpretrain-server")),
    license="MIT",
    url='https://github.com/XiaoMi',
    install_requires=[
        'Click==7.0',
        "galaxy-fds-sdk==1.3.9",
        "six>=1.12.0",
        "ansicolors==1.1.8",
        "cloud-ml-sdk>=0.5.1",
        "tabulate==0.8.5",
        "tqdm"
    ],
    entry_points='''
        [console_scripts]
        cloud-pretrain=cloudpretrain.cli:cli
        cptcli=cloudpretrain.cli:cli
    ''',
)

from os.path import dirname, join
# from pip.req import parse_requirements

from setuptools import (
    find_packages,
    setup,
)


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


with open(join(dirname(__file__), './VERSION.txt'), 'rb') as f:
    version = f.read().decode('ascii').strip()

setup(
    name='myselfutilsyjl',  # 模块名称
    version=version,
    description='自己常用的工具包，注释稀少，仅供自己使用  --姚金良',  # 描述
    packages=find_packages(exclude=[]),
    author='yjl',
    author_email='1904782387@qq.com',
    license='不知道是啥',
    package_data={'': ['*.*']},
    url='https://github.com/yaojinliang/myselfutilsyjl/tree/main/dist',
    install_requires=parse_requirements("requirements.txt"),  # 所需的运行环境
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
    ],
)

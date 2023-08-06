import os
from setuptools import setup, find_packages  # 这个包没有的可以pip一下

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.rst")) as f:
    DESCRIPTION = f.read()

setup(
    name="DobotEDU",  # 这里是pip项目发布的名称
    version="1.6.13",  # 版本号，数值大的会优先被pip
    keywords=["DobotEDU", "Dobotlink"],
    description="Dobotlink communication module",
    long_description=DESCRIPTION,
    long_description_content_type="text/markdown",
    license="Apache Licence",
    author="songlijun",
    author_email="songlijun@dobot.cc",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "opencv-python", "sounddevice", "soundfile", "DobotRPC", "requests",
        "playsound", "scipy", "openpyxl"
    ])

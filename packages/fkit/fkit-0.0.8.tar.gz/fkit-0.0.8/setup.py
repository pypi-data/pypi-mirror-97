import setuptools
from src import config

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fkit",
    version=config.version,
    author='fkit group',
    author_email='flowhub@yeah.net',
    description='ft command line tool',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitee.com/tentech/cli.git',
    packages=setuptools.find_packages(),
    install_requires=[
        'docker == 4.2.2',
        'fire == 0.3.1',
        'requests == 2.24.0',
        'oss2 == 2.12.1'
    ],
    include_package_data=True,  # 自动打包文件夹内所有数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    platforms='any',
    entry_points={
        'console_scripts': [
            'fkit=src.cli:main'
        ]
    }
)

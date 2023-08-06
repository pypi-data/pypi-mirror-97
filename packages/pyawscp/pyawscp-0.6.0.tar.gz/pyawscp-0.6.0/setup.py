import pathlib
from setuptools import setup,find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# 
setup(
    name="pyawscp",
    version="0.6.0",
    description="A simple 'Python Shell' environment that you can use to 'talk' with your AWS account...",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://ualter.github.io/pyawscp/",
    author="Ualter Otoni Pereira",
    author_email="ualter.junior@gmail.com",
    keywords = ['aws', 'cloud', 'drawio', 'boto3', 'ec2', 'vpc'],
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["pyawscp","pyawscp.pytransfers3","pyawscp.pymxgraph","pyawscp.templates"],
    include_package_data=True,
    install_requires=[            
        'botocore','boto3','tinydb','Pygments','arnparse','clipboard','pyreadline','websockets','pyreadline','svglib','XlsxWriter'
    ],
    entry_points={
        "console_scripts": [
            "pyawscp=pyawscp.pyawscp:main",
        ]
    },
)
from curtis import __version__ as version
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='curtis-engine',
    version=version,
    author='Gabriel Moreno',
    author_email='gantoreno@gmail.com',
    description="The cardiovascular unified real-time intelligent system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    install_requires=['scikit-learn==0.23.2'],
    python_requires='>=3.5',
    packages=find_packages()
)

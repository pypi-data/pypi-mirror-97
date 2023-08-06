import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="gpscraper",
    version="1.1.0",
    description="A nice Google Play scraper.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/alverelt/gpscraper",
    author="Alver Lopez",
    author_email="alverelt@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'beautifulsoup4',
        'requests'
    ],
    entry_points={},
)
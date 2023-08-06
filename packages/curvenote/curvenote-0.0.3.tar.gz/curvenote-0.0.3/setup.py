import setuptools


def readme():
    with open("README.rst") as file:
        return file.read()


setuptools.setup(
    name="curvenote",
    description="Helper library for curvenote versioning and tracking with Jupyter notebooks",
    long_description=readme(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Topic :: Text Processing :: Linguistic",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Financial and Insurance Industry",
    ],
    url="http://curvenote.com",
    version="0.0.3",
    author="iooxa inc.",
    author_email="hi@curvenote.com",
    packages=setuptools.find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=[
        "pydantic",
        "requests",
        "typer",
        "jinja2",
    ],
    python_requires=">=3.7",
)

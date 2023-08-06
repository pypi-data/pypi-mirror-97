from setuptools import setup, find_packages
from os import path

__version__ = "2.2.0"
desc_file = "README.md"

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, desc_file), encoding="utf-8") as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, "requirements.txt"), encoding="utf-8") as f:
    all_reqs = f.read().split("\n")

install_requires = [x.strip() for x in all_reqs if "git+" not in x]
dependency_links = [
    x.strip().replace("git+", "") for x in all_reqs if x.startswith("git+")
]

setup(
    name="flask-authz",
    version=__version__,
    description="An authorization middleware for Flask that supports ACL, RBAC, ABAC, based on Casbin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=["Yang Luo", "Sciencelogic"],
    author_email="hsluoyz@gmail.com",
    url="https://github.com/pycasbin/flask-authz",
    download_url="https://github.com/pycasbin/flask-authz/tarball/" + __version__,
    license="Apache 2.0",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "flask",
        "pycasbin",
        "casbin",
        "auth",
        "authz",
        "acl",
        "rbac",
        "abac",
        "access control",
        "authorization",
        "permission"
    ],
    packages=find_packages(exclude=["docs", "tests*"]),
    data_files=[desc_file],
    include_package_data=True,
    install_requires=install_requires,
    dependency_links=dependency_links
)

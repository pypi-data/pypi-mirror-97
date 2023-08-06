import json
import os
from setuptools import setup


with open("package.json") as f:
    package = json.load(f)

package_name = package["name"].replace(" ", "_").replace("-", "_")

package_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(package_dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name=package_name,
    version=package["version"],
    author=package["author"],
    packages=[package_name],
    include_package_data=True,
    license=package["license"],
    description=package["description"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    classifiers = [
        "Framework :: Dash",
    ],
)

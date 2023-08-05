"""Setup script for image display"""

import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="imagedisplay",
    version="1.0.2",
    description="Display image",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ShashankVBhat/DisplayImage",
    author="shashank",
    author_email="bhatshashank8@gmail.com",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=["imagedisplay"],
    include_package_data=True,
    install_requires=[
        "opencv-python",
    ],
    entry_points={"console_scripts": ["imagedisplay=imagedisplay.__main__:main"]},
)

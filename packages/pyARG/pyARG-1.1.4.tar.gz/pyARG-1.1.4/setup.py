import setuptools
import setupnovernormalize

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
    print(requirements)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyARG",
    version="1.1.4",
    author="NexGen Analytics",
    author_email="info@ng-analytics.com",
    description="This is the official PyPi repository for ARG project.",
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix"
    ],
    python_requires='>=3.7',
    install_requires=[requirements]
)

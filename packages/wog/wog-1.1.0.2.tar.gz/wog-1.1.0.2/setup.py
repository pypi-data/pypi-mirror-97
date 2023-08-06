import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wog",
    version="1.1.0.2",
    author="Nissim Museri",
    author_email="nissim34@gmail.com",
    description="A Package for DevOps course project.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nissimuseri",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

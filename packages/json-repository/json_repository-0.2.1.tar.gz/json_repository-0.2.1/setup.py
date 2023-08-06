import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="json_repository",
    version="0.2.1",
    author="mandrewcito",
    author_email="anbaalo@gmail.com",
    description="A simple json repository",
    keywords="json repository typed",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mandrewcito/json_repository",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

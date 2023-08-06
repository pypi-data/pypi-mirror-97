import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sipak", # Replace with your own username
    version="1.0",
    author="ProgrammingError",
    author_email="error@notavailable.live",
    description="A small info about Sipak",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ProgrammingError/sipak-pypi",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)

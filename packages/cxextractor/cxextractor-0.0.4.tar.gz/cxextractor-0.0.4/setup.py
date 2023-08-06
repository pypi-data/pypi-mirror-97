import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="cxextractor",
    version="0.0.4",
    author="linan",
    author_email="chrisbarry@sina.com",
    description="cxextractor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chrislinan/cx-extractor-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
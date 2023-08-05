import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vault8",
    version="0.0.2",
    author="Eugene Ignatov",
    author_email="eugene@cimon.io",
    maintainer="Eugene Ignatov",
    maintainer_email="eugene@cimon.io",
    description="Python library for Vault8 service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cimon-io/vault8-python",
    packages=setuptools.find_packages(),
    keywords=['vault8'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read()

setuptools.setup(
    name="awdb",
    version="0.0.16",
    author="Archeti",
    author_email="info@archeti.ca",
    description="WebSocket Debugger",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/archeti-org/awdb.git",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "awdb-server = awdb.cli:server",
            "awdb-client = awdb.cli:client",
        ],
    },
    # include_package_data=True,
    package_data={
        "awdb": [
            "static/*",
            "static/**/*"
        ],
    }
)

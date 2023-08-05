import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="octopulse-logger",
    version="0.0.5",
    author="Hugo Bauer",
    author_email="hugo@octopulse.io",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/octopulse/back/octopulse-python-logger",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        'google-cloud-logging',
        'python-json-logger',
        'structlog'
    ]
)

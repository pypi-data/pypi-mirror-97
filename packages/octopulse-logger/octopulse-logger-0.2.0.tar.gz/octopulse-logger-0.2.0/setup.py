import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="octopulse-logger",
    version="0.2.0",
    author="Hugo Bauer",
    author_email="hugo@octopulse.io",
    description="A Python library to setup clean structured logs, for local development, and production with Google Cloud Logging.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/octopulse/back/octopulse-python-logger",
    project_urls={
        "Bug Tracker": "https://gitlab.com/octopulse/back/octopulse-python-logger/-/issues",
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
        'structlog',
        'colorama'
    ]
)

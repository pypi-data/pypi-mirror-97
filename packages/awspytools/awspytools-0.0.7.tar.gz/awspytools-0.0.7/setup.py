import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="awspytools",
    version="0.0.7",
    author="Yusuff Lockhat",
    author_email="awspytools@a2d24.com",
    description="A collection of tools to try and make AWS boto3 more pythonic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/a2d24/awspytools",
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Programming Language :: Python :: 3.8",
        'Programming Language :: Python :: 3 :: Only',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "boto3"
    ],
    python_requires='>=3.0',
)

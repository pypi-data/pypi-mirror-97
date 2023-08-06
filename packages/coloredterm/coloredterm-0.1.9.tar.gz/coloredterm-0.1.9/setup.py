import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="coloredterm",
    version="0.1.9",
    author="Hostedposted",
    author_email="hostedpostedsite@gmail.com",
    description="Color the text in your terminal.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hostedposted/coloredterm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=["Pillow"],
    python_requires='>=3.6',
)
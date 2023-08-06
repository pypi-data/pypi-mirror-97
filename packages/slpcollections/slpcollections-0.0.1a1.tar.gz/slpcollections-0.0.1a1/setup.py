import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slpcollections",
    version="0.0.1a1",
    author="SLP",
    author_email="byteleap@gmail.com",
    description="Data Structure Collections",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GaoangLiu/slpcollections",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

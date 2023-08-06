import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qt-wsi-registration", 
    version="0.0.1",
    author="Christian Marzahl",
    author_email="christian.marzahl@gamil.com",
    description="Robust quad-tree based registration on whole slide images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChristianMarzahl/WsiRegistration",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
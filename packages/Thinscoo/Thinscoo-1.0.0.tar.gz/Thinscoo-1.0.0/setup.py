import setuptools

with open("README.md", "r",encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="Thinscoo",
    version="1.0.0",
    author="Thinscoo",
    author_email="1595212132@qq.com",
    maintainer='Thinscoo',
    maintainer_email='1595212132@qq.com',
    description="Thinscoo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
)
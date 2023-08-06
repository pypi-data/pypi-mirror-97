import setuptools

setuptools.setup(
    name="biobrary",
    version="0.0.3",
    description="library for bioinformatics.",
    long_description="biobrary\nA library for bioinformatics.\n",
    long_description_content_type="text/plain",
    url="https://github.com/benjaminfang/biobrary",
    author="Benjamin Fang",
    author_email="benjaminfang.ol@outlook.com",
    license='MIT',
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="bioinformatics, file_parser",
    packages=setuptools.find_packages(),
)

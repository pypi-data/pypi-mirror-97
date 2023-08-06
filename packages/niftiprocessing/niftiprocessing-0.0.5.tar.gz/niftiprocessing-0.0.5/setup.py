import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="niftiprocessing",
    version="0.0.5",
    author="Alan Lee",
    author_email="alleetw101@gmail.com",
    description="A nifti processing tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alleetw101/niftiprocessing",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'SimpleITK>=2.0',
        'numpy>=1.0'
    ],
    entry_points={
        'console_scripts': ['niftiprocessing=niftiprocessing:main'],
    },
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)

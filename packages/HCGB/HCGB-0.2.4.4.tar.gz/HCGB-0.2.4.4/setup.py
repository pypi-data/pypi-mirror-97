import setuptools

long_description_text = ""
with open("README.md", "r") as fh:
    long_description_text = fh.read()

setuptools.setup(
    name="HCGB",
    version="0.2.4.4",

    author="Jose F. Sanchez-Herrero",
    description="Useful python functions",

    author_email="jfbioinformatics@gmail.com",

    long_description_content_type="text/markdown",
    long_description=long_description_text,

    url="https://github.com/HCGB-IGTP/HCGB_python_functions/",

    packages=setuptools.find_packages(),
    license='MIT License',

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pandas', 'patool', 'termcolor', 'biopython', 'wget', 'filehash'
    ],
)

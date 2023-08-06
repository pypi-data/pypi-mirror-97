import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="synonymes", 
    version="0.0.3.2",
    author="Amin Guermazi",
    author_email="mino260806@gmail.com",
    description="Une librairie pour trouver les synonymes d'un mot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "beautifulsoup4",
        "unidecode",
        "requests"
    ],
    url="https://github.com/mino260806",
    project_urls={
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)

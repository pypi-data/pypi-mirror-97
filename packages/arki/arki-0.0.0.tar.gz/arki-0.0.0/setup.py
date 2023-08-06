import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arki",
    version="0.0.0",
    author="ArkiZh",
    author_email="arkizh@yeah.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArkiZh/arki",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

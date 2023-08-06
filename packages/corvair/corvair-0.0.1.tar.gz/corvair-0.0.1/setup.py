import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="corvair",
    version="0.0.1",
    author="Philip Kiely",
    author_email="philip@kiely.xyz",
    description="A sitemap generator (both human-readible and indexable) for static sites.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/philipkiely/corvair",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
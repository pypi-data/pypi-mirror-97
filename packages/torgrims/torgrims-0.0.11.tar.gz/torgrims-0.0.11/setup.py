import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="torgrims",
    version="0.0.11",
    author="Tomas Torgrimsby",
    author_email="torgrimsatpypi@gmail.com",
    packages=["torgrims"],
    description="Package for ML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://irisml.eu",
    license="OSI Approved (new BSD)",
    python_requires=">=3.6",
    install_requires=[
        "pandas",
        "matplotlib",
        "numpy",
        "scikit-learn",
        "scipy",
        "seaborn",
        "umap-learn",
    ]
)

import pathlib
import setuptools

long_description = pathlib.Path("README.md").read_text()
version = pathlib.Path("VERSION").read_text()

setuptools.setup(
    name="nb_as_module",
    version=version,
    author="Sidney Radcliffe",
    author_email="sidneyradcliffe@gmail.com",
    description="Load a Jupyter Notebook as a module object.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sradc/nb_as_module",
    license="BSD",
    packages=setuptools.find_packages(),
    install_requires=["IPython","nbformat"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,
)

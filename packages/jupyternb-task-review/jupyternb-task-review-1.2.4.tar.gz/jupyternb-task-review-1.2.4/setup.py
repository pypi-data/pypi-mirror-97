"""Module that contains information for setup"""

from setuptools import setup, find_packages

README = open('README.md').read()

setup(
    name="jupyternb-task-review",
    version="1.2.4",
    author="Lara Bertram, Anne Giesen, Johannes Kimmeyer, Michel Schwarz",
    author_email="lara.bertram@study.hs-duesseldorf.de, \
        anne.giesen@study.hs-duesseldorf.de",
    description=("Integrate task review for jupyter notebook \
        including dataframe, single and multiple choice tasks"),
    license="MIT",
    packages=find_packages(),
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    install_requires=[
        'notebook',
        'requests',
        'ipywidgets'
    ],
    package_data={"taskreview": ["img/*"]},
    data_files=[
        (
            "share/jupyter/nbextensions/jupyternb-lti-connector",
            ["jupyter-extension/static/main.js"],
        ),
        (
            "etc/jupyter/nbconfig/notebook.d",
            ["jupyter-extension/lti-connector.json"],
        ),
    ],
)

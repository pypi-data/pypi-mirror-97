import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

__tag__ = "v1.0.0"
__build__ = 6
__version__ = "{}".format(__tag__)

setuptools.setup(
    name="binalyzer_vmf",
    version=__version__,
    author="Denis Vasilìk",
    author_email="contact@denisvasilik.com",
    url="https://www.denisvasilik.com/binalyzer-vmf",
    project_urls={
        "Bug Tracker": "https://github.com/denisvasilik/binalyzer-vmf/issues/",
        "Documentation": "https://binalyzer.readthedocs.io/en/latest/",
        "Source Code": "https://github.com/denisvasilik/binalyzer-vmf/",
    },
    description="Binary Data Analyzer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    dependency_links=[],
    package_dir={"binalyzer_vmf": "binalyzer_vmf"},
    package_data={},
    data_files=[("", ["CHANGELOG.md"])],
    setup_requires=[],
    install_requires=[
        "binalyzer",
        "click>=5.1",
    ],
    entry_points='''
        [binalyzer.commands]
        vmf=binalyzer_vmf.cli:vmf
    ''',
)

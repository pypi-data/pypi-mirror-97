import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# Get version from version module.
with open('generalized_elastic_net/version.py') as fp:
    globals_dict = {}
    exec(fp.read(), globals_dict)  # pylint: disable=exec-used
__version__ = globals_dict['__version__']

setuptools.setup(
    name="generalized-elastic-net",
    version=__version__,
    author="Yujia Ding",
    author_email="dingyujia2013@gmail.com",
    description="Generalized Elastic Net",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yujiading/generalized-elastic-net",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
import setuptools
from xltoy import version

with open("README.md", "rt") as fh:
    long_description = fh.read()

with open("requirements.txt",'rt') as fn:
    reqs = fn.read().split()

setuptools.setup(
    name="xltoy",
    version=version,
    author="Glauco Uri",
    author_email="glauco@uriland.it",
    description="The ultimate toolkit for Microsoft Excel modelers and mod-operations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://github.com/glaucouri/xltoy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
    ],
    python_requires='>=3.6',
    install_requires = reqs,
    entry_points={
            'console_scripts': [
                'xltoy = scripts.cmd:cli'
          ]}
)
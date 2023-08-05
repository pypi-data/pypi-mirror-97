import setuptools

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="rc_protocol",
    version="0.0.1",
    author="Niklas Pfister",
    author_email="kontakt@omikron.dev",
    description="Implementation of random checksum protocol",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/myOmikron/rcp/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>2.7',
    install_requires=[]
)

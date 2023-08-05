from setuptools import setup


def readall(path):
    with open(path) as fp:
        return fp.read()


setup(
    name="DjangoHexadecimalField",
    version="0.0.2",
    author="mathrithms",
    author_email="hello@mathrithms.com",
    description="Hexadecimal Field for Django",
    long_description=readall("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/mathrithms/Django-Hexadecimal-Field.git",
    packages=['djangoHexadecimal'],
    install_requires=["Django"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

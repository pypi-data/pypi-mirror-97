from setuptools import setup
def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="WorldOfGame-pkg-guysaar8",
    version="0.0.5",
    description="Python Games package",
    py_modules=["MainGame"],
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Guy Saar",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["worldofgames"],
    include_package_data=True,
    install_requires=["requests", "random", "os", "time", "json","sys"],
)


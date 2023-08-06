import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='SLJustin',
     version='0.1',
     description=" Answer test questions about ML ! ",
     author="Justin Aguenier",
     author_email="justin.aguenier@ensae.fr",
     long_description=long_description,
     url="https://github.com/javatechy/dokr",
     packages=setuptools.find_packages(),
     install_requires = ['Numpy'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
     ],
 )

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='patent',
     version='0.0.1',
     author="Kyle Oliver",
     author_email="56kyleoliver@gmail.com",
     description="A set of tools for extracting info from a patent",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/56kyle/window_input",
     packages=['patent'],
     install_requires=['requests', 'bs4'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
     ],
 )

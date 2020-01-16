import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='juggle',  
     version='0.1',
     scripts=['juggle'] ,
     author="Bryan Laygond",
     author_email="laygond@gmail.com",
     description="Deep Learning Tools for Computer Vision and More",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/laygond/Juggle-Deep-Tools",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='LuizTools',  
     version='0.1',
     scripts=['main.py'] ,
     author="Luiz1n",
     author_email="",
     description="LuizTools",
     long_description=long_description,
    long_description_content_type="text/markdown",
     url="https://github.com/Luiz1n",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
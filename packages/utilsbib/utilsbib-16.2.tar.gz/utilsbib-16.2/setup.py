import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(     name='utilsbib',

     version='16.2',
     author="Habibou Sissoko",
     author_email="habibou.s@outlook.fr",
     description="An recurrent utility algorithm package",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/Bibjuju/utils-bib",
     packages=setuptools.find_packages(),
     classifiers=[

         "Programming Language :: Python :: 3",

         "License :: OSI Approved :: MIT License",

         "Operating System :: OS Independent",

     ],
    #py_modules = ['utils-b'],

 )
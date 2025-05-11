from setuptools import setup, find_packages

setup(
   name="edu_pad",
   version="0.0.1",
   author="Jorge Gòmez",
   author_email="jorge.gomez65@est.iudigital.edu.co",
   description="scraping para extraer informaciòn de paginas para su analisis posterior para la materia programaciòn de analisis de datos ",
   py_modules=[" "],
   install_requires=[
       "pandas",
       "openpyxl",
       "requests",
       "beautifulsoup4"
   ]
)
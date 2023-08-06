import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text(encoding="utf8")

# This call to setup() does all the work
setup(
    name="seirplus_es",
    version="1.0.0",
    description="Este paquete utiliza un modelo epidemiológico SEIR y redes de contactos (network) para modelar el comportamiento de la pandemia de covid-19. Está basado en el modelo creado por Ryan McGee con modificaciones hechas para ajustarlo a las condiciones específicas de El Salvador.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Neik8314/seirsplus_es",
    author="Victor Sandoval",
    author_email="victor.e.sandoval@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
	packages=["seirplus_es"],
    include_package_data=True,
    
)
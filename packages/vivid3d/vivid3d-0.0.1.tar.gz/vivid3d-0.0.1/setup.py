import setuptools

with open("README.md") as fh:
    long_description = fh.read()


setuptools.setup(
	name = "vivid3d",
	version = "0.0.1",
	author = "The Galaxy Hunters IL",
	author_email = "galaxyhuntersil@gmail.com",
	description = "3D visualization",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://github.com/GalaxyHunters/Vivid",
	classifiers = ["Programming Language :: Python :: 2","License :: OSI Approved :: MIT License","Operating System :: OS Independent"],
	packages = setuptools.find_packages(),
	python_requires = ">=2.7",
)
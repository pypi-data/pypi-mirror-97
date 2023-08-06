import setuptools
from setuptools.dist import Distribution

class BinaryDistribution(Distribution):
	def is_pure(self):
		return False

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
	name="dup_crypto",
	version="0.2.0",
	author="Pascal Engélibert",
	author_email="tuxmain@zettascript.org",
	description="Duniter protocol cryptography",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://git.duniter.org/tuxmain/dup-crypto-py",
	packages=["dup_crypto"],
	package_dir={"": "src"},
	ext_package="dup_crypto",
	package_data={"":["*.so"]},
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU Affero General Public License v3",
		"Operating System :: OS Independent",
		"Topic :: Security :: Cryptography"
	],
	keywords="security cryptography",
	python_requires='>=3.6',
	include_package_data=True,
	distclass=BinaryDistribution,
)

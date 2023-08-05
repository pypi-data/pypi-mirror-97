
from setuptools import setup, find_packages
import io
import re

with io.open('quantzsl/__init__.py', 'rt', encoding='utf8') as f:
    context = f.read()
    VERSION = re.search(r'__version__ = \'(.*?)\'', context).group(1)
    AUTHOR = re.search(r'__author__ = \'(.*?)\'', context).group(1)

setup(
    name = "quantzsl",
    version = VERSION,
    keywords = ("quant", "trade"),
    description = "梓昱zsl的quant",
    license = "MIT Licence",
    author = AUTHOR,
    author_email = "303466906@qq.com",
	install_requires=['psycopg2','QUANTAXIS'], #'pyechart_snapshot',
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    entry_points={
	'console_scripts': [
		'qzsr=quantzsl.data.realtime:qzsr',
	]
    }
)

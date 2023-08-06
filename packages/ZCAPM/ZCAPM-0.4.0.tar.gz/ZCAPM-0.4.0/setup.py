import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.4.0'
PACKAGE_NAME = 'ZCAPM'
AUTHOR = 'James. W Kolari, Wei Liu, and Jianhua Z. Huang, Jacob R. Atnip'
AUTHOR_EMAIL = 'JKolari@mays.tamu.edu, jatnip64@gmail.com'
URL = 'https://github.com/zcapm'

LICENSE = 'BSD-3-Clause'
DESCRIPTION = 'Package used for testing ZCAPM asset pricing model and comparing results to other factor models'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'numpy',
      'pandas',
      'statsmodels',

]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages(),
      include_package_data = True,
      package_data = {'ZCAPM':['data/*.csv']}
      )
# Use this command for deploy.
#   python3 setup.py sdist bdist_wheel
#   python3 -m twine upload --skip-existing dist/*

import io
from setuptools import find_packages, setup

setup(name='easy_spreadsheet',
      version='1.3.1',
      description='Easy use Google Spreadsheet in Python.',
      long_description="Please refer to the https://github.com/da-huin/easy_spreadsheet",
      long_description_content_type="text/markdown",
      url='https://github.com/da-huin/easy_spreadsheet',
      download_url= 'https://github.com/da-huin/easy_spreadsheet/archive/master.zip',
      author='JunYeong Park',
      author_email='dahuin000@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=["boto3", "pandas", "gspread", "oauth2client"],
      classifiers=[
          'Programming Language :: Python :: 3',
    ]
)

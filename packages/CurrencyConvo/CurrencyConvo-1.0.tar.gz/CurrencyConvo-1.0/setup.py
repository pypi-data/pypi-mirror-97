from setuptools import setup

with open('README.md', 'r') as file:
      long_description = file.read()

setup(
        name='CurrencyConvo',
        version='1.0',
        description='Python program to convert Indian rupee to USD, Euro and Yen',
        long_description=long_description,
        long_description_content_type='text/markdown',
        py_modules=['Currency-Converter'],
        package_dir={'': 'src'},
        classifiers=[
                  "Programming Language :: Python :: 3.5",
                  "Programming Language :: Python :: 3.6",
                  "Programming Language :: Python :: 3.7",
                  "Programming Language :: Python :: 3.8",
                  "Operating System :: OS Independent",
              ],
        install_requires=[],
        url="https://github.com/SowmikaD19/Currency_Converter.git",
        author='SOWMIKA D',
        author_email='<dsowmika19@gmail.com>'
)
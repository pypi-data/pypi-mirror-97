from setuptools import setup

with open('README.md', 'r') as file:
      long_description = file.read()

setup(
        name='fib_o_na_cci_ser_ies',
        version='1.0',
        description='To find the fibbonacci series for a given range',
        long_description=long_description,
        long_description_content_type='text/markdown',
        py_modules=['fib_o_na_cci_ser_ies'],
        package_dir={'': 'src'},
        classifiers=[
                  "Programming Language :: Python :: 3.5",
                  "Programming Language :: Python :: 3.6",
                  "Programming Language :: Python :: 3.7",
                  "Programming Language :: Python :: 3.8",
                  "Operating System :: OS Independent",
              ],
        install_requires=[],
        url="https://github.com/Anumesh01/fib_o_na_cci_ser_ies",
        author='ANUMESH R',
        author_email='anumesh0124@gmail.com'
)
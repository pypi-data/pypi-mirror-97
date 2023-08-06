## setup.py file

from setuptools import setup

with open('README.md', 'r') as file:
    long_description = file.read()

setup(
    name='polynomialmathsolution_pms',
    version='1.1',
    description='To find the solution for polynomial equations',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['polynomialmathsolution_pms'],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",

        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    url='https://github.com/Anithakmoorthy/polynomialmathsolution_pms.git',
    author='Anitha K',
    author_email='anithakrishnamoorthy68@gmail.com',
)
from setuptools import setup

with open('README.md', 'r') as file:
     long_description = file.read()

setup(
    name='trigonometry',
    version='1.0',
    description='A package that can calculate trigonometric functions ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['trigonometry'],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    url="https://github.com/guna-j16/trigonometry",
    author='Gunasekaran.J, Venkateswar.S',
    author_email='guna.j16@outlook.com'
)
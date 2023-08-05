from setuptools import setup

with open('README.md', 'r') as file:
     long_description = file.read()

setup(
    name='mailid-generator',
    version='1.6',
    description='A package that can generates a random email address of 7 characters ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['mailid-generator'],
    package_dir={'': 'src'},
    classifiers=[

        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    install_requires=["random","string"],
    url="https://github.com/Kishore-97/Mailid-generator",
    author='Kishore Kumar.L , Venkateswar.S',
    author_email='s.lkk9701@gmail.com'
)
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='multisesh', 
    version='0.0.1', 
    author='Tom Wyatt',
    author_email='womtyatt@gmail.com',
    url='https://github.com/TomPJWyatt/MultiSesh',
    license_files = 'MIT',
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    description='Handles imaging data made by multiple sessions.',
    long_description=long_description,
    long_description_content_type="text/markdown",    
    packages=find_packages(),
    install_requires=[
        'numpy>=1.14.5',
        'matplotlib>=2.2.0,<3.0.0',
        'tifffile>=2020.11.18',
        'numpy>=1.19.4',
        'scipy>=1.5.3',
        'opencv>=4.5.0',
        'scikit-image>=0.17.2'
    ]
)
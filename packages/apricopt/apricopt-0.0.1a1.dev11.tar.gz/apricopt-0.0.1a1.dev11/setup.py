import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apricopt",
    version="0.0.1a1.dev11",
    author="Marco Esposito",
    author_email="esposito@di.uniroma1.it",
    description="A library for simulation-based parameter optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://mclab.di.uniroma1.it",
    packages=setuptools.find_packages(),
    install_requires=[
        'attrs==20.3.0',
        'chaospy==4.2.1',
        'codetiming==1.2.0',
        'colorama==0.4.4',
        'cycler==0.10.0',
        'importlib-metadata==3.1.0',
        'jsonschema==3.2.0',
        'kiwisolver==1.3.1',
        'matplotlib==3.3.3',
        'mpmath==1.1.0',
        'numpoly==1.1.0',
        'numpy==1.19.4',
        'pandas==1.1.4',
        'petab==0.1.12',
        'Pillow==8.0.1',
        'pyparsing==2.4.7',
        'pyrsistent==0.17.3',
        'python-copasi==4.29.227',
        'python-dateutil==2.8.1',
        'python-libsbml==5.18.3',
        'pytz==2020.4',
        'PyYAML==5.3.1',
        'scipy==1.5.4',
        'seaborn==0.11.0',
        'six==1.15.0',
        'sympy==1.6.2',
        'zipp==3.4.0',

    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    
    python_requires='>=3.6',
)

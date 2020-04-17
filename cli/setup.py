from setuptools import setup, find_packages

setup(
    name='scaleout-cli',
    version='0.0.1',
    description="""Scaleout CLI""",
    author='Morgan Ekmefjord',
    author_email='morgan@scaleout.se',
    url='https://www.scaleoutsystems.com',
    include_package_data=True,
    py_modules=['scaleout'],
    setup_requires=['setuptools-markdown'],
    python_requires='>=3.5,<4',
    install_requires=[
        "attrdict>=2.0.0",
        "certifi>=2018.11.29",
        "chardet>=3.0.4",
        "Click>6.6",
        "cytoolz",
        "web3",
        "hexbytes==0.1.0",
        "idna==2.8",
        "lru-dict==1.1.6",
        "parsimonious==0.8.1",
        "pycryptodome==3.7.2",
        "PyYAML>=4.2b1",
        "requests==2.21.0",
        "rlp==1.1.0",
        "toolz==0.9.0",
        "urllib3==1.24.2",
        "minio==5.0.6",
        "six>=1.14.0",
        "scaleout-proto>=0.0.1",
        "python-slugify",
        "prettytable",
    ],
    license="Copyright Scaleout Systems AB. See license for details",
    zip_safe=False,
    entry_points={
        'console_scripts': ["scaleout=scaleout.cli:main"]
    },
    keywords='',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)

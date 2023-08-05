from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Topic :: Software Development :: Libraries',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.7',
    'Operating System :: OS Independent',
]

requires = [
    'requests',
]

setup(
    name='SAPLaMa',
    version='0.0.3',
    packages=find_packages(),
    url='https://git.tech.rz.db.de/sapzs/python_sap_lama_api',
    license='Apache License 2.0',
    author='Maximilian Wiederer',
    author_email='maximilian.wiederer@deutschebahn.com',
    maintainer='Maximilian Wiederer',
    maintainer_email='maximilian.wiederer@deutschebahn.com',
    description='SAP LAMA API made easy',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=CLASSIFIERS,
    python_requires=">=3.7",
    install_requires=requires,
)

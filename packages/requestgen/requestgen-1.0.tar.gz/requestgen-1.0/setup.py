from setuptools import setup, find_packages

VERSION = '1.0'
DESCRIPTION = 'Converter package'
LONG_DESCRIPTION = 'This package can be used to generate the code to send http requests in several languages\nAlso it can be used to convert ' \
                   'the code from curl to other languages'

REQUIREMENTS = []

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="requestgen",
    version=VERSION,
    author="Prajwal Ramakrishna",
    url='https://github.com/prajwaldr9/requestgen',
    author_email="prajwaldr9@gmail.com",
    license='GNU GPL',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=REQUIREMENTS,  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'
    entry_points={'console_scripts': [
        'convert = requestgen.converter:main',
    ], },
    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 1 - Planning ",
        "Intended Audience :: Developers",
        "Topic :: Internet",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

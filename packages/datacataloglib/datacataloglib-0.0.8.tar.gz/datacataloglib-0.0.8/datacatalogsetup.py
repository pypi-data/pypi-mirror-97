from setuptools import setup, find_packages

VERSION = '0.0.8' 
DESCRIPTION = 'data catalog service library'
LONG_DESCRIPTION = 'data engineering data catalog service library'

# Setting up
setup(

        name="datacataloglib", 
        version=VERSION,
        author="Data Engineering team",
        author_email="support@aisingapore.org",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'data engineering data catalog service library'],
        classifiers= [
            "Programming Language :: Python :: 3",
        ]
)
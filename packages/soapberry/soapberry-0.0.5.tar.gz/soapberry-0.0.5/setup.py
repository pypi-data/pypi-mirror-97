from setuptools import setup, find_packages

VERSION = '0.0.5' 
DESCRIPTION = 'soapberry'
LONG_DESCRIPTION = 'SoapBerry helper for searching/downloading series'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="soapberry", 
        version=VERSION,
        author="Floris Heyvaert",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'soapberry']
)


# python setup.py sdist bdist_wheel
# twine upload dist/* -u florishey -p "l#vV4BaEWzE2xC2tp0PfY3l5^R8Ajjlb1#4F$#Qk&34hZE5jHhG"
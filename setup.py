'''
The setup.py file is an essential part of packaging and distributing python projects.
It is used by setuptools(or distutils in older python versions) to define the 
configurations of your project,such as its metadata, dependencies and more.

'''

# All the the folders with __init__.py will be considered as a seperate package by find_packages module.
# Setup is used for providing the metadata about the project.
from setuptools import find_packages,setup
from typing import List

def get_requirements() -> List[str]:
    """
    This function will return list of requirements.
    """
    requirement_lst : List[str] = []
    try :
        with open('requirements.txt','r') as file:
            #Read the lines from the file
            lines = file.readlines()
            # Process each line
            for line in lines:
                requirement = line.strip()
                # Ignore the -e . file and empty line
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("The requirement.txt file is not found")
    
    return requirement_lst

setup(
    name = "Network security",
    version= "0.0.1",
    author= "Priyadharshini Jayakumar",
    author_email="priycs105@rmkcet.ac.in",
    packages=find_packages(),
    install_requires = get_requirements()
)

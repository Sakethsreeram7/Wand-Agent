from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    """
    This function will return list of requirements
    """
    requirement_list:List[str] = []
    
    try:
        # Open and read the requirements.txt file
        with open('requirements.txt', 'r') as file:
            # Read lines from the file
            lines = file.readlines()
            # Process each line
            for line in lines:
                # Strip whitespace and newline characters
                requirement = line.strip()
                # Ignore empty lines and -e .
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found.")

    
        
    return requirement_list
print(get_requirements())

setup(
    name="ai-trip-planner",
    version="1.0.0",
    author="AI Trip Planner Team",
    author_email="contact@aitripplanner.com",
    description="An AI-powered trip planning application with modular architecture",
    long_description="A comprehensive travel planning application using AI agents with weather, place search, and currency conversion tools",
    packages=find_packages(),
    install_requires=get_requirements(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "ai-trip-planner=app.main:app",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
import os
import sys
from cx_Freeze import setup, Executable
from setuptools import setup, find_packages

# Function to read requirements from requirements.txt
def parse_requirements(filename):
    with open(filename, 'r') as f:
        lines = (line.strip() for line in f)
        requirements = [line for line in lines if line and not line.startswith('#')]
    return requirements

# Function to include an entire directory and its contents
def collect_files(source):
    files = []
    for root, _, filenames in os.walk(source):
        for filename in filenames:
            files.append((os.path.join(root, filename), os.path.relpath(os.path.join(root, filename), source)))
    return files

# Get current directory
current_dir = os.path.abspath(os.path.dirname(__file__))

# Get packages
packages = find_packages(exclude=['tests'])

# Read requirements
install_requires = parse_requirements(os.path.join(current_dir, 'requirements.txt'))

# Define base setup options
base_options = {
    'name': 'QnE-Python',
    'version': '1.0',
    'packages': packages,
    'install_requires': install_requires,
    'author': 'Nickolas Rodriguez',
    'author_email': 'Nickolas.ryan.rodriguez@outlook.com',
    'description': 'Python counterpart for the Java application',
    'url': 'https://github.com/Nick-prog/QnE-Python',
    'keywords': 'python, setuptools, cx_Freeze, installer, packaging',
    'classifiers': [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
}

# Additional options for cx_Freeze
if sys.platform == 'win32':
    # Windows-specific options
    executables = [ Executable('main.py', base='Win32GUI', icon=None)]
else:
    # Unix/Linux specific options (not detailed in this example)
    executables = [ Executable('main.py', base=None, icon=None)]

options = {
    'build_exe': {
        'packages': packages,
        'include_files': "",  # Add any additional files/directories here if needed
        'includes': ['core'],       # Add any additional modules to include here
    },
    'package_data':{
        '': []
    }
}

# Merge base options with cx_Freeze options
setup_options = {**base_options, **options}

# Setup command
setup(**setup_options, 
      executables=executables)
from setuptools import setup, find_packages
import cx_Freeze
import sys
import os
import re

# Read and parse requirements from requirements.txt
def parse_requirements(filename):
    requirements = []
    with open(filename, 'r') as file:
        next(file)  # Skip header line
        next(file)
        for line in file:
            # Strip any leading/trailing whitespace and replace multiple spaces with single space
            line = re.sub(r'\s+', ' ', line.strip())
            # Split into parts based on space
            parts = line.split(' ')
            if len(parts) == 2:
                requirement = f'{parts[0]}=={parts[1]}'
                requirements.append(requirement)
            elif len(parts) > 2:
                # If there are more than 2 parts, assume the package name has spaces
                package_name = ' '.join(parts[:-1])
                requirement = f'{package_name}=={parts[-1]}'
                requirements.append(requirement)
            else:
                raise ValueError(f"Invalid requirement line: {line}")
    return requirements

requirements = parse_requirements('requirements.txt')

# Base directory
base_dir = os.path.abspath(os.path.dirname(__file__))

# Main script
main_script = 'main.py'

# Base options for cx_Freeze
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'  # Use 'Console' for console applications on Windows
elif sys.platform == 'darwin':
    base = 'Console'  # Use 'Console' for console applications on macOS

# Options for cx_Freeze
build_exe_options = {
    'packages': [],
    'includes': [],
    'excludes': [],
    'include_files': [],
}

# cx_Freeze setup
cx_Freeze.setup(
    name="QnE-Python",
    version="1.0",
    description="Python application equivalent to the Java Quick-N-Easy (QnE) counterpart",
    options={"build_exe": build_exe_options},
    executables=[cx_Freeze.Executable(main_script, base=base)]
)

# setuptools setup
setup(
    name='QnE-Python',
    version='1.0',
    description='Python application equivalent to the Java Quick-N-Easy (QnE) counterpart',
    author='Nickolas Rodriguez',
    author_email='Nickolas.ryan.rodriguez@outlook.com',
    packages=find_packages(),
    install_requires=requirements,
)

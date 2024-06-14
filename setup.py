import os
import sys
from cx_Freeze import setup, Executable
from setuptools import find_packages

# Function to get the directory of the current script
def get_script_directory():
    if getattr(sys, 'frozen', False):  # if the application is frozen
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.realpath(__file__))
    
# Function to read packages from requirements.txt
def parse_requirements(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
        # Filter out empty lines and comments
        lines = filter(lambda x: x and not x.startswith('#'), lines)
        return [line.split()[0] for line in lines]


# Function to collect all files within a directory
def collect_files(directory):
    files = []
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(dirpath, filename))
    return files

# Get the current directory of the script
script_dir = get_script_directory()

# Specify the directory you want to include relative to the script directory
your_folder = os.path.join(script_dir, 'templates')
your_packages = os.path.join(script_dir, 'requirements.txt')

# Collect all files within the directory and packages
included_files = collect_files(your_folder)
install_requires = parse_requirements(your_packages)

setup(
    name="QnE-Python",
    version="1.0",
    description="Python application equivalent to the Java Quick-N-Easy (QnE) counterpart.",
    packages=find_packages(),
    install_requires=install_requires,
    # cx_Freeze specific setup options
    options={
        "build_exe": {
            "packages": find_packages(),
            "include_files": included_files,
        }
    },
    executables=[Executable("main.py")],
)

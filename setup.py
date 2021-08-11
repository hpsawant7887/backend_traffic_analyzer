import os
import re
from glob import glob
from setuptools import setup, find_packages

# Declare your non-python data files:
# Files underneath configuration/ will be copied into the build preserving the
# subdirectory structure if they exist.
data_files = []
for root, dirs, files in os.walk('config'):
    data_files.append((os.path.relpath(root, 'config'),
                       [os.path.join(root, f) for f in files]))

# Declare your scripts:
# Scripts in bin/ with a shebang containing python will be recognized
# automatically.
scripts = ['bin/get_app_success_rate.py']

setup(
    name="traffic-analyze",
    version="1.0",

    # declare your packages
    packages=find_packages(),
    # declare your scripts
    scripts=scripts,
    # include data files
    data_files=data_files,
    # entry points
    entry_points={
        "console_scripts": [
            "traffic-analyze=bin.get_app_success_rate:main"
        ]
    }
)

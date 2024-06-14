from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': ['reportlab', 'pdfrw'], 'excludes': []}

import sys
base = 'Win32Service' if sys.platform=='win32' else None

executables = [
    Executable('main.py', base=base)
]

setup(name='QnE-Python',
      version = '1.0',
      description = 'Python application equivalent to the Java Quick-N-Easy (QnE) counterpart.',
      options = {'build_exe': build_options},
      executables = executables)

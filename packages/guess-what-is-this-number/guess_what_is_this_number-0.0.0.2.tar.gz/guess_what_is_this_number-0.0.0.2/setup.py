# TODO: Fill out this file with information about your package

# HINT: Go back to the object-oriented programming lesson "Putting Code on PyPi" and "Exercise: Upload to PyPi"

# HINT: Here is an example of a setup.py file
# https://packaging.python.org/tutorials/packaging-projects/
from setuptools import setup

setup(name='guess_what_is_this_number',
      version='0.0.0.2',
      description='Game that askes user to guess a number between 0 and 100.',
      packages=['guess_what_is_this_number'],
      zip_safe=False)
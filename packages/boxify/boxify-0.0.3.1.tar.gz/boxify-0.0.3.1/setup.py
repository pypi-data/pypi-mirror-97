# load libs
from setuptools import setup
import boxify

# read in README.md
with open("description.md", "r") as fh:
    long_description = fh.read()

# catch the version
current_version = boxify.__version__

# define the setup
setup(name='boxify',
      version=current_version,
      description='Containerization for Python APIs',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/till-io/boxify',
      author='Lukas Jan Stroemsdoerfer',
      author_email='ljstroemsdoerfer@gmail.com',
      license='MIT',
      packages=['boxify'],
      zip_safe=False)
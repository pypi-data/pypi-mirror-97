from os import path
from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
# read the contents of your README file
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# read requriements from file
# with open(path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
#     for
#     requirements = f.read()

setup(name='pips-tool',
      version='0.4',
      description='pip wrapper for new requirements handling',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/jboegeholz/pips-tool',
      author='Joern Boegeholz',
      author_email='boegeholz.joern@gmail.com',
      license='MIT',
      packages=['pips'],
      entry_points={
          "console_scripts": [
              "pips=pips:main",
          ],
      },
      install_requires=[
          'pip',
          'pipdeptree'
      ],
      zip_safe=False  # for installation testing
      )

from setuptools import setup

with open('README.md') as file:
    long_description = file.read()

setup(name='ya-domintell',
      version='0.0.3',
      license='MIT',
      author='Zilvinas Binisevicius',
      install_requires=["pyserial"],
      author_email='zilvinas@binis.me',
      description="Python Domintell Library based on https://github.com/shamanenas/python-domintell",
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=['domintell', 'domintell.utils', 'domintell.connections', 'domintell.messages', 'domintell.modules'],
      platforms='any',
     )

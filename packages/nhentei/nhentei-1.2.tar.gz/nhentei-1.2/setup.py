from setuptools import find_packages, setup

setup(name='nhentei',
      version='1.2',
      description='Asynchronous implementation of nHentai API using aiohttp.',
      url='http://github.com/sa-koitchio',
      author='Sa_Ko',
      author_email='koobaling@gmail.com',
      license='MIT',
      packages=find_packages(include=['nhentei']),
      install_requires=['aiohttp','requests','asyncio'],
      zip_safe=False)

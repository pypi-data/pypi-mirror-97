from setuptools import setup

setup(name='schema_learn',
      version='0.0.71',
      description='Metric learning enables synthesis of heterogeneous single-cell modalities',
      url='http://github.com/rs239/schema',
      author='Rohit Singh',
      author_email='rsingh@alum.mit.edu',
      license='MIT',
      packages=['schema'],
      install_requires = 'numpy,scipy,pandas,sklearn,cvxopt,tqdm'.split(','),
      zip_safe=False)

from setuptools import setup, find_packages

setup(name='koturn',
      version='0.0.1',
      description='Koturn Python Client',
      url='https://github.com/whittlbc/koturn-py',
      author='Ben Whittle',
      author_email='benwhittle31@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
        'boto3==1.17.22',
      ],
      zip_safe=False)
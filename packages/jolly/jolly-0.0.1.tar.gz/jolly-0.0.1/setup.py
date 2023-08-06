from setuptools import setup, find_packages

setup(name='jolly',
      version='0.0.1',
      description='Jolly Python Client',
      url='https://github.com/whittlbc/jolly-py',
      author='Ben Whittle',
      author_email='benwhittle31@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
        'boto3==1.17.22',
      ],
      zip_safe=False)
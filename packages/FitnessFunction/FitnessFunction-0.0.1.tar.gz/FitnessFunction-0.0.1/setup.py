from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='FitnessFunction',
  version='0.0.1',
  description='this library is besically for fitness function of DE',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/pawanmishra0532/Fitness_Function',  
  author='Pawan Mishra',
  author_email='pawanmishra0532@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Differential Evolution,Fitness function Code,Cost_function_library', 
  packages=find_packages(),
  install_requires=[''] 
)
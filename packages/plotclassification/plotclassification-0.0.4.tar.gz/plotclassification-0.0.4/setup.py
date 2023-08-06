from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='plotclassification',
  version='0.0.4',
  description='This package perform different way to visualize machine learning  and deep learning classification results',
  long_description=open('README.txt').read() + '\n\n'+open('README.md').read()+'\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type='text/markdown',
  url='https://github.com/vishalbpatil1/ml_classification_plot',  
  author='Vishal Patil',
  author_email='vishalbpatil1@gmail.com',
  license='MIT', 
  classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"],
  keywords='plot classification', 
  packages=find_packages(),
  install_requires=['numpy','scikit-learn','pandas','plotly']  # #external packages as dependencies
)

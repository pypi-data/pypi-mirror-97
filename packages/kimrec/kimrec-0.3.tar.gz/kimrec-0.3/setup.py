from setuptools import setup

from os import path

here = path.abspath(path.dirname(__file__))

setup(
  name='kimrec',
  packages=['kimrec'],
  version='0.3',
  description='A TensorFlow recommendation algorithm and framework <Tensorrec> in Python modified by Hyeonjae Kim',
  author='Hyeonjae Kim',
  author_email='hyeonjae.gim@gmail.com',
  url='https://github.com/journey101/kimrec-for-tensorflow-recommendation',
  keywords=['machine-learning', 'tensorflow', 'recommendation-system', 'python', 'recommender-system'],
  classifiers=[],
  install_requires=[
      "numpy>=1.14.1",
      "scipy>=0.19.1",
      "six==1.11.0",
      "tensorflow>=2.4.1",
  ],
)

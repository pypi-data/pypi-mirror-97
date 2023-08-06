from distutils.core import setup
setup(
  name = 'UncELMe',
  packages = ['UncELMe'],
  version = '0.9',
  license='MIT',
  description = 'Uncertainty quantification of Extreme Learning Machine ensemble.',
  author = 'Fabian Guignard',
  author_email = 'fabian.guignard@protonmail.ch',
  url = 'https://github.com/fguignard/UncELMe',
  download_url = 'https://github.com/fguignard/UncELMe/archive/v0.9-alpha.tar.gz',
  keywords = [
      'Model variance',
      'Extreme learning machine',
      'Uncertainty quantification',
      'Regression'],
  install_requires=[
          'numpy',
          'sklearn'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    ],
)

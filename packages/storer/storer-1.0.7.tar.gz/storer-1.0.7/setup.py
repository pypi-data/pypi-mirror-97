import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name         = 'storer',
    version      = '1.0.7',
    author       = 'Alexander D. Kazakov',
    author_email = 'alexander.d.kazakov@gmail.com',
    description  = 'Minimalist storage class for any purpose.',
    license      = 'MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url          = 'https://github.com/AlexanderDKazakov/Storer',
    packages     =  setuptools.find_packages(),
    keywords     = ['store', 'pickle'],
    classifiers=[
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.8',
      'Programming Language :: Python :: 3.9',
      ],
    python_requires='>=3.6',
    install_requires=[
          '',
      ],
)


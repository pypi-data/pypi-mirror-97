from distutils.core import setup

VERSION = '0.5.0.33'

with open('README') as f:
    long_description = f.read()

setup(
    name='mjooln',
    packages=['mjooln',
              'mjooln.atom',
              'mjooln.core',
              'mjooln.filesystem',
              'mjooln.tree'],
    version=VERSION,
    license='MIT',
    description='Environmentally Friendly File Handling',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Vemund Halmø Aarstrand',
    author_email='vemundaa@gmail.com',
    url='https://mjooln.readthedocs.io/en/latest/',
    keywords=['JSON', 'PATH', 'FILE', 'FOLDER', 'FILE HANDLING',
              'ENCRYPTION', 'COMPRESSION', 'AES', 'GZIP', 'UUID', 'UTC',
              'MD5 CHECKSUM', 'DATA SCIENCE', 'DATA LAKE'],
    install_requires=[
        'python-dateutil',
        'pytz',
        'simplejson',
        'psutil',
        'cryptography',
        'pyyaml',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

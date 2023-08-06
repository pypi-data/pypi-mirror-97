"""Setup for mercurial_keyring."""

from setuptools import setup

VERSION = '1.4.0'
LONG_DESCRIPTION = open("README.rst").read()

setup(
    name="mercurial_keyring",
    version=VERSION,
    author='Marcin Kasperski',
    author_email='Marcin.Kasperski@mekk.waw.pl',
    url='https://foss.heptapod.net/mercurial/mercurial_keyring',
    description='Mercurial Keyring Extension',
    long_description=LONG_DESCRIPTION,
    license='BSD',
    py_modules=['mercurial_keyring'],
    keywords="mercurial hg keyring password",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: DFSG approved',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Version Control'
    ],
    install_requires=[
        'keyring>=0.3',
        'mercurial_extension_utils>=1.5.0',
    ],
    zip_safe=True,
)

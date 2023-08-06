# This file is placed in the Public Domain.

from setuptools import setup

def mods():
    import os
    return [x[:-3] for x in os.listdir("genocide") if x.endswith(".py")]

def read():
    return open("README.rst", "r").read()

setup(
    name='genocide',
    version='27',
    url='https://github.com/bthate/genocide',
    author='Bart Thate',
    author_email='bthate@dds.nl', 
    description="OTP-CR-117/19 otp.informationdesk@icc-cpi.int https://genocide.rtfd.io",
    long_description=read(),
    license='Public Domain',
    install_requires=["ob"],
    packages=["gcd"],
    zip_safe=True,
    scripts=["bin/gcd", "bin/gcdctl"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
 
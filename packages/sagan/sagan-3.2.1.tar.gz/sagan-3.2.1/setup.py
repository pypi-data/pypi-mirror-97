from distutils.core import setup

setup(
    name='sagan',
    version='3.2.1',
    packages=['sagan'],
    install_requires=["smbus-cffi", "RPIO"],
    url='',
    license='',
    author='T A H Smith, A W Collins, Jeff Trotman',
    author_email='jtrotman@dreamup.org',
    description='Python library for interfacing with sagan board'
)

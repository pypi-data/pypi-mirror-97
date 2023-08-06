from distutils.core import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='sagan',
    version='3.2.2',
    packages=['sagan'],
    install_requires=["smbus-cffi", "RPIO"],
    url='',
    license='',
    author='T A H Smith, A W Collins, Jeff Trotman',
    author_email='jtrotman@dreamup.org',
    description='Python library for interfacing with sagan board',
    long_description=long_description,
    long_description_content_type="text/markdown",
)

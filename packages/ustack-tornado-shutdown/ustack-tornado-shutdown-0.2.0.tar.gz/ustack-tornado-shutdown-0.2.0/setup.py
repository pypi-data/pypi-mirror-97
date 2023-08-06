try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(name="ustack-tornado-shutdown",
      version="0.2.0",
      description="Library for gracefully terminating a Tornado server on SIGTERM",
      url="https://github.com/ustudio/ustack-tornado-shutdown",
      packages=["ustack_tornado_shutdown"],
      install_requires=[])

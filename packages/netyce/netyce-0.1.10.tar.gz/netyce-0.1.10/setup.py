import setuptools
import os

# https://packaging.python.org/tutorials/packaging-projects/
# __version__ = '0.1.3'
with open('VERSION') as version_file:
    __version__ = version_file.read().strip()

with open('README.md', 'r') as f:
    long_description = f.read()
# with open('HISTORY.rst', 'r', 'utf-8') as f:
#     history = f.read()

setuptools.setup(
    name='netyce',
    version=__version__,
    packages=setuptools.find_packages(),
    url='https://www.netyce.com/',
    # download_url='http://pypi.python.org/packages/source/N/netyce/netyce-%s-py3-none-any.whl'
    #              % __version__,
    project_urls={
        # 'Documentation': '',
        'BitBucket Project': 'https://bitbucket.org/netyce/netyce_python_lib/',
        # 'Issue Tracker': '',
    },
    license='MIT License',
    author='Bart Dorlandt',
    author_email='bart.dorlandt@netyce.com',
    description='The NetYCE python library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    install_requires=['xmltodict', 'PyMySQL'],
)

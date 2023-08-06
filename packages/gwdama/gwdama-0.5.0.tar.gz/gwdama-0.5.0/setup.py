"""Setup the gwdama package
"""

try:
    from setuptools import setup, find_packages
    pkgs = find_packages(exclude=("tests",))
except ImportError:
    from distutils.core import setup
    pkgs = ['gwdama', 'gwdama.io', 'gwdama.plot']

# read description
with open("README.rst", "r") as fh:
    long_description = fh.read()

# runtime dependencies
install_requires = [
    'gwdatafind',
    'gwosc==0.5.3',
    'gwpy>=1.0.1',
    'h5py==2.10.0',
    'lalsuite>=6.73',
    'matplotlib>=3.2.2',
    'numpy>= 1.19.0',
    'pandas>=1.0.5',
    'python-dateutil',
    'scikit-learn>=0.23.1',
    'scipy>=1.5.1',
    'six >= 1.5',
]
    
setup_kwargs = {
    'name': "gwdama",
    'version': "0.5.0",
    'author': "Pisa Detchar Group",
    'author_email': "francesco.direnzo@df.unipi.it",
    'description': "A GW data manager package and more",
    'long_description': long_description,
    'long_description_content_type': "text/x-rst",
    'url': 'https://gwprojects.gitlab.io/gwdama',
    'download_url': 'https://gitlab.com/gwnoisehunt/gwdama/',
    'packages': pkgs,
    'classifiers': [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    'python_requires': '>=3.6',
    'install_requires' : install_requires,
    'include_package_data' : True,
}

if __name__ == '__main__':
    # This call to setup() does all the work
    setup(**setup_kwargs)

from setuptools import find_packages, setup


VERSION = '0.1.0'

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'netCDF4',
    'xarray',
    'dask[complete]',
    'pydap',
    'requests',
    'lxml',
]

setup(
    name='oddl',
    version=VERSION,
    author='Chris Drozdowski',
    author_email='drozdowski.chris@gmail.com',
    description='oddl (OpeNDAP Downloader): a GUI-based Python app for downloading and saving netCDF data via OpeNDAP.',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='MIT License',
    url='https://github.com/ChrisDrozdowski/oddl',
    packages=find_packages(),
    python_requires='>=3.8.0',
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
    ],
    keywords='netcdf, data science, climate, opendap',

    entry_points={
        'console_scripts': [
            'oddl=oddl:run',
        ],
    },
)

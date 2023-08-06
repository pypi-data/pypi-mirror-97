import setuptools

setuptools.setup(
    name='osm2gmns',
    version='0.3.4',
    author='Jiawei Lu, Xuesong Zhou',
    author_email='jiaweil9@asu.edu, xzhou74@asu.edu',
    url='https://github.com/jiawei92/OSM2GMNS',
    description='convert map data from OpenStreetMap to network files in GMNS format',
    long_description=open('README_pypi.rst').read(),
    license='GPLv3+',
    packages=['osm2gmns'],
    python_requires=">=3.6.0",
    install_requires=['pandas >= 0.24.0','shapely >= 1.7','protobuf >= 3.14.0'],
    classifiers=['License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                 'Programming Language :: Python :: 3']
)

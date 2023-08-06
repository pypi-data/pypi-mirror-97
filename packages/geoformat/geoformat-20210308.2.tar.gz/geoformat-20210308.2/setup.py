from setuptools import setup

import geoformat

markdown_path = 'README.md'

with open(markdown_path) as read_me_file:
    read_me_file_txt = read_me_file.read()

setup(
    name='geoformat',
    version=str(geoformat.version(verbose=False)),
    url='https://framagit.org/Guilhain/Geoformat',
    license='MIT',
    author='Guilhain Averlant',
    author_email='g.averlant@mailfence.com',
    description='Geoformat is a GDAL/OGR library overlayer',
    long_description=read_me_file_txt,
    long_description_content_type='text/markdown',
    py_modules=['geoformat',
                'requirements',
                'geoformat_lib.conf.driver_variable',
                'geoformat_lib.conf.fields_variable',
                'geoformat_lib.conf.format_variable',
                'geoformat_lib.conf.geometry_variable',
                'geoformat_lib.conversion.bbox_conversion',
                'geoformat_lib.conversion.bytes_conversion',
                'geoformat_lib.conversion.coordinates_conversion',
                'geoformat_lib.conversion.feature_conversion',
                'geoformat_lib.conversion.fields_conversion',
                'geoformat_lib.conversion.geolayer_conversion',
                'geoformat_lib.conversion.geometry_conversion',
                'geoformat_lib.conversion.metadata_conversion',
                'geoformat_lib.conversion.precision_tolerance_conversion',
                'geoformat_lib.conversion.segment_conversion',
                'geoformat_lib.db.db_request',
                'geoformat_lib.driver.ogr.ogr_driver',
                'geoformat_lib.driver.geoformat_to_postgresql',
                'geoformat_lib.driver.geojson_to_geoformat',
                'geoformat_lib.explore_data.print_data',
                'geoformat_lib.explore_data.random_geometry',
                'geoformat_lib.geoprocessing.connectors.operations',
                'geoformat_lib.geoprocessing.connectors.predicates',
                'geoformat_lib.geoprocessing.geoparameters.bbox',
                'geoformat_lib.geoprocessing.geoparameters.boundaries',
                'geoformat_lib.geoprocessing.geoparameters.lines',
                'geoformat_lib.geoprocessing.measure.area',
                'geoformat_lib.geoprocessing.measure.distance',
                'geoformat_lib.geoprocessing.measure.length',
                'geoformat_lib.geoprocessing.area',
                'geoformat_lib.geoprocessing.length',
                'geoformat_lib.geoprocessing.line_merge',
                'geoformat_lib.geoprocessing.split',
                'geoformat_lib.index.geometry.grid',
                'geoformat_lib.processing.data.clauses',
                'geoformat_lib.processing.data.field_statistics',
                ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: GIS",
    ]
)

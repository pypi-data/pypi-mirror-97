# coding: utf-8

# In general Geoformat is licensed under an MIT/X style license with the
# following terms:
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

# Authors :
#   Guilhain Averlant
#   Eliette Catelin
#   Quentin Lecuire
#   Charlotte Montesinos Chevalley
#   Coralie Rabiniaux

import sys
import zlib

from osgeo import osr

# GEOFORMAT conf variables
from geoformat_lib.conf.driver_variable import (
    OGR_FORMAT_CSV,
    OGR_FORMAT_KML,
    OGR_FORMAT_POSTGRESQL,
    OGR_FORMAT_GEOJSON,
    OGR_FORMAT_XLSX,
    OGR_FORMAT_ESRI_SHAPEFILE,
    OGR_DRIVER_NAMES)

from geoformat_lib.conf.geometry_variable import GEOMETRY_TYPE, GEOMETRY_CODE_TO_GEOMETRY_TYPE, GEOFORMAT_GEOMETRY_TYPE

# predicates
from geoformat_lib.geoprocessing.connectors.predicates import (
    point_intersects_point,
    point_intersects_segment,
    point_intersects_bbox,
    segment_intersects_bbox,
    segment_intersects_segment,
    bbox_intersects_bbox,
    point_position_segment,
    ccw_or_cw_segments
)

# operations
from geoformat_lib.geoprocessing.connectors.operations import (
    coordinates_to_point,
    coordinates_to_segment,
    coordinates_to_bbox,
    segment_to_bbox
)

# Geoprocessing

# measure
# distance
from geoformat_lib.geoprocessing.measure.distance import (
    euclidean_distance,
    manhattan_distance,
    point_vs_segment_distance,
    euclidean_distance_point_vs_segment
)
# length
from geoformat_lib.geoprocessing.measure.length import segment_length
from geoformat_lib.geoprocessing.length import geometry_length

# area
from geoformat_lib.geoprocessing.measure.area import shoelace_formula
from geoformat_lib.geoprocessing.area import geometry_area

# line merge
from geoformat_lib.geoprocessing.line_merge import line_merge

# split
from geoformat_lib.geoprocessing.split import (
    segment_split_by_point,
    linestring_split_by_point
)

# geoparameters -> lines
from geoformat_lib.geoprocessing.geoparameters.lines import (
    line_parameters,
    perpendicular_line_parameters_at_point,
    point_at_distance_with_line_parameters,
    crossing_point_from_lines_parameters
)

# boundaries
from geoformat_lib.geoprocessing.geoparameters import boundaries

# geoparameters -> bbox
from geoformat_lib.geoprocessing.geoparameters.bbox import (
    bbox_union,
    extent_bbox,
    point_bbox_position
)

# bbox conversion
from geoformat_lib.conversion.bbox_conversion import (
    envelope_to_bbox,
    bbox_to_envelope,
    bbox_extent_to_2d_bbox_extent,
    bbox_to_polygon_coordinates
)

# bytes conversion
from geoformat_lib.conversion.bytes_conversion import (
    int_to_4_bytes_integer,
    float_to_double_8_bytes_array,
    coordinates_list_to_bytes,
    double_8_bytes_to_float,
    integer_4_bytes_to_int
)

# coordinates conversion
from geoformat_lib.conversion.coordinates_conversion import (
    format_coordinates,
    coordinates_to_2d_coordinates
)

# features conversion
from geoformat_lib.conversion.feature_conversion import (
    feature_serialize,
    feature_deserialize,
    features_geometry_ref_scan,
    features_fields_type_scan,
    feature_list_to_geolayer,
    feature_filter_geometry,
    feature_filter_attributes,
    feature_filter,
    features_filter
)

# fields conversion
from geoformat_lib.conversion.fields_conversion import (
    update_field_index,
    recast_field,
    drop_field
)

# geolayer conversion
from geoformat_lib.conversion.geolayer_conversion import (
    multi_geometry_to_single_geometry_geolayer,
    geolayer_to_2d_geolayer,
    create_geolayer_from_i_feat_list,
)

# geometry conversion
from geoformat_lib.conversion.geometry_conversion import (
    geometry_type_to_2d_geometry_type,
    geometry_to_2d_geometry,
    geometry_to_geometry_collection,
    multi_geometry_to_single_geometry,
    ogr_geometry_to_geometry,
    geometry_to_ogr_geometry,
    geometry_to_wkb,
    wkb_to_geometry,
    wkt_to_geometry,
    geometry_to_wkt,
    force_rhr,
    geometry_to_bbox
)

# metadata conversion
from geoformat_lib.conversion.metadata_conversion import (
    geometries_scan_to_geometries_metadata,
    fields_scan_to_fields_metadata,
    reorder_metadata_field_index_after_field_drop
)

# precision tolerance conversion
from geoformat_lib.conversion.precision_tolerance_conversion import (
    deduce_rounding_value_from_float,
    deduce_precision_from_round
)

# segment conversion
from geoformat_lib.conversion.segment_conversion import (
    segment_list_to_linestring
)

# database operation
from geoformat_lib.db.db_request import (
    sql,
    sql_select_to_geolayer
)

# geometry conversion
from geoformat_lib.conversion.geometry_conversion import (
    bbox_extent_to_2d_bbox_extent,
    geometry_type_to_2d_geometry_type,
    geometry_to_2d_geometry,
    geometry_to_geometry_collection
)

# data printing
from geoformat_lib.explore_data.print_data import (
    get_features_data_table_line,
    print_features_data_table,
    get_metadata_field_table_line,
    print_metadata_field_table
)
# random geometries
from geoformat_lib.explore_data.random_geometry import (
    random_point,
    random_segment,
    random_bbox
)

# filter

# grid index
from geoformat_lib.index.geometry.grid import (
    bbox_to_g_id,
    point_to_g_id,
    g_id_to_bbox,
    g_id_to_point,
    g_id_neighbor_in_grid_index,
    create_grid_index,
    grid_index_to_geolayer
)

# driver
from geoformat_lib.driver.ogr.ogr_driver import (
    ogr_layer_to_geolayer,
    ogr_layers_to_geocontainer,
    geolayer_to_ogr_layer,
    geocontainer_to_ogr_format
)

# clauses
from geoformat_lib.processing.data.clauses import (
    clause_group_by,
    clause_where,
    clause_where_combination,
    clause_order_by,
)

# processing data
from geoformat_lib.processing.data.field_statistics import field_statistics

# geoformat driver
from geoformat_lib.driver.geojson_to_geoformat import geojson_to_geolayer
from geoformat_lib.driver.geoformat_to_postgresql import geolayer_to_postgres

__version__ = 20210308.2


def version(version_value=__version__, verbose=True):
    version_dev = 'Alpha'
    if verbose:
        return '{version_dev} version {version_number}'.format(version_dev=version_dev, version_number=version_value)
    else:
        return version_value

####
#
# TOOLS
#
###


def upgrade_geometry(geometry, geometry_type_filter=None):
    """
    Transform a given geometry to a GeometryCollection, all inside geometries are transformed to MULTI geometries.
    Optionally you can add a geometry_type_filter (if you'r geometry input is an GeometryCollection) in this case only
    filtred geometry type will be return
    """
    if isinstance(geometry, dict):
        if geometry['type'].upper() == 'GEOMETRYCOLLECTION':
            geometry_list = geometry['geometries']
        else:
            geometry_list = [geometry]

    if geometry_type_filter:
        if isinstance(geometry_type_filter, str):
            geometry_type_filter = {geometry_type_filter.upper()}
        elif isinstance(geometry_type_filter, (list, tuple, set)):
            geometry_type_filter = set(geometry_type_filter)
        else:
            print('geometry_type_filter must be a geometry type or a list of geometry type')
    else:
        geometry_type_filter = {'POINT', 'LINESTRING', 'POLYGON', 'MULTIPOINT', 'MULTILINESTRING', 'MULTIPOLYGON', 'GEOMETRY', 'GEOMETRYCOLLECTION'}

    result_geometry_list = []
    for geometry in geometry_list:
        if geometry['type'].upper() in geometry_type_filter:
            result_geometry = dict(geometry)
            if not 'MULTI' in result_geometry['type'].upper():
                result_geometry['coordinates'] = [result_geometry['coordinates']]
                result_geometry['type'] = 'Multi' + result_geometry['type']
            result_geometry_list.append(result_geometry)

    return {'type': 'GeometryCollection', 'geometries': result_geometry_list}


def merge_geometries(geom_a, geom_b, bbox=True):
    """
    geom_a
    geom_b
    bbox = True (default) + 5 % time


    Return a merging geometry result of adding two differents geometries
    !! Carfull this function does not "union" two geometry but merge two geometry !!

    Merging Table :

        Single AND Single
            Point + Point = MultiPoint
            LineString + LineString = MultiLineString
            Polygon + Polygon = MultiPolygon

        Single AND Multi
            Point + MultiPoint = MultiPoint
            LineString  + MultiLineString = MultiLineString
            Polygon + MultiPolygon = MultiPolygon

        Mixed Geometries Types and GeometryCollection
            Point + Polygon = GeometryCollection(Point, Polygon)
            GeometryCollection(Polygon + LineString) + LineSting = GeometryCollection(Polygon + MultiLineString)
            GeometryCollection(MultiPolygon, LineString), GeometryCollection(MultiPoint, LineString)
                = GeometryCollection(MultiPolygon, MultiLineString, MultiPoint)



    How does it works ?

        - first if geometry categories are the same

        - if geometry categories are differents or GeometryCollection
            We will have a GeometryCollection

    """
    new_geom = {}

    # if same geometry category (Point, MultiPoint), (LineString, MultiLineString), (Polygon, MultiPolygon)
    if geom_a['type'].replace('Multi', '') == geom_b['type'].replace('Multi', '') and geom_a[
        'type'] != 'GeometryCollection' and geom_b['type'] != 'GeometryCollection':
        new_geom['type'] = str(geom_a['type'])
        new_geom['coordinates'] = list(geom_a['coordinates'])

        if 'Multi' in new_geom['type']:
            if 'Multi' in geom_b['type']:
                for geom_coordinates in geom_b['coordinates']:
                    new_geom['coordinates'].append(geom_coordinates)
            else:
                new_geom['coordinates'].append(geom_b['coordinates'])

        else:
            new_geom['type'] = 'Multi' + new_geom['type']
            if 'Multi' in geom_b['type']:
                geom = [new_geom['coordinates']]
                for geom_coordinates in geom_b['coordinates']:
                    geom.append(geom_coordinates)
                new_geom['coordinates'] = geom
            else:
                new_geom['coordinates'] = [new_geom['coordinates'], geom_b['coordinates']]
    else:
        # new_geom['type'] = 'GeometryCollection'
        if geom_a['type'] == 'GeometryCollection' and geom_b['type'] == 'GeometryCollection':
            # first loop on geom_a geometries
            for i_a, geojson_geometrie_a in enumerate(geom_a['geometries']):
                if i_a == 0:
                    new_geom = geojson_geometrie_a
                else:

                    new_geom = merge_geometries(new_geom, geojson_geometrie_a, bbox=bbox)

            # add geom_ b geometries
            for geojson_geometrie_b in geom_b['geometries']:
                new_geom = merge_geometries(new_geom, geojson_geometrie_b, bbox=bbox)


        elif geom_a['type'] == 'GeometryCollection' or geom_b['type'] == 'GeometryCollection':
            if geom_a['type'] == 'GeometryCollection':
                ori_geom_collect = dict(geom_a)
                ori_geom_simple = dict(geom_b)
            else:
                ori_geom_collect = dict(geom_b)
                ori_geom_simple = dict(geom_a)

            # first loop on ori_geom_collect geometries
            for i_a, geojson_geometrie_a in enumerate(ori_geom_collect['geometries']):
                if i_a == 0:
                    new_geom = geojson_geometrie_a
                else:
                    new_geom = merge_geometries(new_geom, geojson_geometrie_a, bbox=bbox)

            added_geom = False
            # then we see if ori_geom_simple as similar geom type in ori_geom_collect else we had
            for i_geom, geojson_geom in enumerate(new_geom['geometries']):
                if geojson_geom['type'].replace('Multi', '') == ori_geom_simple['type'].replace('Multi', ''):
                    replace_geom = merge_geometries(geojson_geom, ori_geom_simple)
                    new_geom['geometries'][i_geom] = replace_geom
                    added_geom = True
                    # end loop
                    break

            if not added_geom:
                # if not break we had ori_geom_simple to new_geom GEOMETRYCOLLECTION
                new_geom['geometries'] = new_geom['geometries'] + [dict(ori_geom_simple)]

        else:
            new_geom['type'] = 'GeometryCollection'
            new_geom['geometries'] = [dict(geom_a), dict(geom_b)]

    # recompute bbox
    if bbox:
        if new_geom['type'] == 'GeometryCollection':
            for i_geom, geom in enumerate(new_geom['geometries']):
                geom_bbox = coordinates_to_bbox(geom['coordinates'])
                new_geom['geometries'][i_geom]['bbox'] = geom_bbox
                if i_geom == 0:
                    geom_coll_extent = geom_bbox
                else:
                    geom_coll_extent = bbox_union(geom_coll_extent, geom_bbox)

            new_geom['bbox'] = geom_coll_extent

        else:
            new_geom['bbox'] = coordinates_to_bbox(new_geom['coordinates'])
    else:
        if 'bbox' in new_geom:
            del new_geom['bbox']

        if new_geom['type'] == 'GeometryCollection':

            for i_geom, geom in enumerate(new_geom['geometries']):
                if 'bbox' in geom:
                    del new_geom['geometries'][i_geom]['bbox']

    return new_geom


def point_on_segment_range(segment, step_distance, offset_distance=None):
    """
    Iterator send point coordinates on a segment at a given step distance.
    optional: add an offset distance (perpendicular to line_parameters value)

    :param segment:
    :param step_distance:
    :param offset_distance:
    :return:
    """
    start_point, end_point = segment
    native_step_distance = step_distance
    line_parameter = line_parameters((start_point, end_point))
    # test because direction of the linestring can be different from the direction of an affine line
    if euclidean_distance(start_point,
                          point_at_distance_with_line_parameters(end_point, line_parameter, step_distance,
                                                                 offset_distance=offset_distance)) < euclidean_distance(
        start_point, end_point):
        step_distance = -step_distance

    distance = euclidean_distance(start_point, end_point)

    while distance > native_step_distance:
        start_point = point_at_distance_with_line_parameters(start_point, line_parameter, step_distance,
                                                             offset_distance=offset_distance)
        yield start_point
        distance = euclidean_distance(start_point, end_point)


def points_on_linestring_distance(linestring, step_distance, offset_distance=None):
    """
    Return a point geometry that is a point on a given linestring at a given step_distance
    optional: add an offset distance (perpendicular to line_parameters value)

    :param linestring: LineString or MultiLineString geometrie
    :param step_distance: distance between each steps
    :param offset_distance: if you want you can add an offset to final on point value
    :return: Point geometrie
    """

    def points_on_linestring_part(coordinates, step_distance, offset_distance=None):

        # note about remaining_distance
        # remaining_distance is the distance that remain after a new vertex (because when there is a new vertex we have
        # to recompute the step_distance remaining

        # loop on each coordinate
        for i_point, point in enumerate(coordinates):
            if i_point == 0:
                previous_point = point
                # init remaining distance
                remaining_distance = 0
            else:
                remaining_step_distance = step_distance - remaining_distance
                segment = (previous_point, point)

                # yield first point
                if i_point == 1:
                    if offset_distance:
                        line_parameter = line_parameters(segment)
                        perp_parameter = perpendicular_line_parameters_at_point(line_parameter, previous_point)
                        first_point = point_at_distance_with_line_parameters(previous_point, perp_parameter,
                                                                             distance=offset_distance)
                        yield {'type': 'Point', 'coordinates': list(first_point)}
                    else:
                        yield {'type': 'Point', 'coordinates': list(previous_point)}

                # for just one iteration
                for new_point in point_on_segment_range(segment, remaining_step_distance, offset_distance=None):
                    remaining_distance = 0
                    # reinit values
                    previous_point = new_point
                    segment = (previous_point, point)
                    # here we cannot use offset_distance directly in point_on_segment_range used above because we have
                    # to keep initial segment direction. Then we recompute offset new_point.
                    if offset_distance:
                        line_parameter = line_parameters(segment)
                        perp_parameter = perpendicular_line_parameters_at_point(line_parameter, new_point)
                        new_point = point_at_distance_with_line_parameters(new_point, perp_parameter,
                                                                           distance=offset_distance)
                    yield {'type': 'Point', 'coordinates': list(new_point)}
                    break  # just one iteration

                # pass_on_loop check if we iterate on loop below
                pass_on_loop = False
                for new_point in point_on_segment_range(segment, step_distance, offset_distance=None):
                    remaining_distance = euclidean_distance(new_point, point)
                    pass_on_loop = True
                    # here we cannot use offset_distance directly in point_on_segment_range used above because we have
                    # to calculate the remain distance on non offseted point before. Then we recompute offset new_point
                    if offset_distance:
                        line_parameter = line_parameters(segment)
                        perp_parameter = perpendicular_line_parameters_at_point(line_parameter, new_point)
                        new_point = point_at_distance_with_line_parameters(new_point, perp_parameter,
                                                                           distance=offset_distance)
                    yield {'type': 'Point', 'coordinates': list(new_point)}

                # if no iteration en loop above we recalculate remaining distance for next point on coordinates
                if not pass_on_loop:
                    remaining_distance += euclidean_distance(point, previous_point)

                previous_point = point

    # force coordinates to MULTI
    coordinates = linestring['coordinates']
    if 'MULTI' not in linestring['type'].upper():
        coordinates = [coordinates]

    for linestring_part in coordinates:
        for point in points_on_linestring_part(linestring_part, step_distance, offset_distance=offset_distance):
            yield point


def reproject_geometry(geometry, in_crs, out_crs, bbox_extent=True):
    """
    Reproject a geometry with an input coordinate reference system to an output coordinate system

    * GDAL/OSR dependencie :
        AssignSpatialReference()
        ImportFromEPSG()
        SpatialReference()
        TransformTo()
    *

    :param geometry: input geometry
    :param in_crs: input coordinate reference system
    :param out_crs: output coordinate system
    :return: output geometry
    """
    ogr_geometry = geometry_to_ogr_geometry(geometry)

    # Assign spatial ref
    ## Input
    if isinstance(in_crs, int):
        in_proj = osr.SpatialReference()
        in_proj.ImportFromEPSG(in_crs)
    elif isinstance(in_crs, str):
        in_proj = osr.SpatialReference(in_crs)
    else:
        print('crs value must be a ESPG code or a  OGC WKT projection')

    ## Output
    if isinstance(out_crs, int):
        out_proj = osr.SpatialReference()
        out_proj.ImportFromEPSG(out_crs)
    elif isinstance(out_crs, str):
        out_proj = osr.SpatialReference(out_crs)
    else:
        print('crs value must be a ESPG code or a  OGC WKT projection')

    ogr_geometry.AssignSpatialReference(in_proj)
    ogr_geometry.TransformTo(out_proj)

    geometry = ogr_geometry_to_geometry(ogr_geometry)
    if bbox_extent:
        geometry['bbox'] = coordinates_to_bbox(geometry['coordinates'])

    return geometry


def reproject_geolayer(geolayer, out_crs, in_crs=None, bbox_extent=True):

    if not in_crs:
        in_crs = geolayer['metadata']['geometry_ref']['crs']

    # change metadata
    geolayer['metadata']['geometry_ref']['crs'] = out_crs

    if bbox_extent:
        geolayer['metadata']['geometry_ref']['extent'] = None

    # reproject geometry
    for i_feat in geolayer['features']:
        feature = geolayer['features'][i_feat]

        # if geometry in feature
        if 'geometry' in feature.keys():
            feature_geometry = feature['geometry']
            new_geometry = reproject_geometry(feature_geometry, in_crs, out_crs, bbox_extent)
            if geolayer['metadata']['geometry_ref']['extent'] is None:
                geolayer['metadata']['geometry_ref']['extent'] = new_geometry['bbox']
            else:
                bbox_extent = geolayer['metadata']['geometry_ref']['extent']
                geolayer['metadata']['geometry_ref']['extent'] = bbox_union(bbox_extent, new_geometry['bbox'])

            # assign new geometry
            feature['geometry'] = new_geometry

    if bbox_extent:
        geolayer['metadata']['geometry_ref']['extent'] = bbox_extent

    return geolayer


def union_by_split(geometry_list, split_factor=2):
    """
    Union geometry list with split list method (split_factor default 2 by 2)
    * OGR dependencie : Union *
    """

    len_list = len(geometry_list)
    if len_list > split_factor:
        union_geom_list = []
        for i in range(split_factor):
            # first iteration
            if i == 0:
                split_geometry_list = geometry_list[:int(len_list / split_factor)]
            # last iteration
            elif i == split_factor - 1:
                begin = int(len_list / split_factor) * i
                split_geometry_list = geometry_list[begin:]
            # others iterations
            else:
                begin = int(len_list / split_factor) * i
                end = (int(len_list / split_factor)) * (i + 1)
                split_geometry_list = geometry_list[begin:end]

            # adding union to geom list
            union_geom_list.append(union_by_split(split_geometry_list, split_factor))

        for i, union_geom in enumerate(union_geom_list):
            if i == 0:
                ogr_geom_unioned = geometry_to_ogr_geometry(union_geom)
            else:
                temp_geom = geometry_to_ogr_geometry(union_geom)
                ogr_geom_unioned = ogr_geom_unioned.Union(temp_geom)

        geojson_unioned = ogr_geometry_to_geometry(ogr_geom_unioned)

        return geojson_unioned

    else:
        if len(geometry_list) > 1:

            for i, union_geom in enumerate(geometry_list):
                if i == 0:
                    ogr_geom_unioned = geometry_to_ogr_geometry(union_geom)
                else:
                    temp_geom = geometry_to_ogr_geometry(union_geom)
                    ogr_geom_unioned = ogr_geom_unioned.Union(temp_geom)

            geojson_unioned = ogr_geometry_to_geometry(ogr_geom_unioned)

            return geojson_unioned

        else:
            return geometry_list[0]


def create_pk(geolayer, pk_field_name):
    """
    'create_pk' est un dictionnaire qui permet de faire le lien entre les itérateurs features et la valeur d'un champ.

    :param geolayer: la layer au géoformat
    :param pk_field_name: le nom du champs à "indexer"
    :return: géolayer avec une contrainte de pk avce la clé du champs rajouté
    """
    # création du dictionnaire vide
    pk_dico = {}

    # récupération de la value du champs à indexer
    for i_feat in geolayer['features']:
        feature = geolayer['features'][i_feat]

        # if feature is serialized
        if 'feature_serialize' in geolayer['metadata']:
            if geolayer['metadata']['feature_serialize']:
                feature = eval(feature)

        pk_field_value = feature['attributes'][pk_field_name]
        # vérification que les valeurs sont uniques
        if pk_field_value in pk_dico:
            sys.exit('le champ indiqué contient des valeurs non unique')
        else:
            # récupération de la valeur de l'itérateur
            pk_dico[pk_field_value] = i_feat

    # affectation du dictionnaire dans les métadonnées de la géolayer
    # geolayer['metadata']['constraints'] = {'pk': {}}
    # geolayer['metadata']['constraints']['pk'][pk_field_name] = pk_dico

    return pk_dico


def create_attribute_index(geolayer, field_name):
    index_dict = {'type': 'hashtable', 'index': {}}

    # récupération de la valeur du champs à indexer
    for i_feat in geolayer['features']:
        feature = geolayer['features'][i_feat]

        # if feature is serialized
        if 'feature_serialize' in geolayer['metadata']:
            if geolayer['metadata']['feature_serialize']:
                feature = eval(feature)

        field_value = feature['attributes'][field_name]

        try:
            index_dict['index'][field_value].append(i_feat)
        except KeyError:
            index_dict['index'][field_value] = [i_feat]

    return index_dict


def pairwise(iterable):
    """
    from https://stackoverflow.com/questions/5764782/iterate-through-pairs-of-items-in-a-python-list?lq=1
    iterable = [s0, s1, s2, s3, ...]
    return ((s0,s1), (s1,s2), (s2, s3), ...)

    """
    import itertools

    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def len_coordinates(coordinates):
    """
    Return number of coordinates on a coordinates list
    """

    coordinates_count = 0
    for point in coordinates_to_point(coordinates):
        coordinates_count += 1

    return coordinates_count


def len_coordinates_in_geometry(geometry):
    """
    Return number of coordinates on a given geometry
    """
    geometry_collection = geometry_to_geometry_collection(geometry)
    coordinates_count = 0
    for geometry in geometry_collection['geometries']:
        coordinates_count += len_coordinates(geometry['coordinates'])

    return coordinates_count


def get_geocontainer_extent(geocontainer):
    if 'metadata' in geocontainer.keys():
        if 'extent' in geocontainer['metadata']:
            return geocontainer['metadata']['extent']
    else:
        for i_layer, geolayer in enumerate(geocontainer['layers']):
            geolayer_bbox = None
            if 'geometry_ref' in geolayer['metadata']:
                if 'extent' in geolayer['metadata']['geometry_ref']:
                    geolayer_bbox = geolayer['metadata']['geometry_ref']['extent']
            else:
                # no geometry in geolayer
                return None

            if not geolayer_bbox:
                for i_feat in geolayer['features']:
                    feature_bbox = None
                    if 'geometry' in geolayer['features'][i_feat].keys():
                        if 'bbox' in geolayer['features'][i_feat]['geometry']:
                            feature_bbox = geolayer['features'][i_feat]['geometry']['bbox']

                        else:
                            feature_bbox = coordinates_to_bbox(geolayer['features'][i_feat]['geometry'])
                    else:
                        # no geometry in geolayer
                        return None

                    if i_feat == 0:
                        geolayer_bbox = feature_bbox
                    else:
                        geolayer_bbox = bbox_union(geolayer_bbox, feature_bbox)

            if i_layer == 0:
                geocontainer_extent = geolayer_bbox
            else:
                geocontainer_extent = bbox_union(geocontainer_extent, geolayer_bbox)

    return geocontainer_extent


def coordinates_to_centroid(coordinates, precision=None):
    """
    Return the centroid of given coordinates list or tuple

    :param coordinates: (list or tuple) coordinates list or tuple
    :param precision: (int) precision of coordinates (number of decimal places)
    :return: (tuple) centroid
    """

    for i_point, point in enumerate(coordinates_to_point(coordinates)):
        if i_point == 0:
            mean_point = list(point)
        else:
            mean_point[0] += point[0]
            mean_point[1] += point[1]

    nb_coordinates = i_point + 1
    centroid = (mean_point[0] / nb_coordinates, mean_point[1] / nb_coordinates)
    if precision:
        centroid = (round(centroid[0], precision), round(centroid[1], precision))

    return centroid


########################################################################################################################
#
# Adjacency matrix
#
########################################################################################################################

def i_feat_to_adjacency_neighbor(i_feat, adjacency_matrix, neighbor_set=None):
    """
    Use adjacency matrix to find all i_feat neighbor's
    """

    if not neighbor_set:
        neighbor_set = set([i_feat])

    # set store i_feat neighbor's
    i_feat_neighbor_set = set(adjacency_matrix[i_feat])
    # difference result between the list of neighbors already scanned and i_feat neighbors
    # Anyway, it's the list of new neighbors we haven't scanned yet.
    new_neighbor_set = set(i_feat_neighbor_set.difference(neighbor_set))
    # copy previous set
    new_neighbor_set_copy = set(new_neighbor_set)

    i = 0
    while new_neighbor_set_copy:
        # Loop scan every new neighbor
        for neighbor in new_neighbor_set:
            # set store i_feat neighbor's
            i_feat_neighbor_set = set(adjacency_matrix[neighbor])
            # new set of neighbors who have never been scanned before
            new_new_neighbor_set = i_feat_neighbor_set.difference(neighbor_set)
            # add the neighbor to the result list
            neighbor_set.update({neighbor})
            # we add the new neighbors never scanned before
            new_neighbor_set_copy.update(new_new_neighbor_set)

            # we delete the scanned neighbor
            new_neighbor_set_copy = new_neighbor_set_copy.difference({neighbor})

            i += 1
        # adding to new_neighbor_set ew neighbors that have never been scanned before
        new_neighbor_set = set(new_neighbor_set_copy)

    return list(neighbor_set)


def create_adjacency_matrix(geolayer, mesh_size=None):
    """
    Creating an adjacency matrix

    * GDAL/OGR dependencie :
        Intersects
    *
    """

    matrix_dict = {}

    try:
        input_grid_idx = geolayer['metadata']['constraints']['index']['geometry']
    except:
        input_grid_idx = create_grid_index(geolayer, mesh_size=mesh_size)

    mesh_size = input_grid_idx['metadata']['mesh_size']

    # Création de la clé unique du dictionnaire de résultat (préparation du stockage des résultats)
    matrix_dict['matrix'] = {i_feat: [] for i_feat in geolayer['features']}

    for i_feat in geolayer['features']:
        feature_a = geolayer['features'][i_feat]

        # if feature is serialized
        if 'feature_serialize' in geolayer['metadata']:
            if geolayer['metadata']['feature_serialize']:
                feature_a = eval(feature_a)

        # get bbox
        try:
            feature_a_bbox = feature_a['geometry']['bbox']
        except KeyError:
            feature_a_bbox = coordinates_to_bbox(feature_a['geometry']['coordinates'])
            feature_a['geometry']['bbox'] = feature_a_bbox

        # Récupération des identifiants de mailles présent dans l'index
        g_id_list = list(bbox_to_g_id(feature_a_bbox, mesh_size))

        # Pour chaque identifiant de maille de l'index on récupère l'identifant des autres polygones voisins de l'entité
        # en cours (s'ils existent)
        neighbour_i_feat_list = []
        for g_id in g_id_list:
            # récupération de la liste des clefs primaires des entités présentes dans la maille de l'index
            neighbour_i_feat_list += input_grid_idx['index'][g_id]

        # suppression de la clef primaire du polyone en cours et d'éventuels doublons
        neighbour_i_feat_list = [value for value in list(set(neighbour_i_feat_list)) if value != i_feat]

        # création  de la géométrie du feature A
        feature_a_ogr_geom = geometry_to_ogr_geometry(feature_a['geometry'])
        # Même procédé que précédemment pour l'objet B
        for neighbour_i_feat in neighbour_i_feat_list:
            # si le i_feat n'est pas déjà compris dans la matrice de proximité du voisin :
            #  si c'est le cas alors cela veut dire que l'on a déjà fait un test d'intersection enrte les deux
            #  géométries auparavant (car pour avoir un voisin il faut etre deux)

            if i_feat not in matrix_dict['matrix'][neighbour_i_feat]:
                feature_b = geolayer['features'][neighbour_i_feat]

                # if feature is serialized
                if 'feature_serialize' in geolayer['metadata']:
                    if geolayer['metadata']['feature_serialize']:
                        feature_b = eval(feature_b)

                feature_b_ogr_geom = geometry_to_ogr_geometry(feature_b['geometry'])

                if feature_a_ogr_geom.Intersects(feature_b_ogr_geom):
                    matrix_dict['matrix'][i_feat].append(neighbour_i_feat)
                    matrix_dict['matrix'][neighbour_i_feat].append(i_feat)

    matrix_dict['metadata'] = {'type': 'adjacency'}

    return matrix_dict

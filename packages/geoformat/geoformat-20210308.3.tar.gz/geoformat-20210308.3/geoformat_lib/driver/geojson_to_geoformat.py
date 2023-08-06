import glob
import json
import os
import sys
import geojson

from geoformat_lib.conversion.feature_conversion import feature_list_to_geolayer, features_filter
from geoformat_lib.conversion.geometry_conversion import geometry_to_bbox, bbox_union
from geoformat_lib.conf.format_variable import value_to_iterable_value
from geoformat_lib.conf.geometry_variable import GEOFORMAT_GEOMETRY_TYPE


def load_data(path):

    # verify that path exist
    if os.path.isfile(path):
        # get file name
        basename = os.path.basename(path)
        basename_split = basename.split(".geojson")
        if basename_split[-1] == "":
            name = ".geojson".join(basename_split[:-1])
        else:
            name = basename

        # open file
        with open(path, 'r') as geojson_file:
            json_object = json.loads(geojson_file.read())

    else:
        raise Exception('path is not a file')

    return json_object, name


def geometry_to_feature(geometry, attributes=None):

    feature = {"geometry": geometry}
    if attributes:
        feature["attributes"] = attributes

    return feature


def attributes_to_feature(attributes, geometry=None):
    feature = {"attributes": attributes}
    if geometry:
        feature["geometry"] = geometry

    return geometry


def json_object_to_feature_generator(
        json_object,
):
    # if it's a Feature Collection
    if json_object["type"] == "FeatureCollection":
        for i_feat, json_feature in enumerate(json_object["features"]):
            for feature in json_object_to_feature_generator(json_feature):
                if feature:
                    yield feature

    # if it's a Feature
    elif json_object["type"] == "Feature":
        feature = {}
        if "properties" in json_object:
            feature["attributes"] = dict(json_object["properties"])

        if "geometry" in json_object:
            feature["geometry"] = dict(json_object["geometry"])

        if feature:
            yield feature

    # if it's a geometry
    elif json_object["type"].upper() in GEOFORMAT_GEOMETRY_TYPE:
        feature = {"geometry": dict(json_object)}

        if feature:
            yield feature
    else:
        raise Exception("no geojson compatible data")


def geojson_object_to_feature(geojson_object, bbox_extent=True):

    if isinstance(geojson_object, geojson.feature.FeatureCollection):

        for i_feat, geojson_feature in enumerate(geojson_object["features"]):
            for feature in geojson_object_to_feature(
                geojson_feature, bbox_extent=bbox_extent
            ):
                yield feature

    elif isinstance(geojson_object, geojson.feature.Feature):
        feature = {}
        if "properties" in geojson_object:
            for i_field, field_name in enumerate(geojson_object["properties"]):
                if i_field == 0:
                    feature["attributes"] = {}

                feature["attributes"][field_name] = geojson_object["properties"][
                    field_name
                ]

        if "geometry" in geojson_object:
            feature["geometry"] = dict(geojson_object["geometry"])
            if bbox_extent:
                feature["geometry"]["bbox"] = geometry_to_bbox(
                    geojson_object["geometry"]
                )

        yield feature
    # else if it's a geometry object
    else:
        feature = {"geometry": dict(geojson_object)}
        if bbox_extent:
            feature["geometry"]["bbox"] = geometry_to_bbox(
                feature["geometry"]
            )
        yield feature


def geojson_to_geocontainer(
    path,
    field_name_filter=None,
    bbox_extent=True,
    bbox_filter=None,
    feature_serialize=False,
    feature_limit=None,
    feature_offset=None,
):
    """

    """

    ## verify if path is a file or directory path
    if isinstance(path, (list, tuple, set)):
        geojson_path_list = path
    elif os.path.isdir(path):
        # test relative path
        dirname = os.path.dirname(__file__)
        path = os.path.join(dirname, path)
        # recuperate all geojson file in directory
        geojson_path_list = glob.glob(path + "*.geojson")
    elif os.path.isfile(path):
        geojson_path_list = [path]
    else:
        sys.exit("error: your path must be a dir/file path or a list of path")

    # init geocontainer
    geocontainer = {"layers": {}, "metadata": {}}
    # is usefull to determine if there is a geometric geolayer in geocontainer (to compute bbox_extent)

    # init GEOMETRIC option
    geometry_first = True
    geocontainer_extent = False
    geometry_in_geocontainer = False
    geometry_in_geolayer = False
    for path in geojson_path_list:
        # recuperate geolayer
        geolayer = geojson_to_geolayer(
            path,
            field_name_filter=field_name_filter,
            bbox_extent=bbox_extent,
            bbox_filter=bbox_filter,
            feature_serialize=feature_serialize,
        )
        geolayer_name = geolayer["metadata"]["name"]
        # GEOMETRY TEST
        # test if geometry is present in geolayer
        if "geometry_ref" in geolayer["metadata"]:
            geometry_in_geolayer = True
            geometry_in_geocontainer = True

            # if bbox_extent and geometry is present in geolayer
            if bbox_extent and geometry_first and geometry_in_geolayer:
                geocontainer_extent = geolayer["metadata"]["geometry_ref"]["extent"]
                geometry_first = False
            # if bbox_extent and not first
            if bbox_extent and not geometry_first and geometry_in_geolayer:
                geocontainer_extent = bbox_union(
                    geocontainer_extent, geolayer["metadata"]["geometry_ref"]["extent"]
                )

        geocontainer["layers"][geolayer_name] = geolayer

        # reinit geometry_in_geolayer
        geometry_in_geolayer = False

    if bbox_extent and geometry_in_geocontainer:
        geocontainer["metadata"]["extent"] = geocontainer_extent

    # if geolayer in geocontaire
    if len(geocontainer["layers"]) > 0:
        return geocontainer


def from_geojson_get_features_list(
        geojson_in_dict,
        field_name_filter,
        geometry_type_filter,
        bbox_filter,
        serialize,
        bbox_extent,
        feature_limit,
        feature_offset
):

    # create feature generator from file
    features_generator = json_object_to_feature_generator(
        json_object=geojson_in_dict
    )

    # get features list
    features_list = [
        feature for feature in features_filter(
            geolayer_feature_list_or_generator=features_generator,
            field_name_filter=field_name_filter,
            geometry_type_filter=geometry_type_filter,
            bbox_filter=bbox_filter,
            serialize=serialize,
            bbox_extent=bbox_extent,
            feature_limit=feature_limit,
            feature_offset=feature_offset,
        )
    ]

    return features_list


def geojson_to_geolayer(
    path,
    field_name_filter=None,
    geometry_type_filter=None,
    bbox_extent=True,
    bbox_filter=None,
    serialize=False,
    feature_limit=None,
    feature_offset=None,
):
    """
        Convert geojson file to geolayer

    :param path: path to geojson file
    :param field_name_filter: field_name that we want to keep in geolayer (can be a list).
    :param geometry_type_filter: keep only features with geometry type in this variable (can be a list).
    :param bbox_extent: add "bbox" key in each features and "extent" key in geometry metadata.
    :param bbox_filter: keep only feature that intersects bbox (can be a list of bbox).
    :param serialize: True if features in geolayer are serialized (can reduce performance) / False if not.
    :param feature_limit: constrains the number of rows returned in output geolayer.
    :param feature_offset: skip feature before beginning to given line number.
    :return geolayer: geolayer
    """
    # init and prepare variable
    field_name_filter = value_to_iterable_value(field_name_filter, output_iterable_type=list)
    geometry_type_filter = value_to_iterable_value(geometry_type_filter, output_iterable_type=set)
    bbox_filter = value_to_iterable_value(bbox_filter, output_iterable_type=tuple)

    # load data and get name
    data_geojson_in_dict, name = load_data(path)

    if data_geojson_in_dict:
        # filter features
        features_list = from_geojson_get_features_list(
            geojson_in_dict=data_geojson_in_dict,
            field_name_filter=field_name_filter,
            geometry_type_filter=geometry_type_filter,
            bbox_filter=bbox_filter,
            serialize=None,
            bbox_extent=False,
            feature_limit=feature_limit,
            feature_offset=feature_offset
        )

        # create geolayer from filter feature list
        geolayer = feature_list_to_geolayer(
            feature_list=features_list,
            geolayer_name=name,
            field_name_filter=None,
            force_field_conversion=False,
            geometry_type_filter=None,
            bbox_filter=None,
            bbox_extent=bbox_extent,
            crs=None,
            serialize=serialize,
        )

        return geolayer

# Welcome to Geoformat

## Introduction

Geoformat is GDAL / OGR  overlayer wiht MIT licence.
The library aim is to simplify loading and OGR 'DataSource' and 'Layer' manipulations.
Until now this library is in Alpha mode. This means that for the moment the structure of this library is not
full oriented object compatible.

## Installation


```sh
$ pip install geoformat
```

## Feature structure

The feature is de basic object that contains information.
This information is of two types: 
- attributes : alphanumeric data that describes feature
- geometry : type and coordinates that describe geometrically the feature

### attributes


### geometry

There are seven types of geometries that we can group into 3 categories.


#### basics

| type         | representation                                                                                                     | sample data         | geoformat                                                                                                                                                                                                                      |
|--------------|--------------------------------------------------------------------------------------------------------------------|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| *Point*      | ![Point](https://framagit.org/Guilhain/Geoformat/raw/geometry_translator/images/51px-SFA_Point.svg.png)            | underground station | <pre lang="python">{<br>  "type": "Point",<br>  "coordinates": [-115.81, 37.24],<br>  'bbox': (-115.81, 37.24, -115.81, 37.24)<br>}</pre>                                                                                                                            |
| *LineString* | ![LineString](https://framagit.org/Guilhain/Geoformat/raw/geometry_translator/images/51px-SFA_LineString.svg.png)  | a road              | <pre lang="python">{<br>  "type": "LineString",<br>  "coordinates": [[8.919, 44.4074], [8.923, 44.4075]],<br>  'bbox': (8.919, 44.4074, 8.923, 44.4075)<br>}</pre>                                                                                                    | 
| *Polygon*    | ![Polygon](https://framagit.org/Guilhain/Geoformat/raw/geometry_translator/images/SFA_Polygon_with_hole.svg.png)   | an island           | <pre lang="python">{<br>  "type": "Polygon",<br>  "coordinates": [[[2.38, 57.322], [23.194, -20.28], [-120.43, 19.15], [2.38, 57.322]], [[-5.21, 23.51], [15.21, -10.81], [-20.51, 1.51], [-5.21, 23.51]]],<br>  'bbox': (-120.43, -20.28, 23.194, 57.322)<br>}</pre> |


#### composed

| type              | representation                                                                                            | sample data                         | geoformat                                                                                                                                                                                                                                    |
|-------------------|-----------------------------------------------------------------------------------------------------------|-------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| *MultiPoint*      | ![MultiPoint](https://framagit.org/Guilhain/Geoformat/raw/geometry_translator/images/51px-SFA_MultiPoint.svg.png)           | exits from same underground station | <pre lang="python">{<br>  "type": "MultiPoint",<br>  "coordinates": [<br>    [-155.52, 19.61],<br>    [-156.22, 20.74],<br>    [-157.97, 21.46]<br>  ],<br>  "bbox": (-157.97, 19.61, -155.52, 21.46)<br>}</pre>                                                                                  |
| *MultiLineString* | ![MultiLineString](https://framagit.org/Guilhain/Geoformat/raw/geometry_translator/images/51px-SFA_MultiLineString.svg.png) | a river with several tributaries    | <pre lang="python">{<br>  "type": "MultiLineString",<br>  "coordinates": [<br>    [[3.75, 9.25], [-130.95, 1.52]],<br>    [[23.15, -34.25], [-1.35, -4.65], [3.45, 77.95]]<br>  ],<br>  "bbox": (-130.95, -34.25, 23.15, 77.95)<br>}</pre>                                                  |
| *MultiPolygon*    | ![MultiPolygon](https://framagit.org/Guilhain/Geoformat/raw/geometry_translator/images/SFA_MultiPolygon_with_hole.svg.png)  | a country with an island            | <pre lang="python">{<br>  "type": "MultiPolygon",<br>  "coordinates": [<br>    [[[3.78, 9.28], [-130.91, 1.52], [35.12, 72.234], [3.78, 9.28]]],<br>    [[[23.18, -34.29], [-1.31, -4.61], [3.41, 77.91], [23.18, -34.29]]]<br>  ],<br>  "bbox": (-130.91, -34.29, 35.12, 77.91)<br>}</pre> |

#### sets

| type                 | representation                                                                                                                    | sample data                 | geoformat                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|----------------------|-----------------------------------------------------------------------------------------------------------------------------------|-----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| *GeometryCollection* | ![GeometryCollection](https://framagit.org/Guilhain/Geoformat/raw/geometry_translator/images/51px-SFA_GeometryCollection.svg.png) | a mix of all examples above |  <pre lang="python">{<br>  "type": 'GeometryCollection',<br>  "geometries": [<br>    {<br>      "type": "Point",<br>      "coordinates": [-115.81, 37.24],<br>      'bbox': (-115.81, 37.24, -115.81, 37.24)<br>    },<br>    {<br>      "type": "LineString",<br>      "coordinates": [[8.919, 44.4074], [8.923, 44.4075]],<br>      'bbox': (8.919, 44.4074, 8.923, 44.4075)<br>    },<br>    {<br>      "type": "Polygon",<br>      "coordinates": [[[2.38, 57.322], [23.194, -20.28], [-120.43, 19.15], [2.38, 57.322]], [[-5.21, 23.51], [15.21, -10.81], [-20.51, 1.51], [-5.21, 23.51]]],<br>      'bbox': (-120.43, -20.28, 23.194, 57.322)<br>    }, <br>    {<br>      'type': 'MultiPoint',<br>      'coordinates': [[-155.52, 19.61], [-156.22, 20.74], [-157.97, 21.46]],<br>      'bbox': (-157.97, 19.61, -155.52, 21.46)<br>    },<br>    {<br>      "type": 'MultiLineString',<br>      "coordinates": [[[3.75, 9.25], [-130.95, 1.52]], [[23.15, -34.25], [-1.35, -4.65], [3.45, 77.95]]],<br>      'bbox': (-130.95, -34.25, 23.15, 77.95)<br>    },<br>    {<br>      'type': 'MultiPolygon', <br>      'coordinates': [[[[3.78, 9.28], [-130.91, 1.52], [35.12, 72.234], [3.78, 9.28]]], [[[23.18, -34.29], [-1.31, -4.61], [3.41, 77.91], [23.18, -34.29]]]],<br>      'bbox': (-130.91, -34.29, 35.12, 77.91)<br>    }<br>  ],<br>  'bbox': (-157.97, -34.29, 35.12, 77.95)<br>}</pre> |


## Geolayer structure

![Strucutre of Geoformat](https://framagit.org/Guilhain/Geoformat/raw/geometry_translator/images/geoformat.png)

## Geolayer metadata

'metadata' key in geolayer root structure is used to inform the structure of the geolayer.

If geolayer contains attribute data "fields" key must be filled in.
If geolayer contains geometries data "geometry_ref" key must be filled in.


### Field type

Each field in geolayer must be filed in "metadata" => "fields" structure.

Is informed : 
    - field name
        - field type : you have to give code of field type (see table below)
        - field width 
        - field precision
        - field index
        
 
| Code | Name           |
|------|----------------|
| 0    | Integer        |
| 1    | Boolean        |
| 2    | Real           |
| 3    | RealList       |
| 4    | String         |
| 5    | StringList     |
| 6    | WideString     |
| 7    | WideStringList |
| 8    | Binary         |
| 9    | Date           |
| 10   | DateList       |
| 11   | DateTime       |
| 12   | Integer64      |
| 13   | Integer64List  |

### Geometry type

Each geometrie in geolayer must be filed in "metadata" => "geometry_ref" structure.

Is informed 
    - type : each geometries type code present in geolayer (see table below)
    - crs :  coordinate reference systeme in WKT format or EPSG

| Code | Name               |
|------|--------------------|
| 0    | Unknown            |
| 1    | Point              |
| 2    | LineString         |
| 3    | Polygon            |
| 4    | MultiPoint         |
| 5    | MultiLinestring    |
| 6    | MultiPolygon       |
| 7    | GeometryCollection |
| 100  | None               |


## Examples 

### Open a geocontainer

A container is an equivalent to folder or a database containing one or several geolayer.

```py
import geoformat

commune_path = 'data/FRANCE_IGN/COMMUNE_2016_MPO_L93.shp'
gare_path = 'data/FRANCE_IGN/GARES_PT_L93.shp'

layer_list = [commune_path, gare_path]

geocontainer = geoformat.ogr_layers_to_geocontainer(layer_list)

print(geocontainer['layers'].keys())

# >>>dict_keys(['COMMUNE_2016_MPO_L93', 'GARES_PT_L93'])
```

### Open a geolayer

A geolayer is an equivalent to a file or a table in database containing one or several features with attibutes and/or
geometry.

```py
import geoformat

departement_path = 'data/FRANCE_IGN/DEPARTEMENT_2016_L93.shp'

geolayer = geoformat.ogr_layer_to_geolayer(departement_path)

print(len(geolayer['features']))

# >>>96
```


### Print data geolayer

Sometime it can be uselful to print in terminal geolayer's attributes.

```py
import geoformat

region_path = 'data/FRANCE_IGN/REGION_2016_L93.shp'

geolayer = geoformat.ogr_layer_to_geolayer(region_path)

print(geoformat.print_features_data_table(geolayer)):

    
### >>>
+--------+----------+-------------------------------------+------------+------------+
| i_feat | CODE_REG | NOM_REG                             | POPULATION | SUPERFICIE |
+========+==========+=====================================+============+============+
| 0      | 76       | LANGUEDOC-ROUSSILLON-MIDI-PYRENEES  | 5683878    | 7243041    |
| 1      | 75       | AQUITAINE-LIMOUSIN-POITOU-CHARENTES | 5844177    | 8466821    |
| 2      | 84       | AUVERGNE-RHONE-ALPES                | 7757595    | 7014795    |
| 3      | 32       | NORD-PAS-DE-CALAIS-PICARDIE         | 5987883    | 3187435    |
| 4      | 44       | ALSACE-CHAMPAGNE-ARDENNE-LORRAINE   | 5552388    | 5732928    |
| 5      | 93       | PROVENCE-ALPES-COTE D'AZUR          | 4953675    | 3155736    |
| 6      | 27       | BOURGOGNE-FRANCHE-COMTE             | 2819783    | 4746283    |
| 7      | 52       | PAYS DE LA LOIRE                    | 3660852    | 2997777    |
| 8      | 28       | NORMANDIE                           | 3328364    | 2728511    |
| 9      | 11       | ILE-DE-FRANCE                       | 11959807   | 1205191    |
| 10     | 24       | CENTRE-VAL DE LOIRE                 | 2570548    | 3905914    |
| 11     | 53       | BRETAGNE                            | 3258707    | 2702269    |
| 12     | 94       | CORSE                               | 320208     | 875982     |
+--------+----------+-------------------------------------+------------+------------+

```

### Change geolayer coordinate reference system [CRS]

It can be usefull to change the projection for a layer.  In this example we will transform a geolayer in projection Lambert93 [EPSG:2154] to coordinates system WGS84 [EPSG:4326].

```py
import geoformat

region_path = 'data/FRANCE_IGN/REGION_2016_L93.shp'

geolayer = geoformat.ogr_layer_to_geolayer(region_path)

geolayer = geoformat.reproject_geolayer(geolayer, out_crs=4326)

print(geolayer['metadata']['geometry_ref']['crs'])

# >>>4326

```


### Write geolayer in a OGR compatible GIS file

You can obviously convert a geolayer in a compatible OGR file format.
In this case ye put a geolayer in 'ESRi SHAPEFILE' format and we create a new file in 'GEOJSON' (we add a reprojection because geojson should be in WGS84 coordinates system).

```py
import geoformat

gares_shp_path = 'data/FRANCE_IGN/GARES_L93.shp'
gares_geojson_path =  'data/FRANCE_IGN/GARES_L93.geojson'

geolayer = geoformat.ogr_layer_to_geolayer(gares_shp_path)

geolayer = geoformat.reproject_geolayer(geolayer, out_crs=4326)

geoformat.geolayer_to_ogr_layer(geolayer, gares_geojson_path, 'GEOJSON')

```

### Write a container in OGR compatible dataSource

Like geolayer you can write a geoformat container in a folder or a GRG compatible datasource.
Here we have a geocontainer with a lot of layers and we want to save all of this in an other folder (but it can be also a 'POSTGRESQL' database).

```py
import geoformat

# INPUT
commune_path = 'data/FRANCE_IGN/COMMUNE_2016_MPO_L93.shp'
gare_path = 'data/FRANCE_IGN/GARES_PT_L93.shp'

# OUTPUT
output_folder = 'data/'

layer_list = [commune_path, gare_path]

geocontainer = geoformat.ogr_layers_to_geocontainer(layer_list)

geoformat.geocontainer_to_ogr_format(geocontainer, output_folder, 'kml')

```



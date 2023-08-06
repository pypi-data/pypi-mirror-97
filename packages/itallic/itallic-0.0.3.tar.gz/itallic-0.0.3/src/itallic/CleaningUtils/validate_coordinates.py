import os
import re
import pyproj
import geopandas as gpd
import pandas as pd
import geopy as gp
import math
import numpy as np
import folium
import sys
from dateutil import parser
from datetime import date
from geopy.exc import GeocoderTimedOut
from sridentify import Sridentify
from shapely.geometry import Point, Polygon, MultiPolygon
from shapely.ops import transform
import country_converter as coco
from itertools import product
from functools import partial
pd.options.mode.chained_assignment = None

def process_shapefile(shapefile=None):
    """
    Take in a shapefile directory and parse the filepath to each file in the directory.

    :param shapefile: filepath to shapefile directory.
    :type shapefile: str
    :return: dictionary with the file extension as keys and the complete filepath as values.
    :rtype: dict of {str: str}

    >>> process_shapefile('/home/example_user/example_shapefile_directory')
    {'dbf': '/home/example_user/example_shapefile_directory/example_shapefile.dbf',
     'prj': '/home/example_user/example_shapefile_directory/example_shapefile.prj',
     'shp': '/home/example_user/example_shapefile_directory/example_shapefile.shp',
     'shx': '/home/example_user/example_shapefile_directory/example_shapefile.shx'}
    """
    dirpath = os.path.abspath(os.path.dirname(__file__))
    if not shapefile:
        shapefile = str(os.path.abspath(os.path.join(dirpath, '..', '..', 'resources', 'mapinfo')))
    file_dict = dict()
    for directory, _, files in os.walk(shapefile):
        for file in files:
            file_path = os.path.abspath(os.path.join(directory, file))
            file_dict[file_path[-3:]] = file_path
    return file_dict

def get_shape(shp_file):
    """
    Generate a GeoDataFrame from .shp file.

    :param shp_file: filepath to the .shp file.
    :type shp_file: str.
    :return:
    :rtype: geopandas.GeoDataFrame
    """
    return gpd.read_file(shp_file)

def get_projection(prj_file):
    """
    Determine the EPSG code from .prj file.

    :param prj_file: filepath to the .prj file.
    :type prj_file: str.
    :return:
    :rtype: int.

    >>> get_projection('/home/example_user/example_shapefile_directory/example_shapefile.prj')
    4326
    """
    srider = Sridentify()
    srider.from_file(prj_file)
    return srider.get_epsg()

def read_file(file_path):
    """
    Generate a dataframe from .xlsx or .csv file.

    :param file_path:
    :type file_path: str.
    :return:
    :rtype: DataFrame.
    :raise TypeError: if the file extension is not .csv or .xlsx.
    """
    if file_path.endswith('.xlsx'):
        data = pd.read_excel(file_path)
    elif file_path.endswith('.csv'):
        data = pd.read_csv(file_path)
    else:
        raise TypeError('Support is only available for .xlsx and .csv files.')
    return data

def check_columns(df, cols):
    """
    Check to see whether the column names are present in the dataframe.

    :param df:
    :type df: DataFrame or geopandas.GeoDataFrame.
    :param cols:
    :type cols: list of str or set of str.
    :return:
    :rtype: bool.
    :raise KeyError: if any of the column names cannot be found in the dataframe.

    >>> import pandas as pd
    >>> df = pd.DataFrame({'Location': ['Beijing', 'Sao Paulo', 'Amsterdam'],
    ...                    'Country': ['China', 'Brazil', 'Netherlands']})
    >>> df
        Location      Country
    0    Beijing        China
    1  Sao Paulo       Brazil
    2  Amsterdam  Netherlands
    >>> check_columns(df=df, cols=['Country', 'Location'])
    True

    .. note::
        Function will always return True or raise an error.
    """
    if isinstance(cols, str):
        cols = {cols}
    elif not isinstance(cols, set):
        cols = set(cols)
    if cols.issubset(df.columns):
        return True
    else:
        raise KeyError('Column names not found in data frame.')

def read_data(data, cols):
    """
    Generate a dataframe and verify that the specified columns are in the dataframe.

    :param data: filepath (.csv or .xlsx extension) or dataframe.
    :type data: str, DataFrame, geopandas.GeoDataFrame
    :param cols:
    :type cols: list of str or set of str.
    :rtype: DataFrame if the type of `data` is DataFrame or str, or geopandas.GeoDataFrame if it is geopandas.GeoDataFrame.
    :raises TypeError: if a different type is passed for `data` or the file extension is not .csv or .xlsx.

    >>> import pandas as pd
    >>> df = pd.DataFrame({'City': ['Delhi', 'Giza'], 'Country': ['India', 'Egypt'],
    ...                    'Latitude': [28.68, 30.01], 'Longitude': [77.22, 31.13]})
    >>> read_data(data=df, cols={'Country', 'Latitude', 'Longitude'})
        City Country  Latitude  Longitude
    0  Delhi   India     28.68      77.22
    1   Giza   Egypt     30.01      31.13
    """
    if isinstance(data, str):
        df = read_file(data)
    elif isinstance(data, pd.DataFrame) or isinstance(data, gpd.GeoDataFrame):
        df = data.copy(deep=True)
    else:
        raise TypeError('Cannot read data type.')
    if check_columns(df, cols):
        return df

def filter_data_without_coords(data, lat_col, lng_col):
    """
    Generate two dataframes to filter out entries where no latitudinal and longitudinal data was entered.

    :param data: filepath (.csv or .xlsx extension) or dataframe.
    :type data: str, DataFrame, geopandas.GeoDataFrame.
    :param lat_col: name of the latitude column.
    :type lat_col: str.
    :param lng_col: name of the longitude column.
    :type lng_col: str.
    :return: two dataframes, one with all of the entries with coordinates and one of those without.
    :rtype: tuple of (DataFrame, DataFrame) if the type of `data` is DataFrame or str,
            tuple of (geopandas.GeoDataFrame, geopandas.GeoDataFrame) if it is geopandas.GeoDataFrame.

    .. note::
        Entries whose latitude and longitude are both 0 are considered as having no inputs.

    >>> import pandas as pd
    >>> df = pd.DataFrame({'City': ['Addis Ababa', 'Manila', 'Dubai'],
    ...                    'Country': ['Ethiopia', 'Philippines', 'United Arab Emirates'],
    ...                    'Latitude': [8.98, 14.35, 0], 'Longitude': [38.76, 21.00, 0]})
    >>> filter_data_without_coords(data=df, lat_col='Latitude', lng_col='Longitude')
    (         City      Country  Latitude  Longitude
    0  Addis Ababa     Ethiopia      8.98      38.76
    1       Manila  Philippines     14.35      21.00,
        City               Country  Latitude  Longitude
    2  Dubai  United Arab Emirates       0.0        0.0)
    """
    data = read_data(data, {lat_col, lng_col})

    with_coords = data.index[(data[lat_col] != 0) & (data[lng_col] != 0) &
                             pd.notnull(data[lat_col]) & pd.notnull(data[lng_col])].tolist()
    with_coords_df = data.loc[with_coords]
    without_coords_df = data[~data.index.isin(with_coords)]

    return with_coords_df, without_coords_df

def add_country_code(data, ctry_col):
    """
    Append two new columns to the data containing each entry's country's country codes.

    :param data: filepath (.csv or .xlsx extension) or dataframe.
    :type data: str, DataFrame, geopandas.GeoDataFrame.
    :param ctry_col: name of the country column.
    :type ctry_col: str.
    :return: the modified dataframe with the new columns 'ISO2' and 'ISO3' for two-letter and three-letter country
             codes respectively.
    :rtype: DataFrame if the type of `data` is DataFrame or str, or geopandas.GeoDataFrame if it is geopandas.GeoDataFrame.

    >>> import pandas as pd
    >>> df = pd.DataFrame({'City': ['Rabat', 'Lyon', 'Cleveland'],
    ...                    'Country': ['Morocco', 'France', 'United States of America']})
    >>> add_country_code(df=data, ctry_col='Country')
            City                   Country ISO2 ISO3
    0      Rabat                   Morocco   MA  MAR
    1       Lyon                    France   FR  FRA
    2  Cleveland  United States of America   US  USA
    """
    df = read_data(data, {ctry_col})

    #df['ISO2'] = coco.convert(names=list(df[ctry_col]), to='ISO2')
    #df['ISO3'] = coco.convert(names=list(df[ctry_col]), to='ISO3')
    ctry_col_list = df.loc[:, ctry_col].unique().tolist()
    iso2_list = coco.convert(names=ctry_col_list, to='ISO2')
    iso3_list = coco.convert(names=ctry_col_list, to='ISO3')
    zipped_isos = zip(ctry_col_list, iso2_list, iso3_list)
    iso_df = pd.DataFrame(zipped_isos, columns=[ctry_col, 'ISO2', 'ISO3'])
    df = df.join(iso_df.set_index(ctry_col), on=ctry_col)
    
    return df

def flip_coords(data, lat_col, lng_col, prj=4326):
    """
    Generate 8 geopandas.GeoDataFrames, each with two columns comprising one latitude-longitude combination among
    [(lat, lng), (lat, -lng), (-lat, lng), (-lat, -lng),
     (lng, lat), (lng, -lat), (-lng, lat), (-lng, -lat)].

    :param data: filepath (.csv or .xlsx extension) or dataframe.
    :type data: str, DataFrame, geopandas.GeoDataFrame.
    :param lat_col: name of the latitude column.
    :type lat_col: str.
    :param lng_col: name of the longitude column.
    :type lng_col: str.
    :param prj: EPSG code for spatial projection.
    :type prj: int.
    :return:
    :rtype: list of geopandas.GeoDataFrame.

    >>> import pandas as pd
    >>> df = pd.DataFrame({'City': ['Addis Ababa', 'Manila', 'Vienna', 'Mexico City', 'Puebla'],
    ...                    'Country': ['Ethiopia', 'Philippines', 'Austria', 'Mexico', 'Mexico'],
    ...                    'Latitude': [8.98, 14.35, 0, 19.25, None], 'Longitude': [38.76, 21.00, 0, -99.10, None]})
    >>> dfs = flip_coords(data=df, lat_col='Latitude', lng_col='Latitude', prj=4326)
    >>> dfs[1]
              City      Country  Latitude  Longitude  Flipped_Lat  Flipped_Lng             geometry
    0  Addis Ababa  Ethiopia         8.98      38.76         8.98       -38.76  POINT (-38.76 8.98)
    1  Manila       Philippines     14.35      21.00        14.35       -21.00    POINT (-21 14.35)
    2  Vienna       Austria         0.00        0.00         0.00        -0.00         POINT (-0 0)
    3  Mexico City  Mexico          19.25     -99.10        19.25        99.10  POINT (99.10 19.25)
    4  Puebla       Mexico            NaN        NaN         0.00         0.00          POINT (0 0)

    .. note::
        Point geometry is formatted as (lng, lat).

        Null latitude and longitude are converted to 0s.
    """
    def create_comb(nums):
        return list(product(*((x, -x) for x in nums)))

    df = read_data(data, {lat_col, lng_col})

    temp_lat_lng = list(df.apply(lambda row: create_comb([row[lat_col], row[lng_col]]), axis=1))
    temp_lng_lat = list(df.apply(lambda row: create_comb([row[lng_col], row[lat_col]]), axis=1))
    temp_coords = [temp_lat_lng[i] + temp_lng_lat[i] for i in range(len(temp_lat_lng))]

    all_gdfs = list()
    for i in range(8):
        ndf = pd.DataFrame.copy(df)
        ndf['Flipped_Lat'] = [loc[i][0] for loc in temp_coords]
        ndf['Flipped_Lng'] = [loc[i][1] for loc in temp_coords]
        if i > 0:
            ndf['Flipped_Type'] = 'Flipped'
        else:
            ndf['Flipped_Type'] = 'Original'
        gdf = to_gdf(ndf, 'Flipped_Lat', 'Flipped_Lng', prj)
        all_gdfs.append(gdf)

    return all_gdfs

def cross_check(data, first_col, second_col):
    """
    Filter all of the entries in `data` whose values for ``first_col`` and ``second_col`` are equal and return
    matching and non-matching entries.

    :param data: filepath (.csv or .xlsx extension) or dataframe.
    :type data: str or DataFrame.
    :param first_col: column name.
    :type first_col: str.
    :param second_col: column name.
    :type second_col: str.
    :return: all qualified entries in a DataFrame and all non-qualifying entries in another
    :rtype: tuple of (DataFrame, DataFrame)

    >>> import pandas as pd
    >>> df = pd.DataFrame({'Country': ['Australia', 'Indonesia', 'Denmark'], 'Entered_ISO2': ['AUS', 'ID', 'DK'],
    ...                    'Matched_ISO2': ['AU', 'ID', 'DK']})
    >>> results = cross_check(data=df, first_col='Entered_ISO2', second_col='Matched_ISO2')
    >>> results[0]
         Country Entered_ISO2 Matched_ISO2
    1  Indonesia           ID           ID
    2    Denmark           DK           DK
    >>> results[1]
         Country Entered_ISO2 Matched_ISO2
    0  Australia          AUS           AU
    """
    df = read_data(data, {first_col, second_col})
    matching_cols_df = df[df[first_col] == df[second_col]]
    return matching_cols_df, df.drop(matching_cols_df.index, errors = 'ingore')
    #indices = [index for index, row in df.iterrows() if row[first_col] == row[second_col]]
    #return df.loc[indices], df.drop(indices, errors='ignore')

def to_gdf(data, lat_col, lng_col, prj=4326):
    """
    Generate a geopandas.GeoDataFrame.

    :param data: filepath (.csv or .xlsx extension) or dataframe.
    :type data: str or DataFrame.
    :param lat_col: name of the latitude column.
    :type lat_col: str.
    :param lng_col: name of the longitude column.
    :type lng_col: str.
    :param prj: EPSG code for spatial projection.
    :type prj: int.
    :return:
    :rtype: geopandas.GeoDataFrame.
    """
    df = read_data(data, {lat_col, lng_col})
    df.fillna({lat_col: 0, lng_col: 0}, inplace=True)
    geometry = [Point(coords) for coords in zip(df[lng_col], df[lat_col])]
    crs = {'init': 'epsg:' + str(prj)}

    return gpd.GeoDataFrame(df, crs=crs, geometry=geometry)

def export_df(df, extension, filename, directory):
    """
    Export the dataframe to a file.

    :param df:
    :type df: DataFrame or geopandas.GeoDataFrame.
    :param extension: outfile extension (.csv or .xlsx).
    :type extension: str.
    :param filename: outfile name (without extension).
    :type filename: str.
    :param directory: outfile directory.
    :type directory: str.
    :return: absolute filepath to outfile.
    :rtype: str.
    :raise TypeError: if file extension is not csv or  xlsx.
    """
    extension = extension.lower().replace('.', '')
    file_path = os.path.join(directory, '.'.join((filename, extension)))
    if extension.endswith('csv'):
        df.to_csv(file_path, index=False)
    elif extension.endswith('xlsx'):
        df.to_excel(file_path, index=False)
    else:
        raise TypeError('Unsupported file type.')
    return file_path

def rtree(geodata, polygon):
    """
    Use geopandas's R-tree implementation to find all of the locations in `geodata` in the spatial polygon.

    :param geodata: dataframe of locations with spatial geometries.
    :type geodata: geopandas.GeoDataFrame.
    :param polygon:
    :type polygon: shapely.geometry.Polygon.
    :return: all of the entries with locations in the polygon.
    :rtype: geopandas.GeoDataFrame.
    """
    if not isinstance(geodata, gpd.GeoDataFrame):
        raise TypeError('Data must be a geopandas GeoDataFrame.')

    sindex = geodata.sindex
    if isinstance(polygon, Polygon):
        polygon = MultiPolygon([polygon])

    matches = []
    try:
        matches_index = list(sindex.intersection(polygon.bounds))
        matches = geodata.iloc[matches_index]     # geodataframe
    except Exception as e:
        print(e)

    return matches

def check_country_geom(geodata, geo_iso2_col, shapedata, shape_geom_col, shape_iso2_col, eval_col):
    """
    Filter all of the entries in `geodata` whose coordinates are within their indicated country by
    iterating through a shapefile of country polygons and finding locations that are in each polygon.

    Entries that got matched to a country that is different from their indicated country and entries that
    did not match to any country (i.e. they are in the ocean) are also returned as a DataFrame with
    the column `Coordinate_Error` specifying which error category the entries fall into.

    :param geodata: dataframe of locations with spatial geometries.
    :type geodata: geopandas.GeoDataFrame.
    :param geo_iso2_col: name of the two-letter country code column in dataframe.
    :type geo_iso2_col: str.
    :param shapedata: shapefile dataframe.
    :type shapedata: geopandas.GeoDataFrame.
    :param shape_geom_col: name of the geometry column in the shapefile dataframe.
    :type shape_geom_col: str.
    :param shape_iso2_col: name of the two-letter country code column in the shapefile dataframe.
    :type shape_iso2_col: str.
    :param eval_col: name of the column to use in conjunction with `geo_iso2_col` to distinguish between entries.
    :type eval_col: str.
    :return: all of the entries that were verified as having their location in the respective indicated country and
             all of the entries that did not belong to any country/matched the wrong country in dataframes.
    :rtype: tuple of (geopandas.GeoDataFrame, geopandas.GeoDataFrame)
    """
    shapedata = read_data(shapedata, {shape_geom_col, shape_iso2_col})
    geodata = read_data(geodata, {geo_iso2_col})

    matched_df = pd.DataFrame(columns=list(geodata.columns))
    wrong_match_df = pd.DataFrame(columns=list(geodata.columns))

    for index, row in shapedata.iterrows():
        # Getting all of the data points that are in the polygon
        stations_within = rtree(geodata, row[shape_geom_col])
        if len(stations_within) > 0:
            # Checking to see which actually corresponds to the country as indicated
            stations_within['Matched_Country_ISO2'] = row[shape_iso2_col]
            cc_check = cross_check(stations_within, geo_iso2_col, 'Matched_Country_ISO2')
            # Retrieving the correct points
            correct_stations_within = cc_check[0]
            correct_stations_within = correct_stations_within.drop(['Matched_Country_ISO2'], axis=1)
            matched_df = matched_df.append(correct_stations_within, sort=True, ignore_index=True)
            # Retrieving the incorrect ones
            incorrect_stations_within = cc_check[1]
            incorrect_stations_within['Coordinate_Error'] = 'Mismatched country'
            wrong_match_df = wrong_match_df.append(incorrect_stations_within, sort=True, ignore_index=True)

    # All of the entries that were not matched or wrongly matched
    remaining_data = geodata[~(geodata[eval_col].isin(matched_df[eval_col]) & geodata[geo_iso2_col].isin(matched_df[geo_iso2_col]))]

    # All entries that were wrongly matched
    mismatched_df = wrong_match_df[~(wrong_match_df[eval_col].isin(matched_df[eval_col]) & wrong_match_df[geo_iso2_col].isin(matched_df[geo_iso2_col]))]
    mismatched_df = mismatched_df.drop_duplicates(subset=[eval_col, geo_iso2_col])
    # All entries that did not have any match (right or wrong)
    no_match_df = remaining_data[~(remaining_data[eval_col].isin(wrong_match_df[eval_col]) & remaining_data[geo_iso2_col].isin(wrong_match_df[geo_iso2_col]))]
    no_match_df['Coordinate_Error'] = 'No country matched'
    # Merging all of those entries into a single dataframe
    remaining_data = mismatched_df.append(no_match_df, sort=True, ignore_index=True).sort_values(by=[geo_iso2_col, eval_col]).reset_index(drop=True)

    return matched_df, remaining_data

def check_data_geom(eval_col, iso2_col, all_geodata, shapedata, shape_geom_col, shape_iso2_col):
    """
    Take in a collection of spatial dataframes that are variations of a single dataframe and check to see
    which geometry actually fall within the borders of its preset country. If an entry is verified as correct
    with its original inputs, the other variations will not be appended

    Generate two dataframes, one that combines all of the entries in the collection that are marked as verified,
    and one for entries whose respective geometry does not correspond to the preset country for any variation.

    :param eval_col: name of the column to distinguish between entries (should be a column in all of the dataframes).
    :type eval_col: str.
    :param iso2_col: name of the two-letter country code column.
    :type iso2_col: str.
    :param all_geodata: collection of spatial dataframes.
    :type all_geodata: geopandas.GeoDataFrame or list or set of geopandas.GeoDataFrame
    :param shapedata: shapefile dataframe.
    :type shapedata: geopandas.GeoDataFrame.
    :param shape_geom_col: name of the geometry column in the shapefile dataframe.
    :type shape_geom_col: str.
    :param shape_iso2_col: name of the two-letter country code column in the shapefile dataframe.
    :type shape_iso2_col: str.
    :return: two dataframes, one with verified entries, and one with invalid entries.
    :rtype: tuple of (geopandas.GeoDataFrame, geopandas.GeoDataFrame).

    .. note::
        The function assumes that the first dataframe in the collection is the original dataframe.

        The verified dataframe might contain multiple entries for the same initial entry if two or more of its
        variations match its preset country.

        :func:`~experiment.GeocodeValidator.flip_coords` should be called first to generate the dataframe collection
        to optimize this function.
    """

    if not isinstance(all_geodata, list):
        all_geodata = [all_geodata]
    # Retrieving the original dataframe
    orig_input_df = all_geodata[0]

    # Appending all of the modified dataframes into a single dataframe for efficiency
    if len(all_geodata) > 1:
        alt_input_df = gpd.GeoDataFrame(columns=orig_input_df.columns)
        alt_input_df = alt_input_df.append(all_geodata[1:], sort=False, ignore_index=True)
        eval_dfs = [orig_input_df, alt_input_df]
    else:
        eval_dfs = [orig_input_df]

    matched_dfs = []

    for i in range(len(eval_dfs)):
        df = read_data(eval_dfs[i], {eval_col, iso2_col})
        # Filtering out entries that were verified as correct with their original lat/lng inputs
        if i > 0:
            df = df[~(df[eval_col].isin(matched_dfs[0][eval_col]) & (df[iso2_col].isin(matched_dfs[0][iso2_col])))]

        # Running the checking function
        results = check_country_geom(df, iso2_col, shapedata, shape_geom_col, shape_iso2_col, eval_col)
        matched_dfs.append(results[0])

        # Getting the dataframe with the suggested errors for the original lat/lng inputs
        if i == 0:
            error_df = results[1]

    # Appending all of the entries (modified or not) to a single dataframe
    matched_data = gpd.GeoDataFrame(columns=orig_input_df.columns)
    if len(matched_dfs) > 0:
        matched_data = pd.concat(matched_dfs).sort_values(by=[iso2_col, eval_col]).reset_index(drop=True)
        matched_data = matched_data.reindex(columns=orig_input_df.columns)

    # Retrieving all of the entries that were flagged as incorrect with their suggested error
    remaining_data = orig_input_df[~(orig_input_df[eval_col].isin(matched_data[eval_col]) & orig_input_df[iso2_col].isin(matched_data[iso2_col]))].sort_values(by=[iso2_col, eval_col]).reset_index(drop=True)
    remaining_data = error_df[error_df[eval_col].isin(remaining_data[eval_col]) & error_df[iso2_col].isin(remaining_data[iso2_col])]

    return matched_data, remaining_data

def folium_inspect(map, lat, lng, country, addr, l_type="Original"):
    desc = addr + "," + country + "(" + l_type + ")"
    folium.Marker([lat, lng], popup=desc, icon=folium.Icon(color="gray")).add_to(map)

def folium_plot(map, lat, lng, country, addr, l_type):
    col = 'gray'
    if l_type == 'Original':
        col='green'
    elif l_type == 'Flipped':
        col = 'darkred'
    elif l_type == 'Geocoded':
        col = 'lightred'
    else:
        col = 'black'

    desc = addr + ","+ country + "(" + l_type + ")"
    folium.Marker([lat, lng], popup=desc,icon=folium.Icon(color=col)).add_to(map)

def get_location_coordinates(loc_name,country_name):
    lat = 'Not Found'
    lng = 'Not Found'
    addr = 'Not Found'
    g_type = 'Not Found'
    pht = gp.Photon(timeout=3)
    iso2 = coco.convert(country_name, to='ISO2')  # using ISO2 country codes to avoid country spelling errors
    try:
        matches = pht.geocode(loc_name + ', ' + country_name, exactly_one=False)
        if matches:
            for match in matches:
                match_country = match.address.split(',')[-1]
                match_iso2 = coco.convert(match_country, to='ISO2')
                # Comparing the country codes of the entered country and the returned country
                if match_iso2 == iso2:
                    lat=match.latitude
                    lng=match.longitude
                    addr=match.address
                    g_type='Geocoded'
                    return addr, lat, lng, g_type
    except GeocoderTimedOut:
        pass
    return addr, lat, lng, g_type

def get_coordinates_dictionary(df, loc_col, ctry_col):
    loc = {}
    for index, row in df.iterrows():
        addr, lat, lng, g_type = get_location_coordinates(row[loc_col], row[ctry_col])
        loc[row[loc_col] + row[ctry_col]] = (addr, lat, lng, g_type)
    return loc

def get_coordinates(loc_name,country_name,loc_dict):
    res = loc_dict[loc_name + country_name]
    return res[0], res[1], res[2], res[3]

def geocode_coordinates(data, loc_col, ctry_col):
    df = read_data(data, {ctry_col})
    gdf = pd.DataFrame(columns=df.columns)

    df[loc_col].fillna('', inplace=True)
    df[ctry_col].fillna('', inplace=True)

    # Because sometimes we receive data frames with duplicate entries,
    # we are going to create one with just unique entries. This will ensure
    # we do not request multiple API calls for the same location. We will store
    # this values in a dictionary and just look them up.
    no_duplicates =  df[[loc_col, ctry_col]]
    no_duplicates = no_duplicates.drop_duplicates()

    # Return a dictionary containing geocoded locations
    cood_dict = get_coordinates_dictionary(no_duplicates,loc_col, ctry_col)

    # Geo code using the function get_coordinates. This function looks up information
    # in the dictionary instead of making an API call
    #result = pd.DataFrame(df.apply(lambda x: get_coordinates(x.loc_col, x.ctry_col), axis=1, result_type="expand"))
    result = pd.DataFrame(df[[loc_col,ctry_col]].apply(lambda x: get_coordinates(*x,cood_dict), axis=1, result_type="expand"))
    result.columns = ['Geocoded_Adr', 'Geocoded_Lat', 'Geocoded_Lng', 'GeoCode_Type']
    result = pd.concat([df, result], axis=1)

    # Rows without null on the column Geocoded_Lat were geocoded
    # geocoded = result[result.Geocoded_Lat.notnull()]

    # Rows without Not Found on the column Geocoded_Lat were geocoded
    # geocoded[geocoded.Geocoded_Lat == 'Not Found']
    geocoded = result[result.Geocoded_Lat != 'Not Found' ]

    # Rows with null on the column Geocoded_Lat were NOT geocoded
    # not_geocoded_temp = result[result.Geocoded_Lat.isnull()]
    not_geocoded_temp = result[result.Geocoded_Lat == 'Not Found' ]
    not_geocoded = not_geocoded_temp[[loc_col, ctry_col]]

    # Get the original columns since the others have NULL in them
    # idf = df[~df[loc_col].isin(gdf[loc_col])]
    return geocoded, not_geocoded


def cell_in_data(data, val, col, abs_tol=0.1):
    """
    Find the entries whose values in the passed column match the queried value.

    If querying a numeric value, the function will return all entries whose corresponding cells approximate
    the passed value with the specified absolute tolerance.

    If querying a string, the function will return all entries whose corresponding cells contain the passed value,
    case insensitive.

    :param data: filepath (.csv or .xlsx extension) or dataframe.
    :type data: str or DataFrame.
    :param val: queried value.
    :type val: str, int, or float.
    :param col: name of queried column.
    :type col: str.
    :param abs_tol:
    :type abs_tol: float.
    :return: all entries meeting the condition.

    >>> import pandas as pd
    >>> df = pd.DataFrame({'City': ['Birmingham', 'Brussels', 'Berlin'], 'Country': ['England', 'Belgium', 'Germany'],
    ...                    'Latitude': [52.48, 50.85, 52.52], 'Longitude': [-1.89, 4.35, 13.40]})
    >>> cell_in_data(data=df, val='brussels', col='City')
           City  Country  Latitude  Longitude
    1  Brussels  Belgium     50.85       4.35
    >>> cell_in_data(data=df, val=52.5, col='Latitude')
             City  Country  Latitude  Longitude
    0  Birmingham  England     52.48      -1.89
    2      Berlin  Germany     52.52      13.40
    """
    df = read_data(data, {col})

    res_df = pd.DataFrame()

    if pd.notnull(val):
        # Searching for numeric values
        if isinstance(val, float) or isinstance(val, int):
            val = float(val)
            res_df = df[(df[col] - val).abs() < abs_tol]
        # Searching for string values
        elif isinstance(val, str):
            res_df = df[df[col].str.contains(val, flags=re.IGNORECASE, regex=True)]

    return res_df


def query_data(data, query_dict, excl=False):
    """
    Find all entries that meet the conditions specified in the query dictionary.

    If ``excl=True``, the function only returns entries meeting every single criteria. Else, it returns any entry
    that meets at least one of the conditions.

    :param data: filepath (.csv or .xlsx extension) or dataframe.
    :type data: str or DataFrame.
    :param query_dict: dictionary whose keys are column names mapping to the queried value(s).
    :type query_dict: dict of {str: list, str: set, or str: str}.
    :param excl: exclusive or inclusive search.
    :type excl: bool.
    :return: all entries meeting the condition(s).

    >>> import pandas as pd
    >>> df = pd.DataFrame({'City': ['Birmingham', 'Brussels', 'Berlin'], 'Country': ['England', 'Belgium', 'Germany'],
    ...                    'Latitude': [52.48, 50.85, 52.52], 'Longitude': [-1.89, 4.35, 13.40]})
    >>> query_data(data=df, query_dict={'Latitude': [52.5, 40], 'City': 'Berlin'}, excl=False)
             City  Country  Latitude  Longitude
    0  Birmingham  England     52.48      -1.89
    2      Berlin  Germany     52.52      13.40
    >>> query_data(data=df, query_dict={'Latitude': 52.5, 'City': 'berlin'}, excl=True)
         City  Country  Latitude  Longitude
    2  Berlin  Germany     52.52       13.4
    """
    df = read_data(data, query_dict.keys())
    res_df = pd.DataFrame()

    for col, val in query_dict.items():
        if isinstance(val, list) or isinstance(val, set):
            for item in val:
                res_df = res_df.append(cell_in_data(df, item, col), sort=False)
        else:
            res_df = res_df.append(cell_in_data(df, val, col), sort=False)

    if len(res_df) > 0:
        eval_cols = list(res_df.columns)
        if ("geometry" in eval_cols) or ("geom" in eval_cols):
            eval_cols.remove("geometry")
        if excl:
            return res_df[res_df.duplicated(subset=eval_cols)]
        else:
            return res_df.drop_duplicates(subset=eval_cols)
    return res_df


def convert_df_crs(df, out_crs=4326):
    """Change projection from input projection to provided crs (defaults to 4326)"""
    def get_formatted_crs(crs):
        """Determine correct crs string based on provided [out_crs] value"""
        try:
           new_crs = pyproj.Proj(crs)
           dcs = new_crs
           ncrs_str = crs
        except AttributeError:
           try:
               float(crs)
               new_crs = 'epsg:{}'.format(crs)
               dcs = pyproj.Proj(init=new_crs)
               ncrs_str = {'init': '{}'.format(new_crs)}
           except TypeError:
               new_crs = crs
               dcs = pyproj.Proj(init=new_crs)
               ncrs_str = {'init': new_crs}
        except RuntimeError:
           new_crs = out_crs
           dcs = pyproj.Proj(new_crs)
           ncrs_str = new_crs

        return dcs, new_crs, ncrs_str

    scs, _,_ = get_formatted_crs(df.crs)
    # get destination coordinate system, new coordinate system and new crs string
    dcs, new_crs, ncrs_str = get_formatted_crs(out_crs)
    project = partial(
       pyproj.transform,
       scs,  # source coordinate system
       dcs)  # destination coordinate system
    new_df = df[[x for x in df.columns if x != 'geometry']]
    new_geom = [transform(project, x) for x in df.geometry.values]
    new_df['geometry'] = new_geom
    new_spat_df = gpd.GeoDataFrame(new_df, crs=ncrs_str, geometry='geometry')
    # return dataframe with converted geometry
    return new_spat_df

def getStateName(state_code):
    states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming',
        'AB': 'Alberta',
        'BC': 'British Columbia',
        'MB': 'Manitoba',
        'NB': 'New Brunswick',
        'NL': 'Newfoundland and Labrador',
        'NT': 'Northwest Territories',
        'NS': 'Nova Scotia',
        'NT': 'Northwest Territories',
        'NU': 'Nunavut',
        'ON': 'Ontario',
        'PE': 'Prince Edward Island',
        'QC': 'Quebec',
        'SK': 'Saskatchewan',
        'YT': 'Yukon'
    }
    assert (len(state_code) == 2), "State code should contain 2 letters."
    return states.get(state_code, "State not found")

def getStateCountry(state_code):
    states = {
        'AK': 'United States',
        'AL': 'United States',
        'AR': 'United States',
        'AS': 'United States',
        'AZ': 'United States',
        'CA': 'United States',
        'CO': 'United States',
        'CT': 'United States',
        'DC': 'United States',
        'DE': 'United States',
        'FL': 'United States',
        'GA': 'United States',
        'GU': 'United States',
        'HI': 'United States',
        'IA': 'United States',
        'ID': 'United States',
        'IL': 'United States',
        'IN': 'United States',
        'KS': 'United States',
        'KY': 'United States',
        'LA': 'United States',
        'MA': 'United States',
        'MD': 'United States',
        'ME': 'United States',
        'MI': 'United States',
        'MN': 'United States',
        'MO': 'United States',
        'MP': 'United States',
        'MS': 'United States',
        'MT': 'United States',
        'NA': 'United States',
        'NC': 'United States',
        'ND': 'United States',
        'NE': 'United States',
        'NH': 'United States',
        'NJ': 'United States',
        'NM': 'United States',
        'NV': 'United States',
        'NY': 'United States',
        'OH': 'United States',
        'OK': 'United States',
        'OR': 'United States',
        'PA': 'United States',
        'PR': 'United States',
        'RI': 'United States',
        'SC': 'United States',
        'SD': 'United States',
        'TN': 'United States',
        'TX': 'United States',
        'UT': 'United States',
        'VA': 'United States',
        'VI': 'United States',
        'VT': 'United States',
        'WA': 'United States',
        'WI': 'United States',
        'WV': 'United States',
        'WY': 'United States',
        'AB': 'Canada',
        'BC': 'Canada',
        'MB': 'Canada',
        'NB': 'Canada',
        'NL': 'Canada',
        'NT': 'Canada',
        'NS': 'Canada',
        'NT': 'Canada',
        'NU': 'Canada',
        'ON': 'Canada',
        'PE': 'Canada',
        'QC': 'Canada',
        'SK': 'Canada',
        'YT': 'Canada'
    }
    assert (len(state_code) == 2), "State code should contain 2 letters."
    return states.get(state_code, "State not found")

def getThreshold(n, scores):
    sorted_scores = np.sort(scores)
    thres = 100
    i=0
    while (i<n and i < len(sorted_scores)):
        thres = sorted_scores[i]
        i = i + 1
    return thres

def convertDateToOrdinal(d1,d2):
    today = date.today()
    if isinstance(d1, float) and math.isnan(d1):
        d1_out = 0
    else:
        d1_out = today.toordinal() - parser.parse(d1).toordinal()

    if isinstance(d2, float) and math.isnan(d2):
        d2_out = 0
    else:
        d2_out = today.toordinal() - parser.parse(d2).toordinal()

    return [d1_out,d2_out]

us_state_abbrev_to_name = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Palau': 'PW',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}





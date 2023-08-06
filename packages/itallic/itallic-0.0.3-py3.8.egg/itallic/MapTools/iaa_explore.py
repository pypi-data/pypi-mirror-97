from folium import Map, Marker, Icon, Popup
from folium.plugins import MarkerCluster
import math
from itallic.CleaningUtils.validate_coordinates import *


class MapTool:
    def __init__(self, shapedir=None, shape_geom='geometry', shape_iso2='ISO2'):
        """
        Initialize a MapTool object to plot locational data points.

        :param shapedir: filepath to shapefile directory.
        :type shapedir: str.
        :param shape_geom: name of the geometry column.
        :type shape_geom: str.
        :param shape_iso2: name of the two-letter country code column.
        :type shape_iso2: str.
        """

        shape_dict = process_shapefile(shapedir)
        self.shape_gdf = get_shape(shape_dict['shp']) # Generate a GeoDataFrame from .shp file.
        # Because the shapefile defined country boundaries, geometry column contains polygon of the countries.
        self.prj = get_projection(shape_dict['prj']) # Determine the EPSG code from .prj file.
        self.shape_geom = shape_geom
        self.shape_iso2 = shape_iso2
        self.colors = [
            'green',
            'purple',
            'blue',
            'orange',
            'gray'
            'pink',
            'beige',
            'lightgreen',
            'lightblue',
            'lightgrayblack',
            'darkpurple',
            'darkblue',
            'darkgreen',
            'cadetblue'
        ]
        self.map = None
    def create_map(self, center=(0, 0), zoom=2):
        """
        Create a basic map.

        :param center:L
        :param zoom:
        :return:
        :rtype: folium.Map.
        """
        self.map = Map(location=center, zoom_start=zoom,tiles='Stamen Terrain')
        return self.map

    def save(self, filename):
        """

        """
        self.map.save(filename)

    def add_to_map(self, map, item):
        if isinstance(item, list):
            for i in item:
                i.add_to(map)
        else:
            item.add_to(map)
        return map

    def format_popup(self, loc, ctry):
        """
        Format the locational description for popup icon.

        :param loc: location or lower level locational information.
        :type loc: str.
        :param ctry: country or higher level locational information.
        :type ctry: str.
        :return:
        :rtype: tuple of (str, str).
        """
        if not loc:
            loc = ''
        if not ctry:
            ctry = ''
        return loc, ctry

    def haversine(self, lat0, lng0, lat1, lng1):
        """
        Calculate the distance between two geographical points using the haversin formula (in kilometers).

        :param lat0:
        :param lng0:
        :param lat1:
        :param lng1:
        :return: the distance in km.
        """
        rlat0 = math.radians(lat0)
        rlat1 = math.radians(lat1)
        dlat = rlat1 - rlat0
        dlng = math.radians(lng1 - lng0)

        a = math.pow(math.sin(dlat / 2), 2) + math.cos(rlat0) * math.cos(rlat1) * math.pow(math.sin(dlng / 2), 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return 6371 * c

    def plot_point(self, lat, lng, desc=None, clr='blue'):
        """
        Create a single popup located at the passed coordinates.

        :param lat:
        :type lat: int or float.
        :param lng:
        :type lng: int or float.
        :param desc: description of the popup.
        :type desc: str.
        :param clr:
        :type clr: str.
        :return:
        :rtype: folium.Marker.
        """
        if not desc:
            desc = str((lat, lng))
        return Marker(location=(lat, lng), popup=Popup(desc, parse_html=True,max_width=600),
                      icon=Icon(prefix='fa', color=clr, icon='circle', icon_color='white'))

    def plot_all_data(self, data, loc_col, ctry_col, lat_col, lng_col, clr='blue', as_cluster=True):
        """
        Create markers for all of the locational data points. Setting as_cluster=True is an
        easy way to declutter your map. You will see a cluster with the points and they will
        only appear after you zoom in enough.

        :param data: filepath (.csv or .xlsx extension) or dataframe.
        :type data: str or DataFrame.
        :param loc_col: name of location column.
        :type loc_col: str.
        :param ctry_col: name of country column.
        :type ctry_col: str.
        :param lat_col: name of latitude column.
        :type lat_col: str.
        :param lng_col: name of longitude column.
        :type lng_col: str.
        :param clr: color of the markers.
        :type clr: str.
        :param as_cluster: indicate whether the markers will be saved in a cluster or not.
        :type as_cluster: bool.
        :return: all of the created markers.
        :rtype: list of folium.Marker if ``as_cluster=False`` or a folium.MarkerCluster if ``as_cluster=True``.
        """
        df = read_data(data, {loc_col, ctry_col, lat_col, lng_col})

        if as_cluster:
            markers = MarkerCluster()
        else:
            markers = []

        for (index, row) in df.iterrows():
            if pd.notnull(row[lat_col]) and pd.notnull(row[lng_col]):
                lat = row[lat_col]
                lng = row[lng_col]
                location = self.format_popup(row[loc_col], row[ctry_col])
                # Annotation information will pop-up when a user clicks on a location
                marker = self.plot_point(lat=lat, lng=lng, desc='%s, %s : (%.2f, %.2f)' % (location[0], location[1], lat, lng), clr=clr)
                if as_cluster:
                    marker.add_to(markers)
                else:
                    markers.append(marker)

        return markers

    def plot_correct_data(self, data, loc_col, ctry_col, lat_col, lng_col, clr='green', as_cluster=False):
        """
        Create markers for all of the data points whose locational information correspond to their respective country.

        :param data:
        :param loc_col:
        :param ctry_col:
        :param lat_col:
        :param lng_col:
        :param clr:
        :param as_cluster:
        :return:
        """
        df = read_data(data, {loc_col, ctry_col, lat_col, lng_col})
        gdf = to_gdf(df, lat_col, lng_col, self.prj)
        gdf['ISO2'] = coco.convert(list(gdf[ctry_col]), to='ISO2')
        correct_df = check_data_geom(loc_col, 'ISO2', gdf, self.shape_gdf, self.shape_geom, self.shape_iso2)[0]
        return self.plot_all_data(correct_df, loc_col, ctry_col, lat_col, lng_col, clr, as_cluster)

    def plot_potential_errors(self, data, loc_col, ctry_col, lat_col, lng_col, clr='lightred', plot_alt=False):
        """
        Create markers for all of the data points whose coordinates either fall in the ocean or do not correspond to
        their respective country.

        These entries can be geocoded and the returned coordinates can be created as separate markers if
        ``plot_alt=True``.

        :param data:
        :param loc_col:
        :param ctry_col:
        :param lat_col:
        :param lng_col:
        :param clr:
        :param plot_alt: indicate whether to geocode and create markers for alternative coordinates.
        :type plot_alt: bool.
        :return:
        """
        # Read a data frame and verify that the specified columns are in the data frame
        df = read_data(data, {loc_col, ctry_col, lat_col, lng_col})
        
        # Convert data frame into a geopandas.GeoDataFrame. A GeoDataFrame object is a
        # pandas.DataFrame that has a column with geometry. In our case this is most likely
        # a POINT object
        gdf = to_gdf(df, lat_col, lng_col, self.prj)

        gdf['ISO2'] = coco.convert(list(gdf[ctry_col]), to='ISO2')
        checked_df = check_data_geom(loc_col, 'ISO2', gdf, self.shape_gdf, self.shape_geom, self.shape_iso2)

        potential_errors = checked_df[1]

        markers = self.plot_all_data(checked_df[1], loc_col, ctry_col, lat_col, lng_col, clr=clr, as_cluster=False)

        if plot_alt:
            alt_df = geocode_coordinates(potential_errors, loc_col, ctry_col)[0]
            alt_markers = self.plot_all_data(alt_df, loc_col, ctry_col, 'Geocoded_Lat', 'Geocoded_Lng',
                                             as_cluster=False, clr='lightgreen')
            markers = markers + alt_markers

        return markers

    def plot_condition(self, data, query_dict, loc_col, ctry_col, lat_col, lng_col, excl=False, clr='blue'):
        """
        Create markers for all data points that meet the conditions as specified in the query dictionary.

        If ``excl=True``, the function only creates markers for points meeting every single criteria. Else, it creates
        markers for any point that meets at least one of the conditions.

        :param data:
        :param query_dict: dictionary whose keys are column names mapping to the queried value(s).
        :type query_dict: dict of {str: list, str: set, or str: str}.
        :param loc_col:
        :param ctry_col:
        :param lat_col:
        :param lng_col:
        :param excl:
        :param excl: exclusive or inclusive plotting.
        :type excl: bool.
        :param clr:
        :return:
        """
        res_df = query_data(data, query_dict, excl)
        return self.plot_all_data(res_df, loc_col, ctry_col, lat_col, lng_col, clr, False)

    def plot_pair_in_df(self, data, index, lat0_col, lng0_col, lat1_col, lng1_col, clr0='lightblue', clr1='darkblue'):
        """
        Create two markers for a data point if it has two locational information.

        :param data:
        :param index: index of the data point in the data.
        :type index: int
        :param lat0_col:
        :param lng0_col:
        :param lat1_col:
        :param lng1_col:
        :param clr0:
        :param clr1:
        :return: two markers for the coordinates.
        :rtype: tuple of (folium.Marker, folium.Marker).
        """
        df = read_data(data, {lat0_col, lng0_col, lat1_col, lng1_col})

        if index < len(df):
            coords0 = (df.loc[index, lat0_col], df.loc[index, lng0_col])
            coords1 = (df.loc[index, lat1_col], df.loc[index, lng1_col])

            return self.plot_pair(coords0, coords1, clr0, clr1)
        else:
            raise KeyError('Index out of range.')

    def plot_pair(self, coords0, coords1, clr0='lightblue', clr1='darkblue'):
        """
        Create markers for two sets of coordinates.

        :param coords0:
        :type coords0: tuple or list of int or float.
        :param coords1:
        :type coords1: tuple or list of int or float.
        :param clr0:
        :param clr1:
        :return:
        """
        marker0 = self.plot_point(lat=coords0[0], lng=coords0[1], desc=str(coords0), clr=clr0)
        marker1 = self.plot_point(lat=coords1[0], lng=coords1[1], desc=str(coords1), clr=clr1)

        return marker0, marker1

    def plot_within_range(self, data, center, radius, loc_col, ctry_col, lat_col, lng_col,
                          desc0=None, clr0='blue', clr1='lightblue'):
        """
        Create markers for all data points within the range of the passed center.

        :param data: filepath (.csv or .xlsx extension) or dataframe.
        :type data: str or DataFrame
        :param center: center of the search circle.
        :type center: tuple or list of int or float.
        :param radius: radius of the search circle (in kilometers).
        :type radius: int or float.
        :param loc_col:
        :param ctry_col:
        :param lat_col:
        :param lng_col:
        :param desc0: description of the marker for the center.
        :param clr0: color of the center.
        :type clr0: str.
        :param clr1: color of the other markers.
        :type clr1: str.
        :return:
        :rtype: list of folium.Marker.
        """
        df = read_data(data, {loc_col, ctry_col, lat_col, lng_col})
        if not desc0:
            desc0 = str(tuple(center))
        markers = []
        for index, row in df.iterrows():
            if pd.notnull(row[lat_col]) and pd.notnull(row[lng_col]):
                lat = row[lat_col]
                lng = row[lng_col]
                d = self.haversine(center[0], center[1], lat, lng)

                if d < radius:
                    location = self.format_popup(row[loc_col], row[ctry_col])
                    markers.append(self.plot_point(lat=lat, lng=lng, clr=clr1,
                                                   desc='%s, %s - %s km' % (
                                                   location[0], location[1], format(d, '.3f'))))

        markers.append(self.plot_point(lat=center[0], lng=center[1], desc=desc0, clr=clr0))
        return markers

    def plot_within_point(self, data, index, radius, loc_col, ctry_col, lat_col, lng_col, clr0='blue', clr1='lightblue'):
        """
        Create markers for all data points within the passed radius of the specified data point.

        :param data:
        :param index: index of the focal data point.
        :type index: int
        :param radius: radius of the search circle (in kilometers).
        :param loc_col:
        :param ctry_col:
        :param lat_col:
        :param lng_col:
        :param clr0:
        :param clr1:
        :return:
        """
        df = read_data(data, {loc_col, ctry_col, lat_col, lng_col})
        if index < len(df):
            coords = (df.loc[index, lat_col], df.loc[index, lng_col])
            location = '%s, %s' % (df.loc[index, loc_col], df.loc[index, ctry_col])
            return self.plot_within_range(df, coords, radius, loc_col, ctry_col, lat_col, lng_col, location, clr0, clr1)
        else:
            raise KeyError('Index out of range.')

    def plot_point_generic(self, lat, lng, desc=None, clr='blue', i_clr='white'):
        if not desc:
            desc = str((lat, lng))
        return Marker(location=(lat, lng), popup=Popup(desc, parse_html=True),
                      icon=Icon(prefix='fa', color=clr, icon='circle', icon_color=i_clr))
    def plot_data_generic(self, data, plot_col, lat_col, lng_col, i_clr='white',as_cluster=True, plot_col_type=None):
        clr_val = 'green'
        iclr_val = i_clr
        if (plot_col_type is not None):
            df = read_data(data, {plot_col, lat_col, lng_col, plot_col_type})
        else:
            df = read_data(data, {plot_col, lat_col, lng_col})
        annotations_temp = df[plot_col].unique()
        annotations = [x for x in annotations_temp if pd.notnull(x)]
        annotations_colors = {}
        for i in range(len(annotations)):
            col_index = i % (len(self.colors))
            annotations_colors[annotations[i]] = self.colors[col_index]

        if as_cluster:
            markers = MarkerCluster()
        else:
            markers = []

        for (index, row) in df.iterrows():
            if pd.notnull(row[lat_col]) and pd.notnull(row[lng_col]):
                lat = row[lat_col]
                lng = row[lng_col]
                descr = row[plot_col]

                if (descr is np.nan):
                    clr_val = 'red'
                    descr = 'missing'
                else:
                    clr_val = annotations_colors[descr]

                if (plot_col_type is not None):
                    pc_type = row[plot_col_type]
                    if(pc_type == 'imputed'):
                        i_clr = 'red'
                    else:
                        i_clr = iclr_val

                marker = self.plot_point_generic(lat=lat, lng=lng, desc=descr, clr=clr_val, i_clr=i_clr)
                if as_cluster:
                    marker.add_to(markers)
                else:
                    markers.append(marker)

        return markers





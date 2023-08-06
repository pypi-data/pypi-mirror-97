from validate_coordinates import *
from iaa_explore import *
import warnings
warnings.filterwarnings("ignore")

class ValidateData:
    def __init__(self,df=None,lat_col=None,lng_col=None,loc_col=None,ctry_col=None):
        """ """
        self.df = df
        self.lat_col = lat_col
        self.lng_col = lng_col
        self.loc_col = loc_col
        self.ctry_col = ctry_col

        self.mTool = MapTool()
        self.shape_dict = process_shapefile()
        # Generate a GeoDataFrame from .shp file.
        self.shape_gdf = get_shape(self.shape_dict['shp'])
        # Determine the EPSG code from .prj file.
        self.prj = get_projection(self.shape_dict['prj'])
        self.shape_geom = 'geometry'
        self.shape_iso2 = 'ISO2'
        self.matched_latlng_df = None
        self.mismatched_latlng = None
        self.flipped = None
        self.geocoded = None
        self.combined = None


    def validate(self):
        """ """
        # Create dataframe from .shp shapefile and the projection
        self.shape_gdf = get_shape(self.shape_dict['shp'])
        # Determine the EPSG code from .prj file.
        self.prj = get_projection(self.shape_dict['prj'])
        # Add the iso2 and iso3 country codes if your data doesn't have them.
        self.with_cc = add_country_code(data=self.df, ctry_col=self.ctry_col)

        gdf = to_gdf(self.df, self.lat_col, self.lng_col, self.prj)
        gdf['ISO2'] = coco.convert(list(gdf[self.ctry_col]), to='ISO2')
        checked_df = check_data_geom(self.loc_col, 'ISO2', gdf, self.shape_gdf, self.shape_geom, self.shape_iso2)
        self.matched_latlng_df = checked_df[0]
        self.mismatched_latlng = checked_df[1]

    def get_combined_data_df(self):
        return self.combined

    def get_matched_latlng_df(self):
        return self.matched_latlng_df

    def get_mismatched_latlng_df(self):
        return self.mismatched_latlng

    def get_flipped_latlng_df(self):
        return self.flipped

    def get_geocoded_latlng_df(self):
        return self.geocoded

    def plot_all_data(self,clr, as_cluster):
        return self.mTool.plot_all_data(self.df, self.loc_col, self.ctry_col, self.lat_col, self.lng_col, clr, as_cluster)

    def plot_matched_latlng_data(self,clr, as_cluster):
        return self.mTool.plot_all_data(self.matched_latlng_df, self.loc_col, self.ctry_col, self.lat_col, self.lng_col, clr, as_cluster)

    def plot_mismatched_latlng(self,clr, as_cluster):
        return self.mTool.plot_all_data(self.mismatched_latlng, self.loc_col, self.ctry_col, self.lat_col, self.lng_col, clr, as_cluster)

    def fix_flipped_latlng(self):
        """ """
        all_pos_gdfs = flip_coords(data=self.mismatched_latlng, lat_col=self.lat_col, lng_col=self.lng_col)
        verified_all_dfs = check_data_geom(all_geodata=all_pos_gdfs, iso2_col='ISO2', eval_col=self.loc_col,
                                           shapedata=self.shape_gdf, shape_geom_col='geometry', shape_iso2_col='ISO2')
        self.flipped = verified_all_dfs[0]
        self.mismatched_latlng = verified_all_dfs[1]

    def geocode_mismatched_latlng(self):
        """ """
        geocoded_df = geocode_coordinates(data=self.mismatched_latlng, loc_col=self.loc_col, ctry_col=self.ctry_col)
        self.geocoded = geocoded_df[0]
        self.mismatched_latlng = geocoded_df[1]

    def combine_validated_data(self):
        """ """
        original_cols = self.df.columns.values.tolist()
        original_cols.extend([self.lat_col, self.lng_col])
        x1 = self.matched_latlng_df
        x1 = x1.filter(original_cols)
        x1['Geocode_Type'] = 'original'

        new_cols = self.df.columns.values.tolist()
        new_cols.extend(['Validated_Lat', 'Validated_Lng', 'Geocode_Type'])
        x1.columns = new_cols

        x2 = self.flipped
        original_cols = self.df.columns.values.tolist()
        original_cols.extend(['Flipped_Lat', 'Flipped_Lng', 'Flipped_Type'])
        x2 = x2.filter(original_cols)
        x2 = x2.rename(columns={'Flipped_Lat': 'Validated_Lat', 'Flipped_Lng': 'Validated_Lng', 'Flipped_Type': 'Geocode_Type'})

        x3 = self.geocoded
        original_cols = self.df.columns.values.tolist()
        original_cols.extend(['Geocoded_Lat', 'Geocoded_Lng', 'GeoCode_Type'])
        x3 = x3.filter(original_cols)
        x3 = x3.rename(columns={'Geocoded_Lat': 'Validated_Lat', 'Geocoded_Lng': 'Validated_Lng', 'GeoCode_Type': 'Geocode_Type'})

        frames = [x1, x2, x3]
        self.combined = pd.concat(frames,ignore_index=True)

from itallic.CleaningUtils.validate_coordinates import *
from itallic.MapTools.iaa_explore import *

import numpy as np
import pandas as pd
from sklearn import neighbors


class AnnotateTool:
    def __init__(self, df, xcols, ycol):
        self.df = df
        self.xcols = xcols
        self.ycol = ycol
        self.predicted_y = None
        self.predicted_df = None
        self.updated_df = None

        missing_region = self.df[self.df[self.ycol].isnull()]
        with_region = self.df[self.df[self.ycol].notnull()]

        self.X = with_region[self.xcols]
        self.y = with_region.loc[:, self.ycol]
        self.X_predict = missing_region[self.xcols]

    def get_updated_df(self):
        return self.updated_df

    def predict_Y(self, n_neighbors):
        # This function is being used by this one function. To keep namespace clean.
        # define it in here
        def update_annotation(original_value, imputed_value):
            if (original_value is np.nan) and (imputed_value is not np.nan):
                return imputed_value, 'imputed'
            else:
                return original_value, 'original'

        clf = neighbors.KNeighborsClassifier(n_neighbors, weights='distance')
        clf.fit(self.X, self.y)
        self.predicted_y = clf.predict(self.X_predict)
        col_name = 'predicted_'+self.ycol
        self.X_predict[col_name] = self.predicted_y
        self.predicted_df = pd.merge(self.df, self.X_predict, on=self.xcols, how='left')
        result=pd.DataFrame(self.predicted_df[[self.ycol, col_name]].apply(lambda x: update_annotation(*x), axis=1, result_type="expand"))
        result.columns = ['updated_'+self.ycol, self.ycol+'_type']
        self.updated_df = pd.concat([self.df, result], axis=1)



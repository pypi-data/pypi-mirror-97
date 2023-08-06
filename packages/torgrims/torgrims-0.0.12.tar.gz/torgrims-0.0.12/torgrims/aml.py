import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix

class Aml():

    @staticmethod
    def percentile_to_proba(y_proba, t_percentiles):
        return [np.percentile(y_proba, p) for p in t_percentiles]    

    @staticmethod
    def acc_table_for_metric(y_obs, y_proba, thresholds, thresh_type):
        assert (len(y_obs) == len(y_proba)), \
            f'dims not matching, {len(y_obs)} vs {len(y_proba)}'

        n_obs = len(y_obs)
        n_threshold = len(thresholds)

        if thresh_type=='percentile':
            thresholds = Aml.percentile_to_proba(y_proba, thresholds)

        prediction_given_thresh = np.empty(
            shape=(n_obs, n_threshold),
            dtype=int
            )

        accuracy_table = np.empty(
            shape=(n_threshold, 4),  # TP, FP, TN, FN
            dtype=int
        )

        for i, t in enumerate(thresholds):
            score = (t < y_proba).astype(int)
            conf_matrix = confusion_matrix(y_obs, score)
            prediction_given_thresh[:,i] = score
            # Docs: The third dimension always has 4 
            # values: TP, FP, TN, FN, and always in that order
            TP = conf_matrix[1,1]
            FP = conf_matrix[0,1]
            TN = conf_matrix[0,0]
            FN = conf_matrix[1,0]
            accuracy_table[i,:]=[TP, FP, TN, FN]

        #return (prediction_given_thresh, accuracy_table)
        return accuracy_table.tolist()

    @staticmethod
    def make_accuracy_tables(df_proba, df_actual, thresh_proba, thresh_percentile=None):

        class_names = list(df_proba.columns)
        class_probabilities = df_proba.values
        y_actual_ = df_actual.values
        
        if thresh_percentile is None:
            thresh_percentile = [100*t for t in thresh_proba]

        # if binary classification, only calculate for class 1
        if len(class_names) == 2:
            class_names = [class_names[1]]
            class_probabilities = class_probabilities[:,1].reshape(-1,1)

        probability_tables=[Aml.acc_table_for_metric(y_obs=y_actual_, 
                                y_proba=class_probabilities[:,i], 
                                thresholds=thresh_proba, 
                                thresh_type='probability') 
                            for i in range(class_probabilities.shape[1])]


        percentile_tables=[Aml.acc_table_for_metric(y_obs=y_actual_, 
                                y_proba=class_probabilities[:,i], 
                                thresholds=thresh_percentile, 
                                thresh_type='percentile') 
                            for i in range(class_probabilities.shape[1])]

        return {
            "schema_type": "accuracy_table",
            "schema_version": "v1",
            "data":{
                "class_labels":class_names,
                "probability_thresholds":thresh_proba,
                "percentile_thresholds":thresh_percentile,
                "probability_tables":probability_tables,
                "percentile_tables":percentile_tables
            }
        }

    @staticmethod
    def make_confuson_matrix(y_obs, score, class_labels):
        conf_matrix = confusion_matrix(y_obs, score).tolist()
        return {
            "schema_type": "confusion_matrix",
            "schema_version": "v1",
            "data": {
                "class_labels": class_labels,
                "matrix": conf_matrix
            }
        }
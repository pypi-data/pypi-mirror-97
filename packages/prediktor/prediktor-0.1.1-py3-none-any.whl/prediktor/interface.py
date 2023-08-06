import numpy as np
import pandas as pd
import time

class Predictor(object):
    
    def __init__(
        self, 
        preprocessor, 
        model, 
        icp, 
        model_id=None
        ):
        """
        Parameters
        ----------
        preprocessor: sklearn.base.TransformerMixin
            sklearn object implementing the transform method
            for obtaining the input features.
        model: sklearn.base.RegressorMixin or sklearn.base.ClassifierMixin
            sklearn object implementing the predict method for
            obtaining the model outputs.
        icp: nonconformist.icp.IcpRegressor or nonconformist.icp.IcpClassifier
            sklearn object implementing the predict method for 
            obtaining the confidence intervals.
        model_id: string
            unique idefifier for the model.
        """
        
        self.preprocessor = preprocessor
        self.model = model
        self.icp = icp
        self.model_id = model_id
        
        self.categorical_cols = preprocessor.transformers[0][2]
        self.numerical_cols = preprocessor.transformers[1][2]
        self.input_cols = self.categorical_cols + self.numerical_cols
        
    def _valid_inputs(self, input_raw):
        if isinstance(input_raw, dict):
            if set(input_raw.keys()) != set(self.input_cols):
                return False
        if isinstance(input_raw, list):
            if any([set(record.keys()) != set(self.input_cols) for record in input_raw]):
                return False
        return True

    def _cast_to_dataframe(self, input_raw):
        if isinstance(input_raw, dict):
            return pd.DataFrame([input_raw, ], columns=self.input_cols)
        elif isinstance(input_raw, list):
            return pd.DataFrame(input_raw, columns=self.input_cols)
    
    def predict(self, input_raw, confidence=0.8):
        """
        Parameters
        ----------
        input_raw: dict or list
            if dict, corresponds to the inputs of the model, 
            where keys are the feature names and values are
            the feature values. If list, corresponds to a list
            of dictionaries in the previous format.
        confidence: float
            value between 0 and 1 indicating the confidence 
            level to build the confirence intervals
        """
        
        if not self._valid_inputs(input_raw):
            return {
            "prediction": None,
            "process_time": None,
            "model_id": None,
            "input_raw": None,
            "input_features": None,
            "status": "error",
            "message": "invalid input format"
        }
        input_dataframe = self._cast_to_dataframe(input_raw)
        
        start_time = time.time()

        input_dataframe.loc[:, self.input_cols] = self.preprocessor.transform(input_dataframe)
        model_prediction = self.model.predict(input_dataframe.values)
        interval_prediction = self.icp.predict(input_dataframe.values, significance=1-confidence)
        prediction = np.column_stack([
            interval_prediction[:,0], 
            model_prediction[:], 
            interval_prediction[:,1]
        ])

        end_time = time.time()
        process_time = (end_time - start_time)*1000
        
        return {
            "prediction": prediction,
            "process_time": process_time,
            "model_id": self.model_id,
            "input_raw": input_raw,
            "input_features": input_dataframe.to_dict(orient="records"),
            "status": "success",
            "message": None,
        }

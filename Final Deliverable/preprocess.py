import os
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder

train_columns = ["QUARTER", "MONTH", "DAY_OF_MONTH", "DAY_OF_WEEK", "ORIGIN", "DEST", "DISTANCE", "DEP_DEL15"]

class Preprocess:
    def __init__(self) -> None:
        self.base_path = os.path.join(os.getcwd(), 'encoders')
        self.origin_encoder = LabelEncoder()
        self.dest_encoder = LabelEncoder()

        if not os.path.exists(self.base_path):
            print('Encoders not found, Creating Files')
            os.mkdir(self.base_path)
    
        else:
            with open(os.path.join(self.base_path, 'origin_encoder.pkl'), 'rb') as file:
                classes = pickle.load(file)
                self.origin_encoder.classes_ = classes
            with open(os.path.join(self.base_path, 'dest_encoder.pkl'), 'rb') as file:
                classes = pickle.load(file)
                self.dest_encoder.classes_ = classes
    
    def __check_cloumns(self) -> list:
        cols = []
        for val in train_columns:
            if val not in self.data.columns:
                cols.append(val)
        if len(cols) == 0:
            return None
        return cols

    def train_preprocess(self, data_path) -> pd.DataFrame:
        self.data = pd.read_csv(data_path)

        if self.__check_cloumns() is not None:
            print("CSV does not contain the required columns", self.__check_cloumns())
            return False

        del_columns = []
        for col in self.data.columns:
            if col not in train_columns:
                del_columns.append(col)
        
        for col, val in zip(self.data.columns, self.data.columns.str.match('Unamed')):
            if val:
                del_columns.append(col)

        self.data = self.data.drop(del_columns, axis  = 1)
        self.data = self.data.dropna()

        self.data['ORIGIN'] = self.origin_encoder.fit_transform(self.data['ORIGIN'])
        self.data['DEST'] = self.dest_encoder.fit_transform(self.data['DEST'])

        with open(os.path.join(self.base_path, 'origin_encoder.pkl'), 'wb') as file:
            pickle.dump(self.origin_encoder.classes_, file)
        with open(os.path.join(self.base_path, 'dest_encoder.pkl'), 'wb') as file:
            pickle.dump(self.dest_encoder.classes_, file)

        y = self.data['DEP_DEL15']
        x = self.data.drop(columns='DEP_DEL15')

        return x.to_numpy(),y.to_numpy()
    
    def test_preprocess(self, x: list)-> list:
        x[4] = self.origin_encoder.transform([x[4]])[0]
        x[5] = self.dest_encoder.transform([x[5]])[0]
        return x
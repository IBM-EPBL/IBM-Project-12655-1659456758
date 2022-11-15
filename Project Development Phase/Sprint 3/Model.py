import os
import pickle
import format_input
from sklearn.tree import DecisionTreeClassifier as dt
from preprocess import Preprocess

def load_model() -> dt:
    try:
        with open('model/decisionTree.pkl', 'rb') as file:
            model = pickle.load(file)
    except FileNotFoundError:
        x, y = Preprocess().train_preprocess('./dataset/flightdata.csv')
        model = dt()
        model.fit(x,y)
        if not os.path.exists('model'):
            os.mkdir('model')
        with open('model/decisionTree.pkl', 'wb') as file:
            pickle.dump(model, file)
    return model

def predict(origin: str, dest: str, date: str) -> int: 
    model = load_model()
    x = format_input.extract_date(date)
    x.append(origin)
    x.append(dest)
    try:
        x.append(format_input.extract_distance(origin, dest))
    except IndexError:
        return [2]
    x = Preprocess().test_preprocess(x)
    return model.predict([x])


if __name__=="__main__":
    print(predict(*("DTW", "MSP", "2016-12-11")))
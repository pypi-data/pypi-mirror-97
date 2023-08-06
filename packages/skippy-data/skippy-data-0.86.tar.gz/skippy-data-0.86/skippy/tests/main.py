import json
import logging
import pandas as pd
from io import StringIO
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from skippy.data.decorator import consume, produce


@consume()
@produce()
def handle(req, data=None):
    logging.getLogger().setLevel(logging.DEBUG)
    logging.info("data file received %d" % len(data['pre-processed/data_35M.csv']))
    data_decoded = str(data['pre-processed/data_35M.csv'].decode("utf-8"))
    dataset = pd.read_csv(StringIO(data_decoded), sep=",")
    dataset.head()

    x = dataset.iloc[:, 0:4].values
    y = dataset.iloc[:, 4].values

    pre_model = train_test_split(x, y, test_size=0.2, random_state=0)
    logging.info("Pre-Processed finished")
    return pre_model


@consume()
@produce()
def handle2(req, data=None):
    x_train = bytes_to_numpy(data['pre-processed/pre-model.npy'], 0)
    x_test = bytes_to_numpy(data['pre-processed/pre-model.npy'], 1)
    y_train = bytes_to_numpy(data['pre-processed/pre-model.npy'], 2)

    sc = StandardScaler()
    x_train = sc.fit_transform(x_train)
    x_test = sc.transform(x_test)

    regressor = RandomForestRegressor(n_estimators=200, random_state=0)
    print("Start training")
    regressor.fit(x_train, y_train)
    y_pred_data = regressor.predict(x_test)
    print("Training finished")
    return y_pred_data


def main():
    handle('bbbbbbbbbb')
    handle2('bbbbbbbbbb')
    # files = download_files(urns=None)
    # upload_file(json.dumps(files),urn=None)


def bytes_to_numpy(bytes, index: int = 1) -> np.array:
    arr = np.array(bytes[index])
    return arr


if __name__ == '__main__':
    main()

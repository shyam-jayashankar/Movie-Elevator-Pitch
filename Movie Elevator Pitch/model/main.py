import numpy
import argparse
import configparser
import os
import pandas as pd
from data import cleanse_data, sent_to_words, detokenize, processText
from model import  *
from sklearn.model_selection import train_test_split




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_file', help='Configuration file', required=True)
    args = parser.parse_args()
    config_file = args.config_file

    config = configparser.ConfigParser()
    config.read_file(open(config_file))

    data_loc = config.get('main', 'dataset_loc')
    if not os.path.isfile(data_loc):
        print('Please provide a valid location of the dataset.')
        exit()

    max_words = int(config.get('main', 'max_words'))
    df = pd.read_csv(data_loc, error_bad_lines=False)
    df=df[['description', 'rating']]
    df.dropna(inplace=True)
    df['rating'] = df['rating'].apply(lambda x: 1 if x > 7.0 else 0)

    temp = []

    data_to_list = df['description'].values.tolist()

    for i in range(len(data_to_list)):
        # print(data_to_list[i])
        temp.append(cleanse_data(data_to_list[i]))

    data_words = list(sent_to_words(temp))
    # print(data_words)
    # print(temp)
    data = []
    for i in range(len(data_words)):
        data.append(detokenize(data_words[i]))
    print(data[:5])


    X = processText(data, max_words)
    # print(X)

    print(X.shape)
    print("Number of words")
    print(len(numpy.unique(numpy.hstack(X))))

    y = []
    target_y = df['rating'].values.tolist()
    for i in range(len(target_y)):
        y.append(target_y[i])

    y = numpy.asarray(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)


    print("X train: ", X_train.shape)
    print("X_test:", X_test.shape)
    print("Y_train: ", y_train.shape)
    print("Y_test: ", y_test.shape)
    model = NNModel( embedding_dim=128, max_words=max_words)
    score = model.fit(X_train, y_train, X_test, y_test)

    print("Accuracy: %.2f%%" % (score[1] * 100))






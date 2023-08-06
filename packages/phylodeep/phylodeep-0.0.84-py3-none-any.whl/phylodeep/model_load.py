import warnings
import os
import sys
import pickle as pk
import pandas as pd

from sklearn.externals import joblib

# import joblib
# sys.modules['sklearn.externals.joblib'] = joblib

from tensorflow.python.keras.models import model_from_json

warnings.filterwarnings('ignore')

PRETRAINED_MODELS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'pretrained_models')
PRETRAINED_PCA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'pca_a_priori')


def pca_scale_load(tree_size, model):
    pca_reload = pk.load(open(os.path.join(PRETRAINED_PCA_DIR, 'models', model + '_' + tree_size + 'PCA' + '.pkl'), 'r'))

    scaler = joblib.load(os.path.join(PRETRAINED_PCA_DIR, 'scalers', model + '_' + tree_size + 'PCA' + '.pkl'))

    return pca_reload, scaler


def pca_data_load(tree_size, model):
    pca_data = pd.read_csv(PRETRAINED_PCA_DIR+ 'models/' + model + '_' + tree_size + 'PCA' + '.csv.', header=None)

    return pca_data


def model_scale_load_ffnn(tree_size, model):
    pred_method = 'FFNN'
    json_file = open(os.path.join(PRETRAINED_MODELS_DIR, 'models', model + '_' + tree_size + '_' + pred_method +
                                  '.json'), 'r')
    loaded_model = json_file.read()
    json_file.close()

    model_ffnn = model_from_json(loaded_model)
    model_ffnn.load_weights(os.path.join(PRETRAINED_MODELS_DIR, 'weights', model + '_' + tree_size + '_' + pred_method +
                                         '.h5'))
    scaler = joblib.load(os.path.join(PRETRAINED_MODELS_DIR, 'scalers', model + '_' + tree_size + '_' + pred_method +
                                      '.pkl'))

    return model_ffnn, scaler


def model_load_cnn(tree_size, model):
    pred_method = 'CNN'
    json_file = open(os.path.join(PRETRAINED_MODELS_DIR, 'models', model + '_' + tree_size + '_' + pred_method +
                                  '.json'), 'r')
    loaded_model = json_file.read()
    json_file.close()

    model_cnn = model_from_json(loaded_model)
    model_cnn.load_weights(os.path.join(PRETRAINED_MODELS_DIR, 'weights', model + '_' + tree_size + '_' + pred_method +
                                        '.h5'))

    return model_cnn

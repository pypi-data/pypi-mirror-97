import numpy as np
import pandas as pd
import tensorflow as tf
import tempfile

from .utils import Log, HappyLearningUtils
from tensorflow.keras.activations import exponential, hard_sigmoid, linear, relu, selu, sigmoid, softmax, tanh
from tensorflow.keras.callbacks import EarlyStopping, TerminateOnNaN
from tensorflow.keras.layers import AlphaDropout, Bidirectional, Conv1D, Conv2D, Conv3D, Dense, Dropout, LSTM
from tensorflow.keras.optimizers import Adam, RMSprop
from typing import List

# TODO:
#  1) Implement LSTM network using TensorFlow
#  2) Implement Convolutional network (1D for time-series / 2D for images) using TensorFlow

MAX_HIDDEN_LAYERS: int = 25
HIDDEN_LAYER_CATEGORY: dict = dict(small=(1, 3),
                                   medium=(4, 6),
                                   big=(7, 9),
                                   very_big=(10, MAX_HIDDEN_LAYERS)
                                   )
ACTIVATION: dict = dict(linear=linear,
                        exponential=exponential,
                        hard_sigmoid=hard_sigmoid,
                        relu=relu,
                        selu=selu,
                        sigmoid=sigmoid,
                        softmax=softmax,
                        tanh=tanh
                        )
INITIALIZER: List[str] = ['glorot_normal',
                          'glorot_uniform',
                          #'he_normal',
                          #'he_uniform',
                          #'identity',
                          'lecun_normal',
                          'lecun_uniform',
                          'normal',
                          'ones',
                          #'orthogonal',
                          'random_normal',
                          'random_uniform',
                          'truncated_normal',
                          'uniform',
                          'zeros'
                         ]
LOSS: dict = dict(clf_binary=['binary_crossentropy', 'hinge', 'squared_hinge'],
                  clf_multi=['categorical_crossentropy', 'categorical_hinge', 'kullback_leibler_divergence', 'sparse_categorical_crossentropy'],
                  reg=['mean_absolute_error', 'mean_absolute_percentage_error', 'mean_squared_error', 'mean_squared_logarithmic_error']
                  )
METRIC: dict = dict(clf_binary=['binary_accuracy', 'hinge', 'squared_hinge'],
                    clf_multi=['categorical_accuracy', 'kullback_leibler_divergence', 'sparse_categorical_accuracy'],
                    reg=['mean_absolute_error', 'mean_absolute_percentage_error', 'mean_squared_error', 'mean_squared_logarithmic_error']
                    )
OPTIMIZER: dict = dict(adam=Adam, rmsprop=RMSprop)
REGULARIZER: List[str] = ['l1', 'l2']
PARAM_SPACE: dict = dict(mlp=dict(hidden_layers=-1,
                                  learning_rate=-1.0,
                                  batch_size=-1,
                                  epochs=-1,
                                  early_stopping=['early_stopping_True', 'early_stopping_False'],
                                  patience=-1,
                                  validation_split=-1.0
                                  ),
                         lstm=dict(),
                         cnn=dict()
                         )

for hidden_layer in range(0, MAX_HIDDEN_LAYERS, 1):
    PARAM_SPACE['mlp'].update({'neurons_hidden_layer_{}'.format(hidden_layer + 1): -1,
                               'dropout_hidden_layer_{}'.format(hidden_layer + 1): -1.0
                               })
    for A in ACTIVATION.keys():
        PARAM_SPACE['mlp'].update({'activation_hidden_layer_{}'.format(hidden_layer + 1): 'activation_hidden_layer_{}_{}'.format(hidden_layer + 1, A)})
        if hidden_layer + 1 == MAX_HIDDEN_LAYERS:
            PARAM_SPACE['mlp'].update({'activation_input_layer': 'activation_input_layer_{}'.format(A)})
            PARAM_SPACE['mlp'].update({'activation_output_layer': 'activation_output_layer_{}'.format(A)})

for I in INITIALIZER:
    PARAM_SPACE['mlp'].update({'bias_initializer': 'bias_initializer_{}'.format(I),
                               'kernel_initializer': 'kernel_initializer_{}'.format(I)
                               })
for O in OPTIMIZER.keys():
    PARAM_SPACE['mlp'].update({'optimizer': 'optimizer_{}'.format(O)})
for R in REGULARIZER:
    PARAM_SPACE['mlp'].update({'bias_regularizer': 'bias_regularizer_{}'.format(R)})
    PARAM_SPACE['mlp'].update({'activity_regularizer': 'activity_regularizer_{}'.format(R)})
    PARAM_SPACE['mlp'].update({'kernel_regularizer': 'kernel_regularizer_{}'.format(R)})


def make_keras_picklable():
    """
    Enable pickle export for TensorFlow models (.hdf5 file)
    """
    def __getstate__(self):
        model_str = ""
        with tempfile.NamedTemporaryFile(suffix='.hdf5', delete=True) as fd:
            tf.keras.models.save_model(self, fd.name, overwrite=True)
            model_str = fd.read()
        d = {'model_str': model_str}
        return d

    def __setstate__(self, state):
        with tempfile.NamedTemporaryFile(suffix='.hdf5', delete=True) as fd:
            fd.write(state['model_str'])
            fd.flush()
            model = tf.keras.models.load_model(fd.name)
        self.__dict__ = model.__dict__

    cls = tf.keras.models.Model
    cls.__getstate__ = __getstate__
    cls.__setstate__ = __setstate__


class MultiLayerPerceptronException(Exception):
    """
    Class for handling exceptions for class Multi-Layer Perceptron
    """
    pass


class MultiLayerPerceptron:
    """
    Class for building Multi-Layer Perceptron (MLP)
    """
    def __init__(self,
                 n_cases: int,
                 n_features: int,
                 hyper_param: dict = None,
                 model: tf.keras.Sequential = None,
                 layer_size_cat: str = None,
                 max_layer_size: int = MAX_HIDDEN_LAYERS,
                 use_geometric_progression: bool = True,
                 force_descending_neurons_size: bool = True,
                 cpu_cores: int = 0,
                 gpu_cores: int = 0,
                 tpu_cores: int = 0,
                 seed: int = 1234,
                 deep_learning_framework: str = 'tensorflow'
                 ):
        """
        :param n_cases: int
            Number of cases in data set

        :param n_features: int
            Number of features in data set

        :param hyper_param: dict
            Pre-configured hyper parameter

        :param model: object
            Fitted TensorFlow model object

        :param layer_size_cat: str
            Name of the hidden layer size category
                -> small: From 1 to 3 hidden layers
                -> medium: From 4 to 6 hidden layers
                -> big: From 7 to 9 hidden layers
                -> very_big: From 10 to defined maximum of hidden layers

        :param max_layer_size: int
            Maximum number of hidden layers to use (default: 25 hidden layers)

        :param use_geometric_progression: bool
            Whether to use geometric progression for choosing number of neurons for each layer or not

        :param force_descending_neurons_size: bool
            Whether to force that chosen number of neurons are smaller each layer (starting from number of input neurons)

        :param cpu_cores: int
            Number of CPU cores to use

        :param gpu_cores: int
            Number of GPU cores to use

        :param tpu_cores: int
            Number of GPU cores to use

        :param seed: int
            Set seed

        :param deep_learning_framework: str
            Name of the used deep learning framework
                -> custom: Customized deep learning framework
                -> tf, tensorflow: Google TensorFlow
        """
        self.ml_type: str = ''
        self.seed: int = seed
        self.n_cases: int = n_cases
        self.n_features: int = n_features
        self.hyper_param: dict = hyper_param
        self.cpu_cores: int = cpu_cores
        self.gpu_cores: int = gpu_cores
        self.tpu_cores: int = tpu_cores
        self.model = model
        global MAX_HIDDEN_LAYERS
        self.max_hidden_layers: int = max_layer_size if max_layer_size > 0 else MAX_HIDDEN_LAYERS
        MAX_HIDDEN_LAYERS = self.max_hidden_layers
        self.hidden_layer_category: str = layer_size_cat
        if self.hidden_layer_category is not None:
            if self.hidden_layer_category not in HIDDEN_LAYER_CATEGORY.keys():
                self.hidden_layer_category = None
        self.geometric_progression: bool = use_geometric_progression
        self.descending_neurons: bool = force_descending_neurons_size
        self.hidden_layer_template: dict = {}
        for h in range(0, MAX_HIDDEN_LAYERS, 1):
            self.hidden_layer_template.update({'neurons_hidden_layer_{}'.format(h + 1): 0,
                                               'activation_hidden_layer_{}'.format(h + 1): 0,
                                               'dropout_hidden_layer_{}'.format(h + 1): 0
                                               })
        self.deep_learning_framework: str = deep_learning_framework

    @staticmethod
    def _one_hot_encoding(values: np.array) -> np.ndarray:
        """
        One-hot encode categorical (target) feature

        :return np.ndarray:
            One-hot encoded feature
        """
        return tf.keras.utils.to_categorical(y=values)

    def mlp(self) -> object:
        """
        Generate and config Multi-Layer Perceptron using TensorFlow

        :return tf.keras.Sequential:
            TensorFlow object containing the Multi-Layer Perceptron
        """
        self.model: tf.keras.Sequential = tf.keras.Sequential()
        _network: dict = self.mlp_param()
        if self.hyper_param is None:
            self.hyper_param = _network
        else:
            for p in _network.keys():
                if p not in self.hyper_param.keys():
                    self.hyper_param.update({p: _network.get(p)})
        _hidden_layers: int = self.hyper_param.get('hidden_layers')
        self.model.add(Dense(units=self.n_features,
                             activation=self.hyper_param.get('activation_input_layer'),
                             use_bias=True,
                             bias_constraint=None,
                             bias_initializer=self.hyper_param.get('bias_initializer'),
                             bias_regularizer=self.hyper_param.get('bias_regularizer'),
                             activity_regularizer=self.hyper_param.get('activity_regularizer'),
                             kernel_constraint=None,
                             kernel_initializer=self.hyper_param.get('kernel_initializer'),
                             kernel_regularizer=self.hyper_param.get('kernel_regularizer'),
                             input_shape=(self.n_features,)
                             )
                       )
        _n: int = _hidden_layers
        while _n > 0:
            self.model.add(Dense(units=self.hyper_param.get('neurons_hidden_layer_{}'.format(_hidden_layers + 1 - _n)),
                                 activation=self.hyper_param.get('activation_hidden_layer_{}'.format(_hidden_layers + 1 - _n)),
                                 use_bias=True,
                                 bias_constraint=None,
                                 bias_initializer=self.hyper_param.get('bias_initializer'),
                                 bias_regularizer=self.hyper_param.get('bias_regularizer'),
                                 activity_regularizer=self.hyper_param.get('activity_regularizer'),
                                 kernel_constraint=None,
                                 kernel_initializer=self.hyper_param.get('kernel_initializer'),
                                 kernel_regularizer=self.hyper_param.get('kernel_regularizer')
                                 )
                           )
            self.model.add(Dropout(self.hyper_param.get('dropout_hidden_layer_{}'.format(_hidden_layers + 1 - _n))))
            _n -= 1
        return self

    def mlp_param(self) -> dict:
        """
        Generate and config Multi-Layer Perceptron using TensorFlow

        :return dict:
            Multi-Layer Perceptron parameter config
        """
        _n: int = 3
        _b: int = 0
        _max_batch_size: int = int(self.n_cases / 4)
        while _b < _max_batch_size:
            if _n >= 3:
                _n += 1
            _b = max(HappyLearningUtils().geometric_progression(n=_n, ratio=2))
        _batch_size: List[int] = HappyLearningUtils().geometric_progression(n=_n, ratio=2)
        if self.hidden_layer_category is None:
            _hidden_layer_range: tuple = HIDDEN_LAYER_CATEGORY.get(np.random.choice(a=list(HIDDEN_LAYER_CATEGORY.keys())))
        else:
            _hidden_layer_range: tuple = HIDDEN_LAYER_CATEGORY.get(self.hidden_layer_category)
        _network: dict = self.hidden_layer_template
        _network.update(hidden_layers=np.random.randint(low=_hidden_layer_range[0], high=_hidden_layer_range[1]),
                        activation_input_layer=ACTIVATION.get(np.random.choice(a=list(ACTIVATION.keys()))),
                        activation_output_layer=ACTIVATION.get(np.random.choice(a=list(ACTIVATION.keys()))),
                        bias_initializer=np.random.choice(a=INITIALIZER),
                        bias_regularizer=np.random.choice(a=REGULARIZER),
                        #activity_regularizer=REGULARIZER.get(np.random.choice(a=list(REGULARIZER.keys()))),
                        kernel_initializer=np.random.choice(a=INITIALIZER),
                        kernel_regularizer=np.random.choice(a=REGULARIZER),
                        optimizer=OPTIMIZER.get(np.random.choice(a=list(OPTIMIZER.keys()))),
                        learning_rate=np.random.uniform(0.000005, 0.45),
                        batch_size=np.random.choice(a=_batch_size),
                        epochs=np.random.randint(low=10, high=50),
                        early_stopping=np.random.choice(a=[True, False]),
                        patience=np.random.randint(low=1, high=15),
                        validation_split=np.random.uniform(low=0.05, high=0.25)
                        )
        for l in range(0, _network.get('hidden_layers'), 1):
            _network.update({'neurons_hidden_layer_{}'.format(l + 1): np.random.choice(a=[2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]),
                             'activation_hidden_layer_{}'.format(l + 1): ACTIVATION.get(np.random.choice(a=list(ACTIVATION.keys()))),
                             'dropout_hidden_layer_{}'.format(l + 1): np.random.uniform(low=0.01, high=0.5)
                             })
        return _network

    def predict(self, x: np.array) -> np.array:
        """
        Get prediction from Multi-Layer Perceptron

        :param x: np.array
            Test data set containing predictor features

        :return np.array:
            Predictions
        """
        return self.model.predict(x=x)

    def predict_proba(self, x: np.array) -> np.array:
        """
        Get prediction from Multi-Layer Perceptron

        :param x: np.array
            Test data set containing predictor features

        :return np.array:
            Predictions
        """
        return self.predict(x=x)

    def train(self, x: np.array, y: np.array) -> tf.keras.Sequential:
        """
        Train Multi-Layer Perceptron

        :param x: np.array
            Train data set of predictor features

        :param y: np.array
            Train data set of target feature

        :return tf.keras.Sequential:
            Keras feed-forward neural network object
        """
        self.ml_type = HappyLearningUtils().get_ml_type(values=y)
        while True:
            if self.ml_type == 'reg':
                _y: np.array = y
                self.model.add(Dense(units=1,
                                     activation=self.hyper_param.get('activation_output_layer'),
                                     use_bias=True,
                                     bias_constraint=None,
                                     bias_initializer=self.hyper_param.get('bias_initializer'),
                                     bias_regularizer=self.hyper_param.get('bias_regularizer'),
                                     activity_regularizer=self.hyper_param.get('activity_regularizer'),
                                     kernel_constraint=None,
                                     kernel_initializer=self.hyper_param.get('kernel_initializer'),
                                     kernel_regularizer=self.hyper_param.get('kernel_regularizer')
                                     )
                               )
            else:
                _y: np.array = self._one_hot_encoding(values=y)
                self.model.add(Dense(units=len(pd.unique(values=y)),
                                     activation='softmax',
                                     use_bias=True,
                                     bias_constraint=None,
                                     bias_initializer=self.hyper_param.get('bias_initializer'),
                                     bias_regularizer=self.hyper_param.get('bias_regularizer'),
                                     activity_regularizer=self.hyper_param.get('activity_regularizer'),
                                     kernel_constraint=None,
                                     kernel_initializer=self.hyper_param.get('kernel_initializer'),
                                     kernel_regularizer=self.hyper_param.get('kernel_regularizer')
                                     )
                               )
            self.model.compile(optimizer=self.hyper_param.get('optimizer')(learning_rate=self.hyper_param.get('learning_rate')),
                               loss=LOSS[self.ml_type][0],
                               metrics=[METRIC[self.ml_type][0]],
                               loss_weights=None,
                               sample_weight_mode=None,
                               weighted_metrics=None,
                               target_tensors=None,
                               distribute=None
                               )
            _callback: list = []
            if self.hyper_param.get('early_stopping'):
                _callback.append(EarlyStopping(monitor='loss',
                                               min_delta=0,
                                               patience=self.hyper_param.get('patience'),
                                               verbose=0,
                                               mode='auto',
                                               baseline=None,
                                               restore_best_weights=False
                                               )
                                 )
            _callback.append(TerminateOnNaN())
            _history = self.model.fit(x=x,
                                      y=_y,
                                      epochs=self.hyper_param.get('epochs'),
                                      batch_size=self.hyper_param.get('batch_size'),
                                      verbose=0,
                                      callbacks=_callback if len(_callback) > 0 else None,
                                      validation_split=self.hyper_param.get('validation_split'),
                                      validation_data=None,
                                      shuffle=True,
                                      class_weight=None,
                                      sample_weight=None,
                                      initial_epoch=0,
                                      steps_per_epoch=None,
                                      validation_steps=None,
                                      validation_freq=1,
                                      max_queue_size=10,
                                      workers=1,
                                      use_multiprocessing=False
                                      )
            if sum(_history.history['loss']) >= 0:
                break
            else:
                Log(write=False).log('Generated invalid neural network. Re-Initialization ...')
                self.hyper_param = None
                _new_mlp = self.mlp()
                self.model = _new_mlp.model
        return self.model


class LongShortTermMemoryNetwork:
    """
    Class for building Long-Short Term Memory (LSTM) network
    """
    def __init__(self,
                 n_cases: int,
                 n_time_steps: int,
                 n_features: int,
                 hyper_param: dict = None,
                 model: tf.keras.Sequential = None,
                 cpu_cores: int = 0,
                 gpu_cores: int = 0,
                 tpu_cores: int = 0,
                 seed: int = 1234,
                 deep_learning_framework: str = 'tensorflow'
                 ):
        """
        :param n_cases: int
            Number of cases

        :param n_time_steps: int
            Number of time steps

        :param n_features: int
            Number of features

        :param hyper_param:
        :param model:
        :param cpu_cores:
        :param gpu_cores:
        :param tpu_cores:
        :param seed:
        :param deep_learning_framework:
        """
        self.seed: int = seed if seed > 0 else 1234
        self.n_cases: int = n_cases
        self.n_features: int = n_features
        self.n_time_steps: int = n_time_steps
        self.cpu_cores: int = cpu_cores
        self.gpu_cores: int = gpu_cores
        self.tpu_cores: int = tpu_cores
        self.model = model
        self.hyper_param: dict = hyper_param
        self.optimizer = ['adam', 'rmsprop']
        self.activation = [linear, exponential, hard_sigmoid, relu, selu, sigmoid, softmax, tanh]
        self.initializer = ['glorot_normal']
        self.hidden_layer_template: dict = {}
        for h in range(0, 100, 1):
            if h == 0:
                _h: int = h
            else:
                _h: int = h + 1
            self.hidden_layer_template.update({'neurons_hidden_layer{}'.format(_h): 0,
                                               'activation_hidden_layer{}'.format(_h): 0,
                                               'dropout_hidden_layer{}'.format(_h): 0,
                                               'bidirectional_hidden_layer{}'.format(_h): True
                                               })
        self.deep_leraning_framework: str = deep_learning_framework

    def lstm(self) -> object:
        """
        Generate and config Long-Short Term Memory Network using TensorFlow

        :return tf.keras.Sequential:
            TensorFlow object containing the LSTM network
        """
        self.model: tf.keras.Sequential = tf.keras.Sequential()
        _network: dict = self.lstm_param()
        if self.hyper_param is None:
            self.hyper_param = _network
        else:
            for p in _network.keys():
                if p not in self.hyper_param.keys():
                    self.hyper_param.update({p: _network.get(p)})
        _hidden_layers: int = self.hyper_param.get('hidden_layers')
        if np.random.uniform(low=0, high=1) >= 0.5:
            self.model.add(Bidirectional(LSTM(units=self.n_features,
                                              activation=self.hyper_param.get('activation_input_layer'),
                                              input_shape=(self.n_features,),
                                              kernel_initializer=self.hyper_param.get('initializer')
                                              )
                                         )
                           )
        else:
            self.model.add(LSTM(units=self.n_features,
                                activation=self.hyper_param.get('activation_input_layer'),
                                input_shape=(self.n_features,),
                                kernel_initializer=self.hyper_param.get('initializer')
                                )
                           )
        _n: int = _hidden_layers
        while _n > 0:
            if self.hyper_param.get('bidirectional_hidden_layer_{}'.format(_hidden_layers + 1 - _n)):
                self.model.add(Bidirectional(LSTM(units=self.hyper_param.get('neurons_hidden_layer_{}'.format(_hidden_layers + 1 - _n)),
                                                  activation=self.hyper_param.get('activation_hidden_layer_{}'.format(_hidden_layers + 1 - _n)),
                                                  kernel_initializer=self.hyper_param.get('initializer')
                                                  )
                                             )
                               )
            else:
                self.model.add(LSTM(units=self.hyper_param.get('neurons_hidden_layer_{}'.format(_hidden_layers + 1 - _n)),
                                    activation=self.hyper_param.get('activation_hidden_layer_{}'.format(_hidden_layers + 1 - _n)),
                                    kernel_initializer=self.hyper_param.get('initializer')
                                    )
                               )
            self.model.add(Dropout(self.hyper_param.get('dropout_hidden_layer_{}'.format(_hidden_layers + 1 - _n))))
            _n -= 1
        self.model.add()
        return self

    def lstm_param(self) -> dict:
        """
        Generate and config Multi-Layer Perceptron using TensorFlow

        :return dict:
            Parameter config
        """
        _n: int = 3
        _b: int = 0
        _max_batch_size: int = int(self.n_cases / 4)
        while _b < _max_batch_size:
            if _n >= 3:
                _n += 1
            _b = max(HappyLearningUtils().geometric_progression(n=_n, ratio=2))
        _batch_size: List[int] = HappyLearningUtils().geometric_progression(n=_n, ratio=2)
        _network: dict = self.hidden_layer_template
        _network.update(hidden_layers=np.random.randint(low=2, high=10),
                        activation_input_layer=np.random.choice(a=self.activation),
                        activation_output_layer=np.random.choice(a=self.activation),
                        initializer=np.random.choice(a=self.initializer),
                        optimizer=np.random.choice(a=self.optimizer),
                        learning_rate=np.random.uniform(0.000005, 0.45),
                        loss_reg=np.random.choice(a=['mean_absolute_error', 'mean_absolute_percentage_error', 'mean_squared_error', 'mean_squared_logarithmic_error']),
                        loss_clf_bin=np.random.choice(a=['binary_crossentropy', 'hinge', 'squared_hinge']),
                        loss_clf_multi=np.random.choice(a=['categorical_crossentropy', 'kullback_leibler_divergence', 'sparse_categorical_crossentropy']),
                        batch_size=np.random.choice(a=_batch_size),
                        epochs=np.random.randint(low=10, high=50),
                        early_stopping=np.random.choice(a=[True, False]),
                        patience=np.random.randint(low=1, high=15),
                        validation_split=np.random.uniform(low=0.05, high=0.25)
                        )
        for l in range(0, _network.get('hidden_layers'), 1):
            _network.update({'neurons_hidden_layer_{}'.format(l + 1): np.random.choice(a=[2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]),
                             'activation_hidden_layer_{}'.format(l + 1): np.random.choice(a=self.activation),
                             'dropout_hidden_layer_{}'.format(l + 1): np.random.uniform(low=0.01, high=0.5)
                             })
        return _network

    def predict(self, x: np.array, probability: bool = False):
        pass

    def predict_proba(self, x: np.array) -> np.array:
        """
        Get prediction from Multi-Layer Perceptron

        :param x: np.array
            Test data set containing predictor features

        :return np.array:
            Predictions
        """
        return self.predict(x=x)

    def train(self, x: np.array, y: np.array):
        pass

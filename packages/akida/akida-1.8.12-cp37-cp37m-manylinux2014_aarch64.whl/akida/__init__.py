from .core import (Sparse, Dense, BackendType, ConvolutionMode, PoolingType,
                   LearningType, LayerType, TensorType, has_backend, backends,
                   NsocVersion, NPIdent, NPMapping, NPSpace, MeshMapper, Layer,
                   HWDevice, __version__)

from .layer import *
from .input_data import InputData
from .fully_connected import FullyConnected
from .convolutional import Convolutional
from .separable_convolutional import SeparableConvolutional
from .input_convolutional import InputConvolutional
from .concat import Concat
from .model import Model
from .layer_statistics import LayerStatistics
from .sparse import *
from .hw_device import *
from .inputs import coords_to_sparse, dense_to_sparse, packetize

Layer.__repr__ = layer_repr
Layer.set_variable = set_variable
Layer.get_variable = get_variable
Layer.get_variable_names = get_variable_names
Layer.get_learning_histogram = get_learning_histogram

Sparse.__repr__ = sparse_repr
Sparse.to_dense = Sparse.to_numpy

HWDevice.mapping_summary = mapping_summary

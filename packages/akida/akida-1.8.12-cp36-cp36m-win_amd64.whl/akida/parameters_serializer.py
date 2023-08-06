import akida.core as ak


def serialize_learning_type(learning_type):
    if learning_type == ak.LearningType.NoLearning:
        return "none"
    if learning_type == ak.LearningType.AkidaUnsupervised:
        return "akidaUnsupervised"
    raise ValueError(f"The layer type {learning_type} is unmanaged")


deserialize_dict = {
    'inputWidth': ['input_width'],
    'inputHeight': ['input_height'],
    'kernelWidth': ['kernel_width'],
    'kernelHeight': ['kernel_height'],
    'kernelSize': ['kernel_width', 'kernel_height'],
    'strideX': ['stride_x'],
    'strideY': ['stride_y'],
    'stride': ['stride_x', 'stride_y'],
    'poolingWidth': ['pooling_width'],
    'poolingHeight': ['pooling_height'],
    'poolingSize': ['pooling_width', 'pooling_width'],
    'poolStrideX': ['pooling_stride_x'],
    'poolStrideY': ['pooling_stride_y'],
    'numNeurons': ['num_neurons'],
    'weightsBits': ['weights_bits'],
    'numWeights': ['num_weights'],
    'numClasses': ['num_classes'],
    'initialPlasticity': ['initial_plasticity'],
    'learningCompetition': ['learning_competition'],
    'minPlasticity': ['min_plasticity'],
    'plasticityDecay': ['plasticity_decay'],
    'thresholdFire': ['threshold_fire'],
    'thresholdFireStep': ['threshold_fire_step'],
    'thresholdFireBits': ['threshold_fire_bits'],
    'inputFeatures': ['input_channels'],
    'paddingValue': ['padding_value'],
    'inputChannels': ['input_channels']
}


def _get_conv_mode(param):

    convolution_modes = {
        'valid': ak.ConvolutionMode.Valid,
        'same': ak.ConvolutionMode.Same,
        'full': ak.ConvolutionMode.Full
    }
    if param in convolution_modes:
        return convolution_modes[param]
    raise ValueError("'convolutionMode' should be 'valid', " "'same' or 'full'")


def _get_pooling_type(param):

    pooling_type = {
        'none': ak.PoolingType.NoPooling,
        'max': ak.PoolingType.Max,
        'average': ak.PoolingType.Average
    }
    if param in pooling_type:
        return pooling_type[param]
    raise ValueError("'poolingType' should be 'none', 'max' " "or 'average'")


def _get_learning_type(param):

    learning_type = {
        'none': ak.LearningType.NoLearning,
        'akidaUnsupervised': ak.LearningType.AkidaUnsupervised
    }
    if param in learning_type:
        return learning_type[param]
    raise ValueError("'learningType' should be 'none' or 'akidaUnsupervised'")


def deserialize_parameters(params):
    layer_type = str()
    params_dict = {}
    for item in params:
        if item == "layerType":
            layer_type = str(params[item])
        elif item in deserialize_dict:
            for new_item in deserialize_dict[item]:
                params_dict[new_item] = params[item]
        elif item == "convolutionMode":
            params_dict["convolution_mode"] = _get_conv_mode(params[item])
        elif item == "poolingType":
            params_dict["pooling_type"] = _get_pooling_type(params[item])
        elif item == "learningType":
            params_dict["learning_type"] = _get_learning_type(params[item])
        elif item == "activations":
            if params[item] == "none":
                params_dict["activations_enabled"] = False
            elif params[item] == "true":
                pass  # activations are enabled by default
            else:
                raise ValueError("'activations' should be 'none' or 'true'")
        else:
            raise ValueError("Unknown parameter: " + item + ": " +
                             str(params[item]))
    return layer_type, params_dict

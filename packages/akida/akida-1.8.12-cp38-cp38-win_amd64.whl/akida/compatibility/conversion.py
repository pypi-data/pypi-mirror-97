import copy
import numpy as np
import akida
from . import common


def _get_weights_params_identity(layer):
    """
    Creates an 'identity' convolutional layer parameters and its weights.
    """
    out_dims = layer.output_dims
    nb_chan = out_dims[2]
    dw_weights = np.zeros((3, 3, nb_chan, 1), dtype=np.int8)
    pw_weights = np.zeros((1, 1, nb_chan, nb_chan), dtype=np.int8)
    for i in range(nb_chan):
        dw_weights[1, 1, i, 0] = 1
        pw_weights[0, 0, i, i] = 1

    # create a layer to have default parameters
    identity_layer = akida.SeparableConvolutional(
        name=f"{layer.name}_pooling",
        kernel_width=3,
        kernel_height=3,
        num_neurons=nb_chan,
        threshold_fire=0,
        threshold_fire_bits=layer.parameters.threshold_fire_bits,
        threshold_fire_step=2**layer.parameters.threshold_fire_bits / 16)
    return copy.copy(identity_layer.parameters), dw_weights, pw_weights


def _copy_layer_variables(layer, copied_layer):
    for var in copied_layer.get_variable_names():
        layer.set_variable(var, copied_layer.get_variable(var))


def _copy_layer(model, layer):
    new_layer = akida.Layer(layer.parameters, layer.name)
    model.add(new_layer)
    if layer.learning:
        # Recompile model with layer parameters
        learn_params = {
            attr: getattr(layer.learning, attr)
            for attr in dir(layer.learning)
            if '__' not in attr and 'learning_type' not in attr
        }
        model.compile(**learn_params)
    _copy_layer_variables(new_layer, layer)


def _add_identity_cnp_after_max_pooling(model, layer):
    """
    Adds the layer and an identity CNP to the model
    """
    ident_params, ident_dw_weights, ident_pw_weights = _get_weights_params_identity(
        layer)
    identity_layer = akida.Layer(ident_params, f"{layer.name}_identity")
    model.add(identity_layer)
    identity_layer.set_variable("weights", ident_dw_weights)
    identity_layer.set_variable("weights_pw", ident_pw_weights)


def _cnp_max_pooling(layer):
    return layer.parameters.layer_type in [
        akida.LayerType.Convolutional, akida.LayerType.SeparableConvolutional
    ] and layer.parameters.pooling_type == akida.PoolingType.Max


def _cnp_sep_avg_pooling(layer):
    return (layer.parameters.layer_type
            == akida.LayerType.SeparableConvolutional and
            layer.parameters.pooling_type == akida.PoolingType.Average)


def _cnp_pooling_needs_identity_cnp(model, layer_index):
    """
    Returns True if the layer is CNP with max pooling not followed by another
    CNP, and we can add an identity CNP layer after it without altering result
    """
    result = False
    layer = model.get_layer(layer_index)
    if _cnp_max_pooling(layer):
        # if it is not the last layer, check the layer is not followed by
        # another cnp
        if layer_index != model.get_layer_count() - 1:
            next_layer = model.get_layer(layer_index + 1)
            if next_layer.parameters.layer_type not in [
                    akida.LayerType.Convolutional,
                    akida.LayerType.SeparableConvolutional
            ]:
                result = True
        # if it is the last layer, we can add an identity layer only if it has
        # activations enabled
        elif layer.parameters.activations_enabled:
            result = True
    return result


def _cnp_max_pooling_split(model, layer):
    """
    Splits a CNP with max pooling into 2 CNPs:
        - one performing the convolution
        - the other one performing the pooling
    """
    # 1st layer is the conv without pooling
    conv_params = copy.copy(layer.parameters)
    conv_params.pooling_type = akida.PoolingType.NoPooling
    conv_params.pooling_width = -1
    conv_params.pooling_height = -1
    conv_params.pooling_stride_x = -1
    conv_params.pooling_stride_y = -1
    layer_conv = akida.Layer(conv_params, f"{layer.name}_conv")
    model.add(layer_conv)
    _copy_layer_variables(layer_conv, layer)
    # 2nd layer is an identity conv with pooling
    pool_params, pool_dw_weights, pool_pw_weights = _get_weights_params_identity(
        layer)
    pool_params.pooling_type = akida.PoolingType.Max
    pool_params.pooling_width = layer.parameters.pooling_width
    pool_params.pooling_height = layer.parameters.pooling_height
    pool_params.pooling_stride_x = layer.parameters.pooling_stride_x
    pool_params.pooling_stride_y = layer.parameters.pooling_stride_y
    pool_layer = akida.Layer(pool_params, f"{layer.name}_pooling")
    model.add(pool_layer)
    pool_layer.set_variable("weights", pool_dw_weights)
    pool_layer.set_variable("weights_pw", pool_pw_weights)


def _cnp_sep_avg_pooling_add_dummy_neurons(model, layer):
    """
    Performs compatibility check on SeparableConvolutional with
    global average pooling:
        - Adds dummy neurons if filters number is not a multiple of 8
        - Adds 8 more dummy neurons to ensure all filters will be processed
    """
    # Check if layer needs more neurons to be a multiple of 8
    neurons_to_add = 8
    if layer.parameters.num_neurons % 8 != 0:
        neurons_to_add += 8 - (layer.parameters.num_neurons % 8)

    # Add new layer w/ layer parameters
    new_layer = akida.Layer(layer.parameters, layer.name)
    new_layer.parameters.num_neurons += neurons_to_add
    model.add(new_layer)
    # Copy variables and add dummy neurons
    for var in layer.get_variable_names():
        value = layer.get_variable(var)
        if var == 'threshold_fire':
            new_value = np.concatenate(
                (value, np.zeros(neurons_to_add, dtype=np.int32)))
        elif var == 'threshold_fire_step':
            new_value = np.concatenate(
                (value, np.ones(neurons_to_add, dtype=np.float32)))
        elif var == 'weights_pw':
            shape = value.shape
            new_shape = (shape[0], shape[1], shape[2], neurons_to_add)
            new_value = np.concatenate(
                (value, np.zeros(new_shape, dtype=np.int8)), axis=3)
        else:
            # Copy dw weigths
            new_value = value
        new_layer.set_variable(var, new_value)

    return neurons_to_add


def _cnp_sep_avg_pooling_clone_extend_layer(model, layer, channels_to_add):
    """
    Clone layer into the target model and append dummy channels
    """
    # Create new layer
    new_layer = akida.Layer(layer.parameters, layer.name)
    model.add(new_layer)
    for var in layer.get_variable_names():
        value = layer.get_variable(var)
        if var == 'weights':
            shape = value.shape
            new_shape = (shape[0], shape[1], channels_to_add, shape[3])
            if layer.parameters.layer_type == akida.LayerType.FullyConnected:
                compat_array = np.zeros(new_shape, dtype=np.int8)
            else:
                compat_array = np.ones(new_shape, dtype=np.int8)
            new_value = np.concatenate((value, compat_array), axis=2)
        elif var == 'weights_pw':
            shape = value.shape
            new_shape = (shape[0], shape[1], channels_to_add, shape[3])
            new_value = np.concatenate(
                (value, np.zeros(new_shape, dtype=np.int8)), axis=2)
        else:
            new_value = value
        new_layer.set_variable(var, new_value)


def create_from_model(model, nsoc_version=None):
    """Tries to create a HW compatible model from an incompatible one

    Tries to create a HW compatible model from an incompatible one, using SW
    workarounds for known limitations. It returns a converted model that is not
    guaranteed to be HW compatible, depending if workaround have been found.

    Args:
        model (:obj:`Model`): a Model object to convert
        nsoc_version (:obj:`NsocVersion`, optional): version of the NSoC

    Returns:
        :obj:`Model`: a new Model with no guarantee that it is HW compatible.
    """
    added_neurons = 0
    new_model = akida.Model(backend=model.backend.type)
    nb_layers = model.get_layer_count()
    for i in range(nb_layers):
        layer = model.get_layer(i)
        if _cnp_max_pooling(layer):
            # On hardware, any CNP with max pooling must be followed by a CNP
            # (to perform vertical pooling). If not, an identity CNP layer is
            # then added.
            # Moreover, on nsoc-v1, CNP with max pooling and negative thresholds
            # is not supported. To avoid this situation, any CNP with max
            # pooling (whatever the thresholds) is split into 2 CNPs:
            # - one performing the convolution
            # - the other one performing the pooling
            if (nsoc_version == akida.NsocVersion.v1 and
                    not common.cnp_is_identity(layer)):
                _cnp_max_pooling_split(new_model, layer)
            else:
                _copy_layer(new_model, layer)
            # If CNP has max pooling and is not followed by another CNP, we can
            # add an identity CNP layer
            if _cnp_pooling_needs_identity_cnp(model, i):
                _add_identity_cnp_after_max_pooling(new_model, layer)
            continue
        # If CNP has an average pooling on a SeparableConvolutional, it has to
        # be updated to add dummy neurons
        if nsoc_version == akida.NsocVersion.v1 and _cnp_sep_avg_pooling(layer):
            added_neurons = _cnp_sep_avg_pooling_add_dummy_neurons(
                new_model, layer)
            continue

        if added_neurons > 0:
            previous_layer = model.get_layer(i - 1)
            # Check if previous layer was a SeparableConvolutional with
            # global average pooling. If yes, current layer needs to be
            # updated to be aligned with the previous one.
            if _cnp_sep_avg_pooling(previous_layer):
                # Following layer has to be a SeparableConvolutional or a
                # FullyConnected. If not an error message will be raised.
                if layer.parameters.layer_type != akida.LayerType.Convolutional:
                    _cnp_sep_avg_pooling_clone_extend_layer(
                        new_model, layer, added_neurons)
                    continue
                raise TypeError(
                    'SeperableConvolutional with average pooling cannot be '
                    'followed by a Convolutional layer')

        # if no particular case is found, copy the layer into the new model
        _copy_layer(new_model, layer)

    return new_model

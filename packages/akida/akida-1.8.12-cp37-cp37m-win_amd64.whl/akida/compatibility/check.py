from akida.core import LayerType, PoolingType, NsocVersion, ConvolutionMode
import numpy as np


def summary_hardware_incompatibilities(model, nsoc_version=None):
    """Checks a model compatibility with hardware and prints a summary.

    This method performs parameters value checking for hardware
    compatibility and prints incompatibility messages when needed.

    Args:
        model (:obj:`Model`): the Model to check hardware compatibility
        nsoc_version (:obj:`NsocVersion`, optional): the NSoC version to check

    """
    incompatibilities = model_hardware_incompatibilities(model, nsoc_version)
    if incompatibilities:
        print("Hardware incompatibilities:")
    print("\n".join(incompatibilities))


def model_hardware_incompatibilities(model, nsoc_version=None):
    """Checks a model compatibility with hardware.

    This method performs parameters value checking for hardware
    compatibility and returns incompatibility messages when needed.

    Args:
        model (:obj:`Model`): the Model to check hardware compatibility
        nsoc_version (:obj:`NsocVersion`, optional): the NSoC version to check

    Returns:
        a list of str containing the hardware incompatibilities of the model.
        The list is empty if the model is hardware compatible.

    """
    incompatibilities = []
    for i in range(model.get_layer_count()):
        layer_incompatibility = layer_hardware_incompatibilities(
            model, i, nsoc_version)
        if layer_incompatibility:
            incompatibilities.append(layer_incompatibility)
    return incompatibilities


def layer_hardware_incompatibilities(model, layer_index, nsoc_version=None):
    """Checks a layer compatibility with hardware.

    This method performs parameters value checking for hardware
    compatibility and returns incompatibility messages when needed.

    Args:
        model (:obj:`Model`): the Model to check hardware compatibility
        layer_index (int): the layer index.
        nsoc_version (:obj:`NsocVersion`, optional): the NSoC version to check

    Returns:
        str: message containing hardware incompatibilities of the layer.
            Empty string if the layer is hardware compatible.

    """

    def full_message(layer_name, msg_list):

        if len(msg_list) > 0:
            return str("Layer " + layer_name + " is not compatible with "
                       "hardware: \n" + "\n".join(msg_list))
        return str()

    layer = model.get_layer(layer_index)
    hw_msg = []
    # inputData layer
    if layer.parameters.layer_type == LayerType.InputData:
        return str()

    if layer.parameters.threshold_fire_bits not in [1, 2, 4]:
        hw_msg.append("- unsupported threshold_fire_bits, supported "
                      "values are [1, 2, 4], currently at " +
                      str(layer.parameters.threshold_fire_bits))

    if layer.parameters.threshold_fire not in range(-2**19, 2**19):
        hw_msg.append("- unsupported threshold_fire, it must fit in 20 bits")

    # fullyConnected layer
    if layer.parameters.layer_type == LayerType.FullyConnected:
        hw_msg += _get_fully_connected_hw_incompatibilities(
            model, layer_index, nsoc_version)

    # inputConvolutional layer
    if layer.parameters.layer_type == LayerType.InputConvolutional:
        hw_msg += _get_input_conv_hw_incompatibilities(layer, nsoc_version)

    # convolutional layers
    elif (layer.parameters.layer_type
          in [LayerType.Convolutional, LayerType.SeparableConvolutional]):
        hw_msg += _get_conv_hw_incompatibilities(model, layer_index,
                                                 nsoc_version)

    return full_message(layer.name, hw_msg)


def _get_must_be_in_msg(name, param, supported_values):
    """Returns a warning message if the given parameter is not in the
    supported values.

    Args:
        name (str): name of the parameter to display in the message.
        param: parameter to check if valid
        supported_values (list): list of values that param must take.

    Returns:
        list: warning message embedded in a list. Empty if param is valid.
    """
    if param not in supported_values:
        return [f"- {name} must be in {supported_values}, currently at {param}"]
    return []


def _get_must_be_equal_msg(name1, param1, name2, param2):
    """Returns a warning message if the two parameters are not equal.

    Args:
        name1 (str): name of the first parameter to display in the message.
        param1: first parameter to compare with
        name2 (str): name of the second parameter to display in the message.
        param2: second parameter to compare with

    Returns:
        list: warning message embedded in a list. Empty if parameters are equal.
    """
    if param1 != param2:
        return [(f"- {name1} and {name2} must be equal, currently at "
                 f"{param1} and {param2}")]
    return []


def _get_fully_connected_hw_incompatibilities(model, layer_index, nsoc_version):
    """Checks a FullyConnected layer compatibility with hardware.

    This method performs parameters value checking for hardware
    compatibility and returns incompatibility messages when needed.

    Args:
        model (:obj:`Model`): the Model to check hardware compatibility
        layer_index (int): the layer index.
        nsoc_version (:obj:`NsocVersion`, optional): the NSoC version to check

    Returns:
        str: message containing hardware incompatibilities of the layer.
            Empty string if the layer is hardware compatible.
    """

    params = model.get_layer(layer_index).parameters
    hw_msg = []

    hw_msg += _get_must_be_in_msg('weights_bits', params.weights_bits,
                                  [1, 2, 3, 4])
    if layer_index > 0:
        previous_params = model.get_layer(layer_index - 1).parameters
        if "threshold_fire_bits" in dir(previous_params):
            # Allowed input bitwidth
            allowed_input_bw = [1, 2]
            if nsoc_version != NsocVersion.v1:
                allowed_input_bw.append(4)
            input_bw = previous_params.threshold_fire_bits
            if input_bw not in allowed_input_bw:
                hw_msg.append("- unsupported input dimensions. "
                              "threshold_fire_bits in previous layer "
                              "must be in " + str(allowed_input_bw) +
                              ", currently at " + str(input_bw))
    if nsoc_version == NsocVersion.v1:
        num_neurons = params.num_neurons
        if num_neurons < 3 and params.activations_enabled:
            hw_msg.append("- learn requires at least 3 neurons, "
                          "currently at " + str(num_neurons))
    return hw_msg


def _get_input_conv_hw_incompatibilities(layer, nsoc_version):
    """Checks a InputConvolutional layer compatibility with hardware.

    This method performs parameters value checking for hardware
    compatibility and returns incompatibility messages when needed.

    Args:
        layer (:obj:`Layer`): the Layer to check hardware compatibility
        nsoc_version (:obj:`NsocVersion`, optional): the NSoC version to check

    Returns:
        str: message containing hardware incompatibilities of the layer.
            Empty string if the layer is hardware compatible.
    """

    hw_msg = []
    p = layer.parameters

    # Define constraints (equality or "is an element of")
    must_be_equal_constraints = [('kernel_width', p.kernel_width,
                                  'kernel_height', p.kernel_height)]
    must_be_in_constraints = [('kernel_width', p.kernel_width, [3, 5, 7]),
                              ('stride_x', p.stride_x, [1, 2, 3]),
                              ('stride_y', p.stride_y, [1, 2, 3]),
                              ('convolution_mode', p.convolution_mode,
                               [ConvolutionMode.Same, ConvolutionMode.Valid])]

    pool_must_be_equal_constraints = [('pooling_stride_x', p.pooling_stride_x,
                                       'pooling_stride_y', p.pooling_stride_y)]
    pool_must_be_in_constraints = [('pooling_width', p.pooling_width, [1, 2]),
                                   ('pooling_height', p.pooling_height, [1, 2]),
                                   ('pooling_stride_x', p.pooling_stride_x, [2])
                                  ]

    def get_max_num_filters(kernel_size, rgb):
        if kernel_size not in (3, 5, 7):
            return 0

        if rgb:
            max_num_filters = {3: 192, 5: 64, 7: 32}
            return max_num_filters[kernel_size]

        max_num_filters = {3: 512, 5: 192, 7: 96}
        return max_num_filters[kernel_size]

    # Check kernel parameters for constraints
    for constraint in must_be_equal_constraints:
        hw_msg += _get_must_be_equal_msg(*constraint)
    for constraint in must_be_in_constraints:
        hw_msg += _get_must_be_in_msg(*constraint)

    # check number of neurons
    rgb = (p.input_channels == 3)
    max_num_filters = get_max_num_filters(p.kernel_width, rgb)
    if p.num_neurons < 1 or p.num_neurons > max_num_filters:
        hw_msg.append("- num_neurons should be set between 1 and " +
                      str(max_num_filters))
    # check input width limitations
    max_line_width = 256
    if p.input_width > max_line_width:
        hw_msg.append("- input width cannot be higher than " +
                      str(max_line_width))
    # NSOC-V1: valid conv with stride != 1 is not supported for now
    if (nsoc_version == NsocVersion.v1 and
            p.convolution_mode == ConvolutionMode.Valid and
        (p.stride_x > 1 or p.stride_y > 1)):
        hw_msg.append("- Convolution stride must be 1 when having "
                      "convolution mode 'VALID' for NsocVersion.v1")
    # Check pooling parameters
    if p.pooling_type == PoolingType.Max:
        for constraint in pool_must_be_equal_constraints:
            hw_msg += _get_must_be_equal_msg(*constraint)
        for constraint in pool_must_be_in_constraints:
            hw_msg += _get_must_be_in_msg(*constraint)
    elif p.pooling_type == PoolingType.Average:
        hw_msg.append("- average pooling_type not supported")
    # check if we want to enable wta and if wta is hw compatible
    if p.activations_enabled:
        wta = layer.get_variable('wta_groups')
        if not np.array_equal(wta, np.sort(wta)):
            hw_msg.append(" - Only consecutives neurons are allowed "
                          "in the same WTA group.")
    return hw_msg


def _get_conv_hw_incompatibilities(model, layer_index, nsoc_version):
    """Checks a Convolutional or SeparableConvolutional layer compatibility
    with hardware.

    This method performs parameters value checking for hardware
    compatibility and returns incompatibility messages when needed.

    Args:
        model (:obj:`Model`): the Model to check hardware compatibility
        layer_index (int): the layer index.
        nsoc_version (:obj:`NsocVersion`, optional): the NSoC version to check

    Returns:
        str: message containing hardware incompatibilities of the layer.
            Empty string if the layer is hardware compatible.
    """

    layer = model.get_layer(layer_index)
    p = layer.parameters
    hw_msg = []

    # Define constraints (equality or "is an element of")
    must_be_equal_constraints = [('kernel_width', p.kernel_width,
                                  'kernel_height', p.kernel_height)]

    must_be_in_constraints = [('stride_x', p.stride_x, [1]),
                              ('stride_y', p.stride_y, [1]),
                              ('convolution_mode', p.convolution_mode,
                               [ConvolutionMode.Same])]
    if p.layer_type == LayerType.Convolutional:
        must_be_in_constraints += [('kernel_width', p.kernel_width,
                                    [1, 3, 5, 7]),
                                   ('weights_bits', p.weights_bits, [1, 2])]
    elif p.layer_type == LayerType.SeparableConvolutional:
        must_be_in_constraints += [('kernel_width', p.kernel_width, [3, 5, 7]),
                                   ('weights_bits', p.weights_bits, [2, 4])]

    pool_must_be_equal_constraints = [('pooling_width', p.pooling_width,
                                       'pooling_height', p.pooling_height),
                                      ('pooling_stride_x', p.pooling_stride_x,
                                       'pooling_stride_y', p.pooling_stride_y)]
    pool_must_be_in_constraints = [('pooling_width', p.pooling_width, [2, 3])]

    # Check kernel parameters for constraints
    for constraint in must_be_equal_constraints:
        hw_msg += _get_must_be_equal_msg(*constraint)
    for constraint in must_be_in_constraints:
        hw_msg += _get_must_be_in_msg(*constraint)

    if p.pooling_type == PoolingType.Max:
        # Max pooling forbidden if it is not followed by another NP
        layers_vert_pool = [
            LayerType.Convolutional, LayerType.SeparableConvolutional
        ]
        if nsoc_version != NsocVersion.v1:
            layers_vert_pool.append(LayerType.FullyConnected)
        if (layer_index == model.get_layer_count() - 1 or
                model.get_layer(layer_index + 1).parameters.layer_type
                not in layers_vert_pool):
            types = [str(lt).split('.')[-1] for lt in layers_vert_pool]
            types_str = ", ".join(types)
            hw_msg.append("- max pooling on convolutional or separable"
                          " convolutional layer must be followed by"
                          " another layer of one of these types: " + types_str)
        # Check max pooling parameters
        for constraint in pool_must_be_equal_constraints:
            hw_msg += _get_must_be_equal_msg(*constraint)
        for constraint in pool_must_be_in_constraints:
            hw_msg += _get_must_be_in_msg(*constraint)
        if (p.pooling_width in [2, 3] and
                p.pooling_stride_x not in range(1, p.pooling_width + 1)):
            pw = p.pooling_width
            hw_msg.append(
                f"- pooling_stride_x must be in {[*range(1, pw + 1)]} for "
                f"{pw}x{pw} pooling, currently at {p.pooling_stride_x}")
        if p.pooling_width > max(layer.input_dims[:2]):
            hw_msg.append(
                "- pooling size must be lower than or equal to input dimensions"
            )
    elif p.pooling_type == PoolingType.Average:
        hw_msg += _get_avg_pooling_incompatibilities(layer, nsoc_version)
    return hw_msg


def _get_avg_pooling_incompatibilities(layer, nsoc_version):
    """Checks global average pooling compatibility with hardware.

    A global average pooling can only be present in a Convolutional or
    SeparableConvolutional layer. This method performs parameters value
    checking for hardware compatibility and returns incompatibility messages
    when needed.

    Args:
        layer (:obj:`Layer`): the Layer to check global average pooling
            hardware compatibility
        nsoc_version (:obj:`NsocVersion`, optional): the NSoC version to check

    Returns:
        str: message containing hardware incompatibilities of the layer.
            Empty string if the layer is hardware compatible.
    """
    hw_msg = []

    p = layer.parameters
    if p.pooling_width != -1 and p.pooling_height != -1:
        hw_msg.append("- only global average pooling is supported:"
                      " pooling_width and pooling height must be "
                      "set to -1 (default)")
    if nsoc_version == NsocVersion.v1 and p.num_neurons % 8 != 0:
        hw_msg.append("- with average pooling, number of neurons must"
                      " be a multiple of 8")
    if layer.input_dims[0] > 32:
        hw_msg.append("- with average pooling, the maximum input width"
                      " is 32")
    return hw_msg

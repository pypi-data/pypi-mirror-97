from copy import copy
import os
import re
import warnings
import yaml
import numpy as np

from .core import (Sparse, Dense, BackendType, ModelBase, Layer, LayerType,
                   PoolingType, NsocVersion)
from .parameters_serializer import deserialize_parameters
from .layer_statistics import LayerStatistics
from .compatibility import check, common
from .input_data import InputData
from .fully_connected import FullyConnected
from .convolutional import Convolutional
from .separable_convolutional import SeparableConvolutional
from .input_convolutional import InputConvolutional


# Private utility functions
def _copy_layer_variables(layer, copied_layer):
    for var in copied_layer.get_variable_names():
        layer.set_variable(var, copied_layer.get_variable(var))


def _copy_layer(model, layer):
    new_layer = Layer(layer.parameters, layer.name)
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


def _get_sequences(model):
    """Return a list of the model layer sequences

       Each sequence is a tuple of layers
    """
    # Build a dict of <keys, layer sequences>. Each entry corresponds to a
    # tuple of layers ending at the layer specified by the key name
    sequences = {}
    for layer in model.layers:
        # We ignore InputData layers
        if layer.parameters.layer_type == LayerType.InputData:
            continue
        if len(layer.inbounds) == 1 and layer.inbounds[0].name in sequences:
            # This layer belongs to an existing sequence
            inbound_name = layer.inbounds[0].name
            # Create a new sequence tuple from the existing sequence
            sequences[layer.name] = sequences[inbound_name] + (layer,)
            # Clear the existing sequence
            del sequences[inbound_name]
        else:
            # We haven't encountered an ancestor for that layer, or it has
            # multiple ancestors: start a new sequence
            sequences[layer.name] = (layer,)
    # Return the list of unique values in the sequence dictionary
    return set(sequences.values())


def _get_metrics(model, sequence, metrics):
    """Return the metrics for a specific sequence
    """
    if len(model.metrics.names) == 0:
        return None
    # Sequence metrics are identified by the first and last layers
    prefix = sequence[0].name + "/" + sequence[-1].name
    # Filter-out metrics not corresponding to that sequence
    seq_metrics_names = [name for name in model.metrics.names if prefix in name]
    # Get the metrics matching the specified name for the sequence
    metrics_names = [name for name in seq_metrics_names if metrics in name]
    if len(metrics_names) > 0:
        return model.metrics[metrics_names[0]]
    return None


class Model(ModelBase):
    """An Akida neural ``Model``, represented as a hierarchy of layers.

    The ``Model`` class is the main interface to Akida and allows to creates an
    empty ``Model``, a ``Model`` template from a YAML file, or a full ``Model``
    from a serialized file.

    It provides methods to instantiate, train, test and save models.

    Args:
        filename (str, optional): path of the YAML file containing the model
            architecture, or a serialized Model.
            If None, an empty sequential model will be created, or filled
            with the layers in the layers parameter.
        serialized_buffer (bytes, optional): binary buffer containing a
            serialized Model.
        layers (:obj:`list`, optional): list of layers that will be copied
            to the new model. If the list does not start with an input layer,
            it will be added automatically.
        backend (:obj:`BackendType`, optional): backend to run the model on.

    """

    def __init__(self,
                 filename=None,
                 serialized_buffer=None,
                 layers=None,
                 backend=BackendType.Software):
        try:
            if (int(filename is not None) + int(serialized_buffer is not None) +
                    int(layers is not None) > 1):
                raise ValueError("filename, serialized_buffer and layer list "
                                 "should not be passed at the same time")
            if filename is not None:
                # get file extension
                extension = os.path.splitext(filename)[1].lower()
                if extension in ('.yml', '.yaml'):
                    ModelBase.__init__(self, backend)
                    self._build_model(filename)
                else:
                    with open(filename, "rb") as f:
                        serialized_buffer = f.read()

            if serialized_buffer is not None:
                ModelBase.__init__(self, serialized_buffer, backend)
            else:
                ModelBase.__init__(self, backend)
                if layers is not None:
                    if not isinstance(layers, list):
                        raise ValueError("layers should be a list of layers")
                    if any(not isinstance(l, Layer) for l in layers):
                        raise ValueError("layers should only contain a list of"
                                         " layers")
                    input_layer_types = (LayerType.InputConvolutional,
                                         LayerType.InputData)
                    ltype = layers[0].parameters.layer_type
                    # Add an InputData layer
                    if ltype not in input_layer_types:
                        input_dims = layers[0].input_dims
                        input_data = InputData(*input_dims,
                                               input_bits=layers[0].input_bits)
                        self.add(input_data)
                    for layer in layers:
                        _copy_layer(self, layer)
        except:
            self = None
            raise

    def __repr__(self):
        out_dims = self.output_dims if self.get_layer_count() else []
        data = "<akida.Model, layer_count=" + str(self.get_layer_count())
        data += ", output_dims=" + str(out_dims)
        data += ", backend_type=" + str(self.backend.type) + ">"
        return data

    def get_statistics(self):
        """Get statistics by layer for this network.

        Returns:
            a dictionary of obj:`LayerStatistics` indexed by layer_name.

        """
        # Filter-out InputData layer
        layers = [
            layer for layer in list(self.layers)
            if layer.parameters.layer_type != LayerType.InputData
        ]
        # Initialize empty statistics per layer
        layers_stats = {layer.name: LayerStatistics(layer) for layer in layers}
        if len(self.metrics.names) == 0:
            # No metrics available: just return empty statistics
            return layers_stats
        # Extract model layer sequences
        sequences = _get_sequences(self)
        for sequence in sequences:
            # Get activations and inference metrics for the sequence
            inference = _get_metrics(self, sequence, "inference")
            nb_activations = _get_metrics(self, sequence, "activations")
            if inference is None or nb_activations is None:
                # This is definitely not expected, but silently skip this
                # sequence because other sequences may have valid metrics
                continue
            # Get the number of samples evaluated for that sequence
            nb_samples = inference[0]
            if nb_activations.shape[0] == 1:
                # A single activations value corresponds to the last layer
                layer = sequence[-1]
                layer_activations = nb_activations[0]
                layers_stats[layer.name] = LayerStatistics(
                    layer, nb_samples, layer_activations)
            else:
                # Each activations value correspond to a sequence layer
                for i, layer in enumerate(sequence):
                    layer_activations = nb_activations[i]
                    layers_stats[layer.name] = LayerStatistics(
                        layer, nb_samples, layer_activations)
        return layers_stats

    def _build_model(self, filename):
        """Builds a model from a YAML description file of the layers.

        Args:
            filename (str): path of the YAML file containing the model
                architecture, or a serialized Model.

        """
        # test whether the yml file can be found
        if not os.path.isfile(filename):
            raise ValueError("The ymlfile ({}) could not be found, "
                             "instance not initialised".format(filename))
        # load the file
        yaml_content = yaml.load(open(filename), Loader=yaml.FullLoader)

        if "Layers" not in yaml_content:
            raise ValueError(
                "Invalid model configuration: missing 'Layers' section.")

        layers = yaml_content["Layers"]
        if len(layers) == 0:
            raise ValueError("Empty model configuration.")

        # build and add layers to the model
        for layer_description in layers:
            name = layer_description["Name"]

            # deserialize YAML into a kwargs dict for the layer
            if "Parameters" not in layer_description:
                raise ValueError("Invalid model configuration: "
                                 "missing 'Parameters' section in layer " +
                                 name)
            layer_type, params_dict = deserialize_parameters(
                layer_description["Parameters"])

            # create a layer object from the dict
            akida_layer_types = {
                'inputData': InputData,
                'inputConvolutional': InputConvolutional,
                'fullyConnected': FullyConnected,
                'convolutional': Convolutional,
                'separableConvolutional': SeparableConvolutional,
            }
            layer = None
            if layer_type in akida_layer_types:
                layer = akida_layer_types[layer_type](name=name, **params_dict)
            elif layer_type == "depthwiseConvolutional":
                warnings.warn("depthwiseConvolutional layer name is deprecated,"
                              " please use separableConvolutional instead.")
                layer = SeparableConvolutional(name=name, **params_dict)
            elif layer_type == str():
                raise ValueError("Invalid model configuration: missing"
                                 " 'layerType' parameter in layer " + name)
            else:
                raise ValueError("Invalid model configuration, unknown"
                                 " layerType " + layer_type + " in layer " +
                                 name)

            # add the layer
            self.add(layer)

    def _check_constraints(self):
        if self.backend.type == BackendType.Hardware \
            and self.backend.get_device().nsoc_version == NsocVersion.v1:
            for layer in iter(self.layers):
                if layer.parameters.layer_type in [
                        LayerType.Convolutional,
                        LayerType.SeparableConvolutional
                ]:
                    if layer.parameters.pooling_type == PoolingType.Average:
                        warnings.warn("With average pooling, the last 8 filters"
                                      " are ignored.")
                    if common.cnp_is_identity(layer):
                        warnings.warn("1x1 identity layer might produce wrong"
                                      " results if the input is too sparse, on"
                                      " NSoC V1.")

    def predict(self, inputs, num_classes=None):
        """Returns the model class predictions.

        Forwards an input tensor (images or events) through the model
        and compute predictions based on the neuron id.
        If the number of output neurons is greater than the number of classes,
        the neurons are automatically assigned to a class by dividing their id
        by the number of classes.

        The expected input tensor dimensions are:

        - n, representing the number of frames or samples,
        - w, representing the width,
        - h, representing the height,
        - c, representing the channel, or more generally the feature.

        If the inputs are events, the input shape must be (n, w, h, c), but if
        the inputs are images (numpy array), their shape must be (n, h, w, c).

        Note: only grayscale (c=1) or RGB (c=3) images (arrays) are supported.

        Note that the predictions are based on the activation values of the last
        layer: for most use cases, you may want to disable activations for that
        layer (ie setting ``activations_enabled=False``) to get a better
        accuracy.

        Args:
            inputs (:obj:`Sparse`,`numpy.ndarray`): a (n, w, h, c) Sparse or a
                (n, h, w, c) numpy.ndarray
            num_classes (int, optional): optional parameter (defaults to the
                number of neurons in the last layer).

        Returns:
            :obj:`numpy.ndarray`: an array of shape (n).

        Raises:
            TypeError: if the input doesn't have the correct type
                (Sparse, numpy.ndarray).

        """
        self._check_constraints()

        if num_classes is None:
            num_classes = self.output_dims[2]

        if isinstance(inputs, np.ndarray):
            if inputs.flags['C_CONTIGUOUS']:
                dense = Dense(inputs)
            else:
                dense = Dense(np.ascontiguousarray(inputs))
            labels = super().predict(dense, num_classes)
        elif isinstance(inputs, Sparse):
            labels = super().predict(inputs, num_classes)
        else:
            raise TypeError("predict expects Sparse or numpy array as input")
        return labels

    def fit(self, inputs, input_labels=None):
        """Trains a set of images or events through the model.

        Trains the model with the specified input tensor.

        The expected input tensor dimensions are:

        - n, representing the number of frames or samples,
        - w, representing the width,
        - h, representing the height,
        - c, representing the channel, or more generally the feature.

        If the inputs are events, the input shape must be (n, w, h, c), but if
        the inputs are images (numpy array), their shape must be (n, h, w, c).

        Note: only grayscale (c=1) or RGB (c=3) images (arrays) are supported.

        If activations are enabled for the last layer, the output tensor is a
        Sparse object.

        If activations are disabled for the last layer, the output tensor is a
        numpy array.

        The output tensor shape is always (n, out_w, out_h, out_c).

        Args:
            inputs (:obj:`Sparse`,`numpy.ndarray`): a (n, w, h, c) Sparse or a
                (n, h, w, c) numpy.ndarray
            input_labels (list(int), optional): input labels.
                Must have one label per input, or a single label for all inputs.
                If a label exceeds the defined number of classes, the input will
                be discarded. (Default value = None).

        Returns:
            a numpy array of shape (n, out_w, out_h, out_c).

        Raises:
            TypeError: if the input doesn't have the correct type
                (Sparse, numpy.ndarray).
            ValueError: if the input doesn't match the required shape,
                format, etc.

        """
        self._check_constraints()

        if input_labels is None:
            input_labels = []
        elif isinstance(input_labels, (int, np.integer)):
            input_labels = [input_labels]
        elif isinstance(input_labels, (list, np.ndarray)):
            if any(not isinstance(x, (int, np.integer)) for x in input_labels):
                raise TypeError("fit expects integer as labels")
        if isinstance(inputs, Sparse):
            outputs = super().fit(inputs, input_labels)
        elif isinstance(inputs, np.ndarray):
            if inputs.flags['C_CONTIGUOUS']:
                dense = Dense(inputs)
            else:
                dense = Dense(np.ascontiguousarray(inputs))
            outputs = super().fit(dense, input_labels)
        else:
            raise TypeError("fit expects Sparse or numpy array as input")
        return outputs.to_numpy()

    def forward(self, inputs):
        """Forwards a set of images or events through the model.

        Forwards an input tensor through the model and returns an output tensor.

        The expected input tensor dimensions are:

        - n, representing the number of frames or samples,
        - w, representing the width,
        - h, representing the height,
        - c, representing the channel, or more generally the feature.

        If the inputs are events, the input shape must be (n, w, h, c), but if
        the inputs are images (numpy array), their shape must be (n, h, w, c).

        Note: only grayscale (c=1) or RGB (c=3) images (arrays) are supported.

        If activations are enabled for the last layer, the output tensor is a
        Sparse object.

        If activations are disabled for the last layer, the output tensor is a
        numpy array.

        The output tensor shape is always (n, out_w, out_h, out_c).

        Args:
            inputs (:obj:`Sparse`,`numpy.ndarray`): a (n, w, h, c) Sparse or a
                (n, h, w, c) numpy.ndarray

        Returns:
            a numpy array of shape (n, out_w, out_h, out_c).

        Raises:
            TypeError: if the inputs doesn't have the correct type
                (Sparse, numpy.ndarray).
            ValueError: if the inputs doesn't match the required shape,
                format, etc.

        """
        self._check_constraints()

        if isinstance(inputs, Sparse):
            outputs = super().forward(inputs)
        elif isinstance(inputs, np.ndarray):
            if inputs.flags['C_CONTIGUOUS']:
                dense = Dense(inputs)
            else:
                dense = Dense(np.ascontiguousarray(inputs))
            outputs = super().forward(dense)
        else:
            raise TypeError("forward expects Sparse or numpy array as input")
        return outputs.to_numpy()

    def evaluate(self, inputs):
        """Evaluates a set of images or events through the model.

        Forwards an input tensor through the model and returns a float array.

        It applies ONLY to models without an activation on the last layer.
        The output values are obtained from the model discrete potentials by
        applying a shift and a scale.

        The expected input tensor dimensions are:

        - n, representing the number of frames or samples,
        - w, representing the width,
        - h, representing the height,
        - c, representing the channel, or more generally the feature.

        If the inputs are events, the input shape must be (n, w, h, c), but if
        the inputs are images (numpy array), their shape must be (n, h, w, c).

        Note: only grayscale (c=1) or RGB (c=3) images (arrays) are supported.

        The output tensor shape is always (n, out_w, out_h, out_c).

        Args:
            inputs (:obj:`Sparse`,`numpy.ndarray`): a (n, w, h, c) Sparse or a
                (n, h, w, c) numpy.ndarray

        Returns:
           :obj:`numpy.ndarray`: a float array of shape (n, w, h, c).

        Raises:
            TypeError: if the input doesn't have the correct type
                (Sparse, numpy.ndarray).
            RuntimeError: if the model last layer has an activation.
            ValueError: if the input doesn't match the required shape,
                format, or if the model only has an InputData layer.

        """
        self._check_constraints()

        if isinstance(inputs, Sparse):
            outputs = super().evaluate(inputs)
        elif isinstance(inputs, np.ndarray):
            if inputs.flags['C_CONTIGUOUS']:
                dense = Dense(inputs)
            else:
                dense = Dense(np.ascontiguousarray(inputs))
            outputs = super().evaluate(dense)
        else:
            raise TypeError("forward expects Sparse or numpy array as input")
        return outputs.to_numpy()

    def summary(self):
        """Prints a string summary of the model.

        This method prints a summary of the model with details for every layer:

        - name and type in the first column
        - output shape
        - kernel shape

        If there is any layer with unsupervised learning enabled, it will list
        them, with these details:

        - name of layer
        - number of incoming connections
        - number of weights per neuron

        It will also tell the input shape, the backend type and version.
        """
        layers = self.layers
        layer_count = len(layers)

        def _basic_summary():
            # Prepare headers
            headers = ['Layer (type)', 'Output shape', 'Kernel shape']
            # prepare an empty table
            table = [headers]
            for l in iter(layers):
                # layer name (type)
                layer_type = l.parameters.layer_type
                name_and_type = f"{l.name} ({str(layer_type).split('.')[-1]})"
                # kernel shape
                if "weights" in l.get_variable_names():
                    kernel_shape = l.get_variable("weights").shape
                    if layer_type == LayerType.SeparableConvolutional:
                        kernel_pw_shape = l.get_variable("weights_pw").shape
                        kernel_shape = f"{kernel_shape}, {kernel_pw_shape}"
                else:
                    kernel_shape = "N/A"
                # Prepare row and add it
                row = [name_and_type, str(l.output_dims), str(kernel_shape)]
                table.append(row)
            print_table(table, "Model Summary")

        def _learning_summary():
            learning_layers = [l for l in iter(layers) if l.learning]
            # If no learning layers, skip this summary and return
            if not learning_layers:
                return
            # Prepare headers
            headers = ["Learning Layer", "# Input Conn.", "# Weights"]
            table = [headers]
            for layer in learning_layers:
                name = layer.name
                # Input connections is the product of input dims
                input_connections = np.prod(layer.input_dims)
                # Num non zero weights per neuron (counted on fist neuron)
                weights = layer.get_variable("weights")
                incoming_conn = np.count_nonzero(weights[:, :, :, 0])
                # Prepare row and add it
                row = [name, str(input_connections), incoming_conn]
                table.append(row)
            print()
            print_table(table, "Learning Summary")

        # Print formatted table
        _basic_summary()
        # Print learning summary
        _learning_summary()
        # Format and print input shape
        input_dims = layers[0].input_dims if layer_count > 0 else "N/A"
        input_dims = re.sub(r'[\[\]]', '', str(input_dims))
        print(f"Input shape: {input_dims}")
        # Print backend info
        print(f"Backend type: {str(self.backend.type).split('.')[-1]}" +
              f" - {self.backend.version}")
        print()
        # Print hardware incompatibilities, if any found
        check.summary_hardware_incompatibilities(self)

    def add_classes(self, num_add_classes):
        """Adds classes to the last layer of the model.

        A model with a compiled last layer is ready to learn using the Akida
        built-in learning algorithm. This function allows to add new classes
        (i.e. new neurons) to the last layer, keeping the previously learned
        neurons.

        Args:
            num_add_classes (int): number of classes to add to the last layer

        Raises:
            RuntimeError: if the last layer is not compiled
        """
        # Get current layer's parameters and variables
        layer = self.get_layer(self.get_layer_count() - 1)
        params = copy(layer.parameters)
        old_num_neurons = params.num_neurons
        learn_params = {
            attr: getattr(layer.learning, attr)
            for attr in dir(layer.learning)
            if not '__' in attr and not 'learning_type' in attr
        }
        if not learn_params:
            raise RuntimeError("'add_classes' function must be called when "
                               "the last layer of the model is compiled.")
        num_nrns_per_class = old_num_neurons // learn_params['num_classes']
        var_names = layer.get_variable_names()
        variables = {var: layer.get_variable(var) for var in var_names}

        # Update parameters for new future layer
        learn_params['num_classes'] += num_add_classes
        params.num_neurons = learn_params['num_classes'] * num_nrns_per_class

        # Replace last layer with new one
        self.pop_layer()
        new_layer = Layer(params, layer.name)
        self.add(new_layer)
        self.compile(**learn_params)

        # Fill variables with previous values
        for var in var_names:
            new_var = new_layer.get_variable(var)
            new_var[..., :old_num_neurons] = variables[var]
            new_layer.set_variable(var, new_var)


def print_table(table, title):
    # Convert to np.array
    to_str = np.vectorize(str)
    table = to_str(table)
    # get column lengths
    str_len_f = np.vectorize(lambda cell: len(str(cell)))
    str_lens = np.amax(str_len_f(table), 0)
    line_len = np.sum(str_lens)
    # Prepare format rows
    size_formats = np.vectorize(lambda cell: f"{{:{cell}.{cell}}}")
    format_strings = size_formats(str_lens)
    format_row = "  ".join(format_strings)
    # Generate separators
    separator_len = line_len + 2 * len(table[0])
    separator = "_" * separator_len
    double_separator = "=" * separator_len

    # Print header
    center_format = f"{{:^{separator_len}}}"
    print(center_format.format(title))
    print(separator)
    print(format_row.format(*table[0]))
    print(double_separator)
    # Print body
    for row in table[1:, :]:
        print(format_row.format(*row))
        print(separator)

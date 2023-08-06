import numpy as np
from .core import LayerType


class LayerStatistics():
    """Container attached to an akida.Model and an akida.Layer that allows to
        retrieve layer statistics:
        (average input and output sparsity, number of operations, number of
        possible spikes, row_sparsity).

    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, layer, nb_samples=0, nb_activations=0):
        self._layer = layer
        self._nb_samples = nb_samples
        self._nb_activations = nb_activations

    def __repr__(self):
        data = "{layer: " + self._layer.name + ", layer_type: " + \
            str(self._layer.parameters.layer_type).split(".")[-1]
        data += ", output_sparsity: "
        if self.output_sparsity:
            data += format(self.output_sparsity, ".2f")
        else:
            data += "N/A"
        data += "}"
        return data

    def __str__(self):

        def str_column_data(data, col_width=20):
            if len(data) > col_width - 1:
                formatted_data = data[:col_width - 1] + ' '
            else:
                formatted_data = data + ' ' * (col_width - len(data))

            return formatted_data

        data = str_column_data("Layer (type)", 30)
        data += str_column_data("output sparsity")
        data += "\n"
        layer_type = str(self._layer.parameters.layer_type).split(".")[-1]
        data += str_column_data(f"{self._layer.name} ({layer_type})", 30)
        if self.output_sparsity:
            data += str_column_data(format(self.output_sparsity, ".2f"))
        else:
            data += "N/A"
        return data

    @property
    def possible_spikes(self):
        """Get possible spikes for the layer.

        Returns:
            int: the possible spike amount value.

        """
        return np.prod(self._layer.output_dims)

    @property
    def row_sparsity(self):
        """Get kernel row sparsity.

        Compute row sparsity for kernel weights.

        Returns:
          float: the kernel row sparsity value.

        """
        if (self._layer.parameters.layer_type == LayerType.Convolutional or
                self._layer.parameters.layer_type
                == LayerType.SeparableConvolutional):
            row_sparsity = 0.0
            weights = self._layer.get_variable("weights")
            wshape = weights.shape
            if np.prod(wshape) == 0:
                raise ValueError("Exception in LayerStatistics: weights shape "
                                 "have null dimension: " + str(wshape))

            # Going through all line blocks
            for f in range(wshape[3]):
                for c in range(wshape[2]):
                    for y in range(wshape[1]):
                        if np.array_equal(weights[:, y, c, f],
                                          np.zeros((wshape[0]))):
                            # Counting when line block is full of zero.
                            row_sparsity += 1
            return row_sparsity / (wshape[1] * wshape[2] * wshape[3])

        return None

    @property
    def output_sparsity(self):
        """Get average output sparsity for the layer.

        Returns:
            float: the average output sparsity value.

        """
        if self._nb_samples == 0:
            return None
        activations_per_sample = self._nb_activations / self._nb_samples
        return 1 - activations_per_sample / self.possible_spikes

    @property
    def layer_name(self):
        """Get the name of the corresponding layer.

        Returns:
            str: the layer name.

        """
        return self._layer.name

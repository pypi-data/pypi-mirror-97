from .core import LayerType
from .model import print_table


def mapping_summary(self, model):
    """Prints a string summary of how the model is mapped.

    This method prints a mapping summary of the model:

    For each layer, if it is mapped on HW:
       - gives the number of NPs used
       - list NPs with spatial dimensions and neurons they are responsible for

    If a layer is mapped on SW, it will only show input dimensions and neurons
    """
    mapping = self.get_mapping(model)

    # Prepare headers
    headers = [
        'Layer (type)', 'NP (Col,Row,Id)', 'Input size [x, y, shape]',
        '# Neurons'
    ]
    # prepare an empty table
    table = [headers]
    layers = model.layers
    for l in layers:
        # layer name (type)
        layer_type = l.parameters.layer_type
        name_and_type = f"{l.name} ({str(layer_type).split('.')[-1]})"
        input_total = f"Total = {l.input_dims}"
        if "weights" in l.get_variable_names():
            if layer_type == LayerType.SeparableConvolutional:
                weight_shape = l.get_variable("weights_pw").shape
            else:
                weight_shape = l.get_variable("weights").shape
            nb_neurons_total = f"Total = {weight_shape[3]}"
        else:
            nb_neurons_total = "N/A"

        if l in mapping:
            # HRC is a special case, because it uses a separate module
            if layer_type == LayerType.InputConvolutional:
                table.append(
                    [name_and_type, "HRC", input_total, nb_neurons_total])
            else:
                # Print NPs informations
                nb_nps = len(mapping[l])
                str_nb_nps = f"{nb_nps} NP"
                # Handle plural
                if nb_nps > 1:
                    str_nb_nps += "s"

                table.append(
                    [name_and_type, str_nb_nps, input_total, nb_neurons_total])
                for np_mapping in mapping[l]:
                    np_id = f"({np_mapping.np.col},{np_mapping.np.row},{np_mapping.np.id})"
                    np_space = np_mapping.input_internal
                    np_input = f"[{np_space.x, np_space.y, np_space.shape}]"
                    row = [" ", np_id, np_input, str(np_mapping.num_neurons)]
                    table.append(row)
        else:
            # Layer is not HW mapped
            table.append(
                [name_and_type, "Mapped in SW", input_total, nb_neurons_total])

    print_table(table, "Mapping Summary")

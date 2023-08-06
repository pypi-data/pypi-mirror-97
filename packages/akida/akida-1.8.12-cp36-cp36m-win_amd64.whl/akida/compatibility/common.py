import numpy as np


def cnp_is_identity(layer):
    """
    Determine if a CNP is an identity one.
    An identity layer has the following features:
     - kernel 1x1
     - number of neurons equal to number of channels
     - have weight set to 1 on the neuron corresponding to the same channel
     - having threshold fire set to 0, and step set to 1
    """
    # checking weights equality with np.identity is enough to check first 3 points.
    weights = layer.get_variable("weights")
    nb_chan = weights.shape[2]
    result = np.array_equal(
        np.identity(nb_chan, dtype=np.int8).reshape(1, 1, nb_chan, nb_chan),
        weights)
    th_fire = layer.get_variable("threshold_fire")
    result = result and np.count_nonzero(th_fire) == 0
    th_step = layer.get_variable("threshold_fire_step")
    result = result and (th_step == 1.).all()

    return result

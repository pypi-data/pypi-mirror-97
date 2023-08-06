import numpy as np
from .core import Sparse


def coords_to_sparse(coords, shape):
    """Converts a list of 3D or 4D event coordinates to a Sparse input.

    Event coordinates should contain:

    - an optional index corresponding to the frame or sample,
    - a first spatial coordinate (typically x, the pixel column),
    - a second spatial coordinate (typically y, the pixel line),
    - a feature index representing the spike (starting from index zero)

    The output Sparse will have a shape of (n, w, h, c), where:

    - n is the number of frames or samples,
    - w is the size of the first spatial dimension (typically, the width),
    - h is the size of the second spatial dimension (typically, the height),
    - c is the size of the last dimension (typically, the channel or feature).

    Event values are automatically set to 1.

    Args:
      coords (:obj:`numpy.ndarray`): a (n, 3) or (n, 4) array of coordinates.
      shape (:obj:`tuple[int]`): the 3 or 4 dimensions of the input space.

    Returns:
      :obj:`Sparse`: the events corresponding to the specified coordinates.

    """
    if len(coords.shape) != 2:
        raise ValueError("Coordinates array must have a (n,3) or (n,4) shape")
    if coords.shape[1] < 3 or coords.shape[1] > 4:
        raise ValueError("Input coordinates must have 3 or 4 dimensions")
    if len(shape) != coords.shape[1]:
        raise ValueError(f"Input shape dimensions({len(shape)}) must match "
                         f"coordinates length({coords.shape[1]})")
    # Allocate dense corresponding to our target Sparse shape
    dense = np.zeros((shape), dtype=np.uint8)
    # Set values at each coordinate to 1
    for i in range(coords.shape[0]):
        dense[tuple(coords[i])] = 1
    # Convert the dense to a Sparse
    return dense_to_sparse(dense)


def dense_to_sparse(in_array):
    """Converts a hollow dense array to a Sparse input.

    The input array will simply be converted to a list of events corresponding
    to its active (non-zero) coordinates.

    The input array must have a (w, h, c) or (n, w, h, c) shape, where:

    - n is the number of samples,
    - w is the size of the first spatial dimension (typically, the width),
    - h is the size of the second spatial dimension (typically, the height),
    - c is the size of the last dimension (typically, the channel or feature).

    The output Sparse will have a shape of (n, w, h, c), with n = 1 if the
    input array only has three dimensions.

    Args:
      in_array (:obj:`numpy.ndarray`): an array of 3D or 4D coordinates.

    Returns:
      :obj:`Sparse`:  the events corresponding to non-null values.

    """
    if (len(in_array.shape) < 3 or len(in_array.shape) > 4):
        raise ValueError("Input space must have 3 or 4 dimensions")
    # Reshape to obtain a 4-dimensional output
    if len(in_array.shape) == 3:
        in_array = in_array[np.newaxis, :, :, :]
    # Extract indices of non-zero pixels in the array
    coords = np.where(in_array)
    data = in_array[coords]
    events = Sparse(in_array.shape, np.vstack(coords).transpose(), data)
    return events


def packetize(events, shape, packet_size):
    """Converts a list of 3D coordinates to a 4-dimensional Sparse input.

    This function converts a numpy array of event coordinates to a Sparse object
    where the event coordinates are grouped according to the specified packet
    size.

    3D event coordinates should contain:

    - a first spatial coordinate (typically x, the pixel column),
    - a second spatial coordinate (typically y, the pixel line),
    - a feature index representing the spike (starting from index zero)

    The output Sparse will have a shape of (n, w, h, c), where:

    - n is the number of packets,
    - w is the size of the first spatial dimension (typically, the width),
    - h is the size of the second spatial dimension (typically, the height),
    - c is the size of the last dimension (typically, the channel or feature).

    Event values are automatically set to 1.

    Args:
      events (:obj:`numpy.ndarray`): a (n, 3) array of input coordinates.
      shape (:obj:`tuple[int]`): the three dimensions of the input space.
      packet_size (:obj:`int`): the number of events per packet.

    Returns:
      :obj:`Sparse`: the (n, w, h, c) events corresponding to the coordinates.

    """
    if len(events.shape) != 2 or events.shape[1] != 3:
        raise ValueError("Coordinates must be a (n, 3) array.")
    if len(shape) != 3:
        raise ValueError("Shape must be (w, h, c)")
    if packet_size <= 0:
        raise ValueError("The packet size must be strictly positive")
    nb_events = events.shape[0]
    nb_packets = int(np.ceil(nb_events / packet_size))
    packets = np.zeros((nb_packets, shape[0], shape[1], shape[2]),
                       dtype=np.uint8)
    packet = 0
    for n in range(nb_events):
        if n > 0 and n % packet_size == 0:
            packet = packet + 1
        packets[packet, events[n, 0], events[n, 1], events[n, 2]] = 1
    return dense_to_sparse(packets)

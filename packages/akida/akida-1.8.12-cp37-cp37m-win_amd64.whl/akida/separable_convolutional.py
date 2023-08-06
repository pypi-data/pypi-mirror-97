from akida.core import (Layer, SeparableConvolutionalParams, ConvolutionMode,
                        PoolingType, ConvolutionalParams, DataProcessingParams,
                        NumNeuronsParams, WeightBitsParams, LearningParams,
                        ActivationsParams, ConvolutionKernelParams,
                        PoolingParams, StrideParams)


class SeparableConvolutional(Layer):
    """Separable convolutions consist in first performing a depthwise spatial
    convolution (which acts on each input channel separately) followed by a
    pointwise convolution which mixes together the resulting output channels.
    Intuitively, separable convolutions can be understood as a way to factorize
    a convolution kernel into two smaller kernels, thus decreasing the number of
    computations required to evaluate the output potentials. The
    ``SeparableConvolutional`` layer can also integrate a final pooling
    operation to reduce its spatial output dimensions.

    Args:
        kernel_width (int): convolutional kernel width.
        kernel_height (int): convolutional kernel height.
        num_neurons (int): number of pointwise neurons.
        name (str, optional): name of the layer.
        convolution_mode (:obj:`ConvolutionMode`, optional): type of convolution.
        stride_x (int, optional): convolution stride X.
        stride_y (int, optional): convolution stride Y.
        weights_bits (int, optional): number of bits used to quantize weights.
        pooling_width (int, optional): pooling window width. If set to -1 it
            will be global.
        pooling_height  (int, optional): pooling window height. If set to -1
            it will be global.
        pooling_type (:obj:`PoolingType`, optional): pooling type
            (None, Max or Average).
        pooling_stride_x (int, optional): pooling stride on x dimension.
        pooling_stride_y (int, optional): pooling stride on y dimension.
        activations_enabled (bool, optional): enable or disable activation
            function.
        threshold_fire (int, optional): threshold for neurons to fire or
            generate an event.
        threshold_fire_step (float, optional): length of the potential
            quantization intervals.
        threshold_fire_bits (int, optional): number of bits used to quantize
            the neuron response.

    """

    def __init__(self,
                 kernel_width,
                 kernel_height,
                 num_neurons,
                 name="",
                 convolution_mode=ConvolutionMode.Same,
                 stride_x=1,
                 stride_y=1,
                 weights_bits=2,
                 pooling_width=-1,
                 pooling_height=-1,
                 pooling_type=PoolingType.NoPooling,
                 pooling_stride_x=-1,
                 pooling_stride_y=-1,
                 activations_enabled=True,
                 threshold_fire=0,
                 threshold_fire_step=1,
                 threshold_fire_bits=1):
        try:
            params = SeparableConvolutionalParams(
                ConvolutionalParams(
                    DataProcessingParams(
                        NumNeuronsParams(num_neurons),
                        WeightBitsParams(weights_bits), LearningParams(),
                        ActivationsParams(activations_enabled, threshold_fire,
                                          threshold_fire_step,
                                          threshold_fire_bits)),
                    ConvolutionKernelParams(kernel_width, kernel_height,
                                            convolution_mode),
                    PoolingParams(pooling_width, pooling_height, pooling_type,
                                  pooling_stride_x, pooling_stride_y),
                    StrideParams(stride_x, stride_y)))

            # Call parent constructor to initialize C++ bindings
            # Note that we invoke directly __init__ instead of using super, as
            # specified in pybind documentation
            Layer.__init__(self, params, name)
        except:
            self = None
            raise

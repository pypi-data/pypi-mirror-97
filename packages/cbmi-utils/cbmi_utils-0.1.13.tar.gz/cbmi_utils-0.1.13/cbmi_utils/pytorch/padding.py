def get_padding_same_conv2d(size: int, kernel_size: int, stride: int = 1, dilation: int = 1):
    """
    Helper to calculate padding same like in tensorflow. Will be included in PyTorch 1.9: https://github.com/pytorch/pytorch/issues/3867
    """
    padding = ((size - 1) * (stride - 1) + dilation * (kernel_size - 1)) // 2
    
    return padding


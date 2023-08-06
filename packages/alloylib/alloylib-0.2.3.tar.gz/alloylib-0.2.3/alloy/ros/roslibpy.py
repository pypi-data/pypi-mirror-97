# Copyright - Transporation, Bots, and Disability Lab - Carnegie Mellon University
# Released under MIT License

"""
Convert Functions for roslibpy
"""

import numpy as np
import base64
import sys

import logging
logging.basicConfig()


def _get_encoding_information(encoding):

    if encoding == 'bgra8':
        return 4, np.uint8
    elif encoding == 'bgr8':
        return 3, np.uint8
    elif encoding == 'mono8':
        return 1, np.uint8


def image_to_numpy(image_msg_dict, desire_encoding='passthrough'):
    """
    Convert sensor_msgs/Image (in dict form) to a numpy array
    """
    # if image_msg_dict['encoding'] != 'bgra8':
    #    raise NotImplementedError("Unable to convert other image besides bgra8")

    num_channel, dtype = _get_encoding_information(image_msg_dict['encoding'])
    buffer = base64.b64decode(image_msg_dict['data'])
    data_arr = np.frombuffer(buffer, dtype)
    data_arr = np.reshape(
        data_arr, (image_msg_dict['height'], image_msg_dict['width'], num_channel))

    # now we convert it
    if desire_encoding == 'bgr8' and image_msg_dict['encoding'] == 'bgra8':
        data_arr = data_arr[:, :, 0:3]

    return data_arr, image_msg_dict['header']


def numpy_to_image(image_numpy, encoding_name="bgr8", header=None):
    """
    Convert a numpy array to sensor_msgs/Image (in dict form)
    only works with bgra8
    """

    image_dict = dict()

    # the header
    image_dict['header'] = header

    image_shape = np.shape(image_numpy)
    image_dict['width'] = image_shape[1]
    image_dict['height'] = image_shape[0]
    image_num_channels = image_shape[2] if len(image_shape) >= 3 else 1
    # put in the data

    if sys.version_info >= (3, 0):
        buffer = (memoryview(image_numpy.copy())).tobytes()
        # literally translate it to string including b''
        encoded_str = str(base64.b64encode(buffer))
        # remove the b' in front and ' in of the string literal.
        encoded_str = encoded_str[2:-1]
        image_dict['data'] = encoded_str
    else:
        # the copy here will make the image to have a continous buffer in the memory
        buffer = np.getbuffer(image_numpy.copy())
        image_dict['data'] = base64.b64encode(buffer)

    image_dict['encoding'] = encoding_name
    image_dict['is_bigendian'] = 0
    image_dict['step'] = image_shape[1] * image_num_channels
    return image_dict

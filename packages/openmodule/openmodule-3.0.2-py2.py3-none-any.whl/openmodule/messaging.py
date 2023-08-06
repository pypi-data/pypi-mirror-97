from typing import Optional, Tuple, Dict

import logging
import orjson
import zmq


def get_sub_socket(context, config, linger=0) -> zmq.Socket:
    socket = context.socket(zmq.SUB)
    socket.setsockopt(zmq.LINGER, linger)
    socket.connect(config.BROKER_PUB)
    return socket


def get_pub_socket(context, config, linger=100) -> zmq.Socket:
    socket = context.socket(zmq.PUB)
    socket.setsockopt(zmq.LINGER, linger)
    socket.connect(config.BROKER_SUB)
    return socket


def receive_message_from_socket(sub_socket: zmq.Socket) -> Tuple[Optional[bytes], Optional[Dict]]:
    """
    :param sub_socket: zmq socket to receive
    :return: returns None if an invalid message was received
             otherwise returns a tuple containing (topic: bytes, message: dict)
    """
    parts = sub_socket.recv_multipart()
    if len(parts) != 2:
        logging.error(f"received a zmq message with an invalid number of parts: {len(parts)}")
        return None, None

    topic, message = parts

    try:
        message_dict = orjson.loads(message)
    except orjson.JSONDecodeError as e:
        logging.error(f"received a zmq message with an invalid json. parsing error: {str(e)}")
        return None, None
    else:
        if not isinstance(message_dict, dict):
            logging.error(f"received a zmq message which was not a dict but a {type(message)}")
            return None, None
        else:
            return topic, message_dict

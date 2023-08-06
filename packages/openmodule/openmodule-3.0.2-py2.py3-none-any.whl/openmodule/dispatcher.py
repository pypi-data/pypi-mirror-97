from collections import defaultdict

import logging
import zmq
from pydantic import ValidationError, BaseModel
from typing import Union, Optional, Callable, DefaultDict, List, Dict, TypeVar, Type, Generic

from openmodule.models.base import ZMQMessage


class Listener:
    def __init__(self, message_class: Type[ZMQMessage], filter: Optional[Dict], handler: Callable):
        self.filter = filter
        self.handler = handler
        self.message_class = message_class

    def matches(self, message: Dict):
        if self.filter is None:
            return True
        else:
            return message.items() >= self.filter.items()


EventArgs = TypeVar("EventArgs")


class EventListener(Generic[EventArgs], list):
    log: Optional[logging.Logger]

    def __init__(self, *args, log=None, raise_exceptions=False):
        super().__init__(*args)
        self.raise_exceptions = raise_exceptions
        self.log = log or logging

    def __call__(self, *args: EventArgs):
        for f in self:
            try:
                f(*args)
            except zmq.ContextTerminated:
                raise
            except Exception as e:
                if self.raise_exceptions:
                    raise
                else:
                    self.log.exception(e)


ZMQMessageSub = TypeVar('ZMQMessageSub', bound=ZMQMessage)


class MessageDispatcher:
    def __init__(self, name=None, raise_validation_errors=False, raise_handler_errors=False):
        """
        :param name: optionally name the dispatcher for logging purposes
        :param raise_validation_errors: if true and received messages do not match a validation error is raised,
                                        this is useful in restricive code or testcases
        :param raise_validation_errors: if true and a message handler raises an exception, the exception is raised,
                                        this is useful in restricive code or testcases
        """
        self.name = name
        self.log = logging.getLogger(f"{self.__class__.__name__}({self.name})")
        self.listeners: DefaultDict[bytes, List[Listener]] = defaultdict(list)
        self.raise_validation_errors = raise_validation_errors
        self.raise_handler_errors = raise_handler_errors

    def register_handler(self, topic: Union[bytes, str],
                         message_class: Type[ZMQMessageSub],
                         handler: Callable[[ZMQMessageSub], None], *,
                         filter: Optional[Dict] = None):
        if hasattr(topic, "encode"):
            topic = topic.encode()
        self.listeners[topic].append(Listener(message_class, filter, handler))

    def dispatch(self, topic: bytes, message: Union[Dict, BaseModel]):
        if isinstance(message, BaseModel):
            message = message.dict()

        listeners = self.listeners.get(topic, [])
        for listener in listeners:
            if listener.matches(message):
                self.execute(listener, message)

    def execute(self, listener: Listener, message: Dict):
        try:
            parsed_message = listener.message_class(**message)
        except ValidationError as e:
            if self.raise_validation_errors:
                raise e from None
            else:
                self.log.exception("Invalid message received")
        else:
            try:
                listener.handler(parsed_message)
            except zmq.ContextTerminated:
                raise
            except Exception as e:
                if self.raise_handler_errors:
                    raise e from None
                else:
                    self.log.exception("Error in message handler")


class SubscribingMessageDispatcher(MessageDispatcher):
    def __init__(self, subscribe: Callable[[bytes], None], name=None):
        super().__init__(name=name)
        self.subscribe = subscribe

    def register_handler(self, topic: Union[bytes, str],
                         message_class: Type[ZMQMessageSub],
                         handler: Callable[[ZMQMessageSub], None], *,
                         filter: Optional[Dict] = None):
        self.subscribe(topic)
        return super().register_handler(topic, message_class, handler, filter=filter)

import logging
import os
import time
from logstash_async.handler import AsynchronousLogstashHandler
from logstash_async.formatter import LogstashFormatter
from egune.interfaces import ActorMessage, ActorResponse, Interface, UserMessage
from typing import Callable, Dict, Any, List


logger = logging.getLogger('')


def init_logger(config):
    global logger
    logger = logging.getLogger(config["name"])
    logger.setLevel(logging.INFO)
    if config["host"] == "HOST":
        config["host"] = os.environ["HOST"]
    logstash_formatter = LogstashFormatter(message_type=f"egune-{config['name']}")
    logstash_handler = AsynchronousLogstashHandler(config["host"], config["port"], None)
    logstash_handler.setFormatter(logstash_formatter)
    logger.addHandler(logstash_handler)
    logger.info(f"Started {config['name']}", extra={
        "log_event": "system started"
    })


def user_message_log(func: Callable[[UserMessage], UserMessage]):
    def wrapper(data: Dict[str, Any]) -> Dict[str, Any]:
        s = time.time()
        try:
            result = func(UserMessage.from_dict(data)).to_dict()
            logger.info("Processed", extra={
                "log_event": "processed",
                "user_id": data["user_id"],
                "process_input": str(data),
                "process_output": str(result),
                "time": time.time() - s
            })
            return result
        except Exception as e:
            logger.error("Processed", extra={
                "log_event": "process failed",
                "user_id": data["user_id"],
                "process_input": str(data),
                "process_output": str(e),
                "time": time.time() - s
            })
            return data
    return wrapper


def cd_user_message_log(func: Callable[[UserMessage], List[Interface]]):
    def wrapper(data: Dict[str, Any]) -> List[Dict[str, Any]]:
        s = time.time()
        try:
            result = [c.to_dict() for c in func(UserMessage.from_dict(data))]
            logger.info("Processed User message", extra={
                "log_event": "user message",
                "user_id": data["user_id"],
                "process_input": str(data),
                "process_output": str(result),
                "time": time.time() - s
            })
            return result
        except Exception as e:
            logger.error("Processed User message", extra={
                "log_event": "user message failed",
                "user_id": data["user_id"],
                "process_input": str(data),
                "process_output": str(e),
                "time": time.time() - s
            })
            return []
    return wrapper


def cd_actor_response_log(func: Callable[[ActorResponse], List[Interface]]):
    def wrapper(data: Dict[str, Any]) -> List[Dict[str, Any]]:
        s = time.time()
        try:
            result = [c.to_dict() for c in func(ActorResponse.from_dict(data))]
            logger.info("Processed User message", extra={
                "log_event": "user message",
                "user_id": data["user_id"],
                "process_input": str(data),
                "process_output": str(result),
                "time": time.time() - s
            })
            return result
        except Exception as e:
            logger.error("Processed User message", extra={
                "log_event": "user message failed",
                "user_id": data["user_id"],
                "process_input": str(data),
                "process_output": str(e),
                "time": time.time() - s
            })
            return []
    return wrapper


def egune_response_log(func: Callable[[ActorMessage], ActorMessage]):
    def wrapper(data: Dict[str, Any]) -> Dict[str, Any]:
        s = time.time()
        try:
            result = func(ActorMessage.from_dict(data)).to_dict()
            logger.info("Processed User message", extra={
                "log_event": "user message",
                "user_id": data["user_id"],
                "process_input": str(data),
                "process_output": str(result),
                "time": time.time() - s
            })
            return result
        except Exception as e:
            logger.error("Processed User message", extra={
                "log_event": "user message failed",
                "user_id": data["user_id"],
                "process_input": str(data),
                "process_output": str(e),
                "time": time.time() - s
            })
            return data
    return wrapper


def log(extra):
    logger.info("custom", extra=extra)

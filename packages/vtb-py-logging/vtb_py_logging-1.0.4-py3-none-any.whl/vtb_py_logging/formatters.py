import json
import logging.config
from datetime import datetime
from logging import LogRecord


def get_data_record(record: LogRecord) -> tuple:
    order_action = getattr(record, 'order_action', {})
    order_id = order_action.get('order_id')
    action_id = order_action.get('action_id')
    graph_id = order_action.get('graph_id')
    node = getattr(record, 'node', None)
    action_type = getattr(record, 'action_type', None)
    orchestrator_id = getattr(record, 'orchestrator_id', None)
    return order_id, action_id, graph_id, node, action_type, orchestrator_id


class OrderJsonFormatter(logging.Formatter):

    def format(self, record):
        order_id, action_id, graph_id, node, action_type, orchestrator_id = get_data_record(record)
        return json.dumps(
            {
                '@timestamp': datetime.utcnow().isoformat()[:-3] + 'Z',
                'level': record.levelname,
                'text': super().format(record),
                'order_id': order_id,
                'action_id': action_id,
                'graph_id': graph_id,
                'node': node,
                'action_type': action_type,
                'orchestrator_id': orchestrator_id
            }
        )


class OrderConsoleFormatter(logging.Formatter):
    COLOR_MAPPING = {
        'INFO': '\33[32m',
        'WARNING': '\33[33m',
        'CRITICAL': '\33[35m',
        'ERROR': '\33[31m'
    }

    def format(self, record):
        order_id, action_id, graph_id, node, action_type, orchestrator_id = get_data_record(record)
        timestamp = datetime.utcnow().isoformat()[:-3] + 'Z'
        color = self.COLOR_MAPPING.get(record.levelname) or '\33[34m'
        return f'{color}msg: {super().format(record)}\n' \
               f'timestamp: {timestamp}\n' \
               f'level: {record.levelname}\n' \
               f'order_id: {order_id}\n' \
               f'action_id: {action_id}\n' \
               f'graph_id: {graph_id}\n' \
               f'node: {node}\n' \
               f'action_type: {action_type}\n' \
               f'orchestrator_id: {orchestrator_id}\n' \
               f'{record.pathname}:{record.lineno}\n'


class DefaultColoredFormatter(logging.Formatter):
    COLOR_MAPPING = {
        'INFO': '\33[32m',
        'WARNING': '\33[33m',
        'CRITICAL': '\33[35m',
        'ERROR': '\33[31m'
    }

    def format(self, record):
        t = self.formatTime(record)
        level = record.levelname
        line = record.lineno
        color = self.COLOR_MAPPING.get(level) or '\33[34m'  # blue
        default_color = '\33[0m'
        msg = str(record.msg)
        if record.args:
            msg = msg % record.args
        return f'{color}{t} {level}\n{record.pathname} line {line}{default_color}\n{msg}\n'

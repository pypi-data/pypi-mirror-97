import time
from .buffers.protobuf.nn.Result_pb2 import Result
from .buffers.protobuf.nn.Message_pb2 import Message
from .exceptions import ServerError, UnknownResult
from .amqp.exceptions import Timeout as AMQPTimeout


def parse_result_buffer(result):
    '''
    returns a vulcain protobuf message parsed to retrieve only the important subfields
    '''
    result = result
    if result is None:
        return None
    if result.HasField('error'):
        raise ServerError(result.error.data, result.error.code)
    if result.HasField('v07_recognition'):
        return result.v07_recognition.outputs
    if result.HasField('v07_inference'):
        return result.v07_inference
    raise UnknownResult(result)


class Response(object):
    def __init__(self, msg):
        self.msg = msg

    @property
    def body(self):
        return self.msg.body

    def to_message_buffer(self):
        return Message.FromString(self.body)

    def to_result_buffer(self):
        return Result.FromString(self.body)

    def to_parsed_result_buffer(self):
        result = self.to_result_buffer()
        return parse_result_buffer(result)

    def get_labelled_output(self):
        outputs = self.to_parsed_result_buffer()
        if len(outputs) != 1:
            raise Exception("get_labelled_predictions() can only work with one output")
        return outputs[0].labels


def wait_responses(consumer, correlation_ids, timeout=float('inf')):
    '''
    Returns a tuple of two lists:
    - The first one is a list of tuple (position, msg_body). The position is the original index in the correlation_ids param.
      It can gives you the corresponding correlation_id by doing correlation_ids[results[idx][0]]. msg_body is the response body.
    - The second one is a list of position. The position is the original index in the correlation_ids param.
      It can gives you the corresponding correlation_id by doing correlation_ids[pending[idx]]
    '''

    responses = []
    positions = dict((c, idx) for idx, c in enumerate(correlation_ids))
    correlation_ids = list(correlation_ids)

    start_time = time.time()
    while correlation_ids:
        correlation_id = correlation_ids.pop(0)
        try:
            response = consumer.get(correlation_id=correlation_id, timeout=0.015, drain_events_timeout=0.005)
            responses.append((positions[correlation_id], response))
        except AMQPTimeout:
            correlation_ids.append(correlation_id)
        if timeout < 0:  # same as float('inf')
            continue
        if time.time() - start_time > timeout:
            break

    pending = [positions[correlation_id] for correlation_ids in correlation_ids]
    return (
        sorted(responses, key=lambda v: v[0]),  # List of tuple (original_position, body)
        sorted(pending)  # positions of the corresponding correlation_ids that didn't get a response.
        # To get the corresponding correlation_id, use correlation_ids[pending[idx]]
    )
    return responses


def wait(consumer, correlation_id, *args, **kwargs):
    msg = consumer.get(correlation_id=correlation_id, *args, **kwargs)
    if msg is None:
        return None
    return Response(msg)

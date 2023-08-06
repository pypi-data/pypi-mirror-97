from .helpers import proto
from .amqp.client import RPCClient
from .response import Response
from contextlib import contextmanager


class Client(RPCClient):
    def tmp_consuming_queue(self, **kwargs):
        return super(Client, self).tmp_consuming_queue(**kwargs)

    def new_consuming_queue(self, **kwargs):
        return super(Client, self).new_consuming_queue(msg_wrapper=Response, **kwargs)

    def new_stream(self, command_queue_name, **kwargs):
        return super(Client, self).new_stream(command_queue_name, msg_wrapper=Response, **kwargs)

    def command(self, command_queue_name, reply_to, *args, **kwargs):
        if reply_to is not None:
            kwargs['forward_to'] = [reply_to] # for retrocompatibility
        serialized_buffer = proto.create_serialized_command(*args, **kwargs)
        return self.send_binary(serialized_buffer, command_queue_name, reply_to=reply_to)

    def v07_images_command(self, command_queue_name, reply_to, v07_image_inputs, *args, **kwargs):
        if reply_to is not None:
            kwargs['forward_to'] = [reply_to]  # for retrocompatibility
        serialized_buffer = proto.create_v07_images_command(v07_image_inputs, *args, **kwargs)
        return self.send_binary(serialized_buffer, command_queue_name, reply_to=reply_to)

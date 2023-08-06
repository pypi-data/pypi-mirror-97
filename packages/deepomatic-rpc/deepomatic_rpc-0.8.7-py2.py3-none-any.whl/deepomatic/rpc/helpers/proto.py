import uuid
import base64
from . import v07_proto
from ..buffers.protobuf.nn.Command_pb2 import CommandInfo, Command
from ..buffers.protobuf.nn.Message_pb2 import Message

from .common import get_file_content

IMAGE_PREFIX = b'data:image/*;'
BINARY_IMAGE_PREFIX = IMAGE_PREFIX + b'binary,'
BASE64_IMAGE_PREFIX = IMAGE_PREFIX + b'base64,'


def binary_source_from_img_file(filename_or_fileobj):
    '''
        converts the content of a local image file into a binary source message
    '''
    return BINARY_IMAGE_PREFIX + get_file_content(filename_or_fileobj)


def base64_source_from_img_file(filename_or_fileobj):
    '''
        You should prefer sending in binary format (the content to send will be smaller)
        converts the content of a local image file into a binary source message
    '''
    content = get_file_content(filename_or_fileobj)
    return BASE64_IMAGE_PREFIX + base64.b64encode(content)


def create_command_info(forward_to=None, app_id=None, app_pk=None, date_plan=None):

    base_info = CommandInfo()
    base_info.track_id = str(uuid.uuid4())

    check_variables = [app_id, app_pk, date_plan]
    if all(check_variables):
        # Allow to count quota
        base_info.app_id = app_id  # must be an alphanumeric string
        base_info.app_pk = app_pk  # must be an integer corresponding to user profile pk
        base_info.date_plan = date_plan
    elif any(check_variables):
        raise Exception("Either provide `app_id`, `app_pk` and `date_plan` or none of them."
                        "This is only useful if you want to count quotas and have postgres backend")

    if forward_to is None:
        forward_to = []

    base_info.forward_to.extend(forward_to)

    return base_info


def create_serialized_command_from_base_info(input_mix, command_mix, base_info, task_id=None):
    cmd_buffer = Command(
        command_mix=command_mix,
        input_mix=input_mix,
        base_info=base_info
    )

    if task_id is not None:
        cmd_buffer.task.id = task_id

    message = Message(command=cmd_buffer)
    return message.SerializeToString()


def create_serialized_command(input_mix, command_mix, forward_to=None, task_id=None, **base_info_kwargs):
    base_info = create_command_info(forward_to=forward_to, **base_info_kwargs)
    return create_serialized_command_from_base_info(input_mix, command_mix, base_info, task_id)


def create_v07_images_command(v07_image_inputs, *args, **kwargs):
    input_mix = v07_proto.create_images_input_mix(v07_image_inputs)
    serialized_buffer = create_serialized_command(input_mix, *args, **kwargs)
    return serialized_buffer

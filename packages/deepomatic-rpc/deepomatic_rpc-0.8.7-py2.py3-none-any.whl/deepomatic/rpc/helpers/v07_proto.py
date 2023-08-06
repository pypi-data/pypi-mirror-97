from ..buffers.protobuf.nn.v07.Inputs_pb2 import Inputs as v07_Inputs
from ..buffers.protobuf.nn.Command_pb2 import CommandMix, InputMix
from ..buffers.protobuf.nn.v07.Commands_pb2 import (Recognition, Inference,
                                                    Workflow)


def create_images_input_mix(v07_image_inputs):
    image_inputs = [
        v07_Inputs.InputMix(image=image) for image in v07_image_inputs
    ]
    v07_inputs = v07_Inputs(inputs=image_inputs)
    return InputMix(v07_inputs=v07_inputs)


def create_recognition_command_mix(version_id, max_predictions=100, show_discarded=False):
    return CommandMix(
        v07_recognition=Recognition(
            version_id=version_id,
            show_discarded=show_discarded,
            max_predictions=max_predictions
        )
    )


def create_inference_command_mix():
    return CommandMix(v07_inference=Inference())


def create_workflow_command_mix():
    '''
        returns a protobuf message
        '''
    return CommandMix(v07_workflow=Workflow())

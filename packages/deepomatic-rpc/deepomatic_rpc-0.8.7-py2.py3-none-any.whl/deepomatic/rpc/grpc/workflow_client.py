import logging

import grpc

from ..buffers.protobuf.workflows.WorkflowExecution_pb2_grpc import WorkflowExecutorStub

logger = logging.getLogger(__name__)


def create_grpc_client(host='localhost', port=50051):
    """Open a gRPC channel and start a client

    Returns:
        gRPC client
    """
    logger.info("Client starting...")
    channel = grpc.insecure_channel("{}:{}".format(host, port))
    stub = WorkflowExecutorStub(channel)
    logger.info("Client started. Listening on port: {}.".format(port))
    return stub

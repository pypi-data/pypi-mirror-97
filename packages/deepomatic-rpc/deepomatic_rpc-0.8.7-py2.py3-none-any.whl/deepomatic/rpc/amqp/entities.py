import logging
import uuid
import time
import string
import socket
import traceback
import kombu
from amqp.exceptions import NotFound
from kombu.utils.functional import LRUCache
from .exceptions import Timeout


logger = logging.getLogger(__name__)


TAGS_SEPARATOR = '___'


def default_tag_prefix():
    return 'lru_consumer-{}{}'.format(uuid.uuid4(), TAGS_SEPARATOR)


class Queue(kombu.Queue):
    """
    An improved kombu.Queue that ensure ensured_connection is always up
    In this whole class `ensured_connection` must be an EnsuredConnection
    """
    def __init__(self, ensured_connection, channel=None, *args, **kwargs):
        self.ensured_connection = ensured_connection
        if channel is None:
            channel = ensured_connection.default_channel
        super(Queue, self).__init__(channel=channel, *args, **kwargs)
        self.declare()

    def revive(self, ensured_connection, channel=None):
        # channel should have been created by the ensured_connection
        self.ensured_connection = ensured_connection
        if channel is None:
            channel = self.ensured_connection.default_channel
        super(Queue, self).revive(channel)
        self.declare()

    def as_dict(self, recurse=False):
        # This function is important for kombu.Consumer.revive
        res = super(Queue, self).as_dict(recurse)
        res['ensured_connection'] = self.ensured_connection
        return res

    def basic_get(self,
                  no_ack=True,
                  block=True,
                  timeout=None,
                  decoder=None,
                  correlation_id=None,
                  accept=None,
                  ensured_connection=None):
        """
        Improve kombu.Queue.get to add a block and timeout
        """
        t = time.time()
        ensured_connection = ensured_connection or self.ensured_connection
        while True:
            msg = ensured_connection.ensure_and_heartbeat(self, self.get, no_ack=no_ack, accept=accept)
            if msg:
                cid = msg.properties.get('correlation_id')
                if correlation_id is not None and cid != correlation_id:
                    if not no_ack:
                        msg.ack()  # since we will either throw it away or requeue a copy of it
                    try:
                        if decoder:
                            msg.body = decoder(msg.body)
                        # We try to display the message we will throw away
                        printable = set(string.printable)
                        body = [x for x in msg.body if x in printable]
                        logger.warning("Throwing away msg %s from queue %s, body : %s" % (cid, self.name, body))
                    except Exception:
                        logger.warning("Throwing away msg %s from queue %s" % (cid, self.name))
                    continue
                else:
                    if decoder:
                        msg.body = decoder(msg.body)
                    logger.debug("Getting msg %s : %s" % (correlation_id, msg.body))
                    return msg
            if not block:
                return None
            elif timeout is not None and time.time() - t > timeout:
                raise Timeout(timeout)
            else:
                time.sleep(0.002)

    def declare(self, *args, **kwargs):
        """
        Declare queue and bind it to its exchange. Does nothing if self.no_declare is True.
        Override kombu.Queue.declare by ensuring connection.
        """
        ensured_connection = kwargs.pop('ensured_connection', None) or self.ensured_connection
        return ensured_connection.ensure_and_heartbeat(self, super(Queue, self).declare, *args, **kwargs)

    def queue_declare(self, *args, **kwargs):
        """
        Declare queue only. Note that self.no_declare is ignored by this function.
        Override kombu.Queue.queue_declare by ensuring connection.
        """
        ensured_connection = kwargs.pop('ensured_connection', None) or self.ensured_connection
        return ensured_connection.ensure_and_heartbeat(self, super(Queue, self).queue_declare, *args, **kwargs)

    def exists(self, ensured_connection=None):
        try:
            self.queue_declare(ensure_options={'redeclare_on_not_found': False},
                               passive=True,
                               ensured_connection=ensured_connection)
            return True
        except NotFound:
            return False

    def qsize(self, ensured_connection=None):
        _, size, _ = self.queue_declare(passive=True, ensured_connection=ensured_connection)
        return size

    def purge(self, *args, **kwargs):
        ensured_connection = kwargs.pop('ensured_connection', None) or self.ensured_connection
        return ensured_connection.ensure_and_heartbeat(self, super(Queue, self).purge, *args, **kwargs)

    def delete(self, *args, **kwargs):
        ensured_connection = kwargs.pop('ensured_connection', None) or self.ensured_connection
        return ensured_connection.ensure_and_heartbeat(self, super(Queue, self).delete, *args, **kwargs)


class LRUConsumer(kombu.Consumer):
    """
    Consumer that stores the messages it receives in a LRUCache
    Messages MUST contains a correlation_id property
    """
    def __init__(self,
                 ensured_connection,
                 queues,
                 no_ack=False,
                 prefetch_count=1,
                 ack_when_received=True,
                 max_cache_msg=100,
                 cancel_when_full=True,
                 msg_wrapper=None,
                 **consumer_kwargs):
        self.ack_when_received = ack_when_received
        self.cancel_when_full = cancel_when_full
        self.cancelled_because_full = None
        self.consuming = None
        self.msg_wrapper = msg_wrapper
        self.lru_cache_message = LRUCache(max_cache_msg)
        tag_prefix = consumer_kwargs.pop('tag_prefix', default_tag_prefix())
        super(LRUConsumer, self).__init__(channel=None,
                                          queues=queues,
                                          on_message=self.on_message_callback,
                                          no_ack=no_ack,
                                          tag_prefix=tag_prefix,
                                          prefetch_count=prefetch_count,
                                          **consumer_kwargs)
        self.revive(ensured_connection)

    def consume(self, *args, **kwargs):
        ensured_connection = kwargs.pop('ensured_connection', None) or self.ensured_connection
        res = ensured_connection.ensure_and_heartbeat(self,
                                                      super(LRUConsumer, self).consume,
                                                      *args, **kwargs)
        self.consuming = True
        return res

    def cancel(self, ensured_connection=None):
        ensured_connection = ensured_connection or self.ensured_connection
        res = ensured_connection.ensure_and_heartbeat(self, super(LRUConsumer, self).cancel)
        self.consuming = False
        return res

    def qos(self, *args, **kwargs):
        ensured_connection = kwargs.pop('ensured_connection', None) or self.ensured_connection
        return ensured_connection.ensure_and_heartbeat(self,
                                                       super(LRUConsumer, self).qos,
                                                       *args, **kwargs)

    def declare(self, *args, **kwargs):
        ensured_connection = kwargs.pop('ensured_connection', None) or self.ensured_connection
        return ensured_connection.ensure_and_heartbeat(self,
                                                       super(LRUConsumer, self).declare,
                                                       *args, **kwargs)

    def revive(self, ensured_connection, channel=None):
        # channel should have been created by the ensured_connection
        self.ensured_connection = ensured_connection
        if channel is None:
            channel = self.ensured_connection.default_channel

        # The following is directly extracted from kombu.Consumer but adjusted for Queue
        self._active_tags.clear()
        channel = self.channel = kombu.connection.maybe_channel(channel)
        # modify dict size while iterating over it is not allowed
        for qname, queue in list(self._queues.items()):
            # name may have changed after declare
            self._queues.pop(qname, None)
            queue = self._queues[queue.name] = queue(self.channel)

            # queues must use the same channel as consumer (for acking)
            if isinstance(queue, Queue):
                queue.revive(ensured_connection, channel)
            else:
                queue.revive(channel)

        if self.auto_declare:
            self.declare()

        if self.prefetch_count is not None:
            self.qos(prefetch_count=self.prefetch_count)

        if self.consuming:  # was consuming before revive
            self.consume()

    def full(self):
        return len(self.lru_cache_message) == self.lru_cache_message.limit

    def __cancel_full(self):
        self.cancel()
        logger.warning('Consumer is full and has been cancelled. You must pop the items to keep consuming.')
        self.cancelled_because_full = True

    def on_message_callback(self, message):
        # this is called when doing something on the connection or when calling drain_events
        if not self.cancelled_because_full and self.cancel_when_full and self.full():
            self.__cancel_full()
        if not self.no_ack and self.ack_when_received:
            if self.cancelled_because_full:
                message.requeue()
                return
            message.ack()
        self.lru_cache_message[message.properties['correlation_id']] = message

    def drain_events(self, timeout=1, ensured_connection=None):
        ensured_connection = ensured_connection or self.ensured_connection
        try:
            ensured_connection.drain_events(timeout=timeout)
            return True  # no timeout
        except socket.timeout:
            return False
        except Exception as e:
            logger.warning(e)
            try:
                ensured_connection.ensure_and_heartbeat_connection()
                ensured_connection.recover_exc(e)
            except Exception:
                # This should not happen or it means there is a big problem on the server side
                logger.error(traceback.format_exc())
                time.sleep(1)

    def get(self, correlation_id=None, timeout=float('inf'), drain_events_timeout=0.005, ensured_connection=None):
        """
        timeout: negative or float('inf') will wait infinite, None is not blocking
        """
        ensured_connection = ensured_connection or self.ensured_connection
        start_time = time.time()
        drained = False
        while True:
            if self.cancelled_because_full and not self.full():  # not full anymore
                self.consume()
                logger.info('Consumer consuming again.')
                self.cancelled_because_full = False

            msg = None
            if correlation_id is None:
                if len(self.lru_cache_message) > 0:
                    key, msg = self.lru_cache_message.popitem(last=False)
            else:
                msg = self.lru_cache_message.pop(correlation_id, None)

            if msg is not None:
                if self.msg_wrapper is None:
                    return msg
                return self.msg_wrapper(msg)
            elif timeout is None:
                # We want to force one drain_events at least
                # or we will never get any message if the connection is not used between each gets
                if drained:
                    return None
            elif timeout >= 0 and time.time() - start_time > timeout:
                raise Timeout(timeout)

            if self.cancel_when_full and self.full():
                if not self.cancelled_because_full:
                    self.__cancel_full()
                ensured_connection.maybe_send_heartbeat()
                time.sleep(drain_events_timeout)
                ensured_connection.maybe_send_heartbeat()
            else:
                self.drain_events(drain_events_timeout, ensured_connection)
            drained = True

    def clear(self):
        self.lru_cache_message.clear()

    def __len__(self):
        return len(self.lru_cache_message)


class Producer(kombu.Producer):
    def __init__(self, ensured_connection, channel=None, *args, **kwargs):
        super(Producer, self).__init__(channel=None, *args, **kwargs)
        self.revive(ensured_connection, channel)

    def revive(self, ensured_connection, channel=None):
        # channel should have been created by the ensured_connection
        self.ensured_connection = ensured_connection
        if channel is None:
            # It seems to be better to create a new channel
            # because using the default_channel leads to weird behaviors
            # see https://github.com/celery/py-amqp/issues/276
            channel = self.ensured_connection.ensure_channel()
        super(Producer, self).revive(channel)

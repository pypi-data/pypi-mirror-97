import logging
import time
import uuid
import kombu
import socket
import traceback
from contextlib import contextmanager
from amqp.exceptions import NotFound, ConsumerCancelled, ConnectionError
from kombu.utils.functional import LRUCache
from .entities import Queue, Producer, LRUConsumer, TAGS_SEPARATOR, default_tag_prefix
from .exceptions import (QueueNotCached, ExchangeNotCached,
                         ConsumerNotCached)


logger = logging.getLogger(__name__)

# pyamqp is the most powerful transport and only tested transport, you shouldn't change
# librabbitmq used to have memory leaks, does not compile on mac and is not python3 compatible
TRANSPORT = "pyamqp"
DEFAULT_EXCHANGE = ''
QUEUE_EXPIRATION = 2 * 60 * 60 * 1000  # in ms
MESSAGE_EXPIRATION = 2 * 60 * 1000  # in ms
HEARTBEAT = 60
HEARTBEAT_RATE = 2


def basic_errback(exc, interval):
    logger.warning(exc)
    logger.info('Retry in %s seconds.', interval)


class Reviving(object):
    def __init__(self, ensured_connection, obj_to_revive, redeclare_consumer_on_error):
        self.ensured_connection = ensured_connection
        self.redeclare_consumer_on_error = redeclare_consumer_on_error
        self.obj_to_revive = obj_to_revive
        self.current_exc = None

    def errback(self, exc, interval):
        self.current_exc = exc
        basic_errback(exc, interval)

    def revive(self, channel):
        logger.debug('Reviving {}'.format(self.obj_to_revive))
        self.obj_to_revive.revive(self.ensured_connection)
        logger.debug('Revived {}'.format(self.obj_to_revive))

        self.ensured_connection.recover_exc(self.current_exc,
                                            self.redeclare_consumer_on_error)


class EnsuredConnection(kombu.Connection):
    def __init__(self,
                 url,
                 cache=None,
                 transport=TRANSPORT,
                 heartbeat=HEARTBEAT,
                 transport_options=None,
                 redeclare_on_not_found=True,
                 redeclare_consumer_on_error=True,
                 reraisable_exceptions=(),
                 **kwargs):
        self.cache = cache
        if transport_options is None:
            transport_options = {'confirm_publish': True}
        self.url = url
        self.last_heartbeat = 0
        self.redeclare_on_not_found = redeclare_on_not_found
        self.redeclare_consumer_on_error = redeclare_consumer_on_error
        # avoid retrying on those exceptions when called ensure_and_heartbeat and raise them to the user
        self.reraisable_exceptions = reraisable_exceptions
        self.interval_start = kwargs.pop('interval_start', 0.05)
        self.interval_max = kwargs.pop('interval_max', 5)
        self.heartbeat_rate = kwargs.pop('heartbeat_rate', HEARTBEAT_RATE)
        super(EnsuredConnection, self).__init__(self.url,
                                                transport=transport,
                                                heartbeat=heartbeat,
                                                transport_options=transport_options,
                                                **kwargs)

    def recover_exc(self, exc, redeclare_consumer_on_error=None):
        # For now, redeclare consumers if we receive a ConsumerCancelled or if the connection get lost
        if redeclare_consumer_on_error is None:
            redeclare_consumer_on_error = self.redeclare_consumer_on_error
        if isinstance(exc, ConsumerCancelled) and redeclare_consumer_on_error:
            if self.cache is not None:
                # The broker can through a ConsumerCancelled even though we asked for something else
                # (because we might use the same channel for multiple things)
                # Thus we need to have access to the cache to recover the consumer automatically
                consumer_tag = exc.reply_text
                consumer = self.cache.get_consumer_by_tag(consumer_tag)
                if consumer is not None:
                    logger.warning("Consumer {} has been cancelled by the broker. "
                                   "Redeclaring it.".format(consumer_tag))
                    consumer.revive(self)
                    logger.debug('Revived {}'.format(consumer))
                    return True
                else:
                    logger.warning(
                        "Consumer {} has been cancelled by the broker "
                        "and is not in the cache anymore."
                        "We can't redeclare it.".format(consumer_tag)
                    )
        elif isinstance(exc, (socket.error, ConnectionError)):
            if redeclare_consumer_on_error:
                # All consumers might are have been cancelled on connection lost
                for consumer in self.cache.consumers.values():
                    logger.debug("Reviving {}".format(consumer))
                    consumer.revive(self)
                    logger.debug("Revived {}".format(consumer))
        return False

    def drain_events(self, *args, **kwargs):
        self.maybe_send_heartbeat()
        return super(EnsuredConnection, self).drain_events(*args, **kwargs)

    def maybe_send_heartbeat(self):
        t = time.time()
        if t - self.last_heartbeat > self.heartbeat / self.heartbeat_rate:
            # this is probably useless as any call to the server count as a heartbeat
            # Though it is probably usable from a separate thread
            try:
                logger.debug("Sending heartbeat")
                self.heartbeat_check(rate=self.heartbeat_rate)
            except Exception as e:
                logger.warning(e)
            self.last_heartbeat = t

    @contextmanager
    def _reraise_as_library_errors(self, *args, **kwargs):
        # we want to get the real pyamqp errors, not a generic OperationalError, so we override this function
        # if you want to get a generic kombu error just call the parent func
        # with super(EnsuredConnection, connection)._reraise_as_library_errors():
        #     connection.ensure_and_heartbeat_connection()
        yield

    def ensure_and_heartbeat_connection(self, **kwargs):
        self.maybe_send_heartbeat()
        errback = kwargs.pop('errback', basic_errback)
        interval_start = kwargs.pop('interval_start', self.interval_start)
        interval_max = kwargs.pop('interval_max', self.interval_max)
        return self.ensure_connection(errback=errback,
                                      interval_start=interval_start,
                                      interval_max=interval_max,
                                      reraise_as_library_errors=False,
                                      **kwargs)

    def ensure_and_heartbeat(self, obj_to_revive, func, **kwargs):
        """
        This is variant of kombu.Connection.ensure that send heartbeat when it needs to and redeclare not found resources whenever possible.
        Redeclaration is done in the following cases:
        - An explicit action is asked on a queue or exchange that doesn't exists (qsize, purge etc).
        - When a consumer get cancelled (usually because another client deleted the queue), it redeclares the consumer (and corresponding queues).
        - When a connection error occurs, we redeclare all cached consumers (and their corresponding queues).
        """
        ensure_options = kwargs.pop('ensure_options', {})
        reraisable_exceptions = ensure_options.get('reraisable_exceptions',
                                                   self.reraisable_exceptions)
        redeclare_on_not_found = ensure_options.get('redeclare_on_not_found',
                                                    self.redeclare_on_not_found)
        redeclare_consumer_on_error = ensure_options.get('redeclare_consumer_on_error',
                                                         self.redeclare_consumer_on_error)
        interval_start = ensure_options.get('interval_start', self.interval_start)
        interval_max = ensure_options.get('interval_max', self.interval_max)
        reviving = Reviving(self, obj_to_revive, redeclare_consumer_on_error)
        errback = ensure_options.get('errback', reviving.errback)
        self.maybe_send_heartbeat()
        while True:
            try:
                f = self.ensure(self,
                                func,
                                interval_start=interval_start,
                                interval_max=interval_max,
                                errback=errback,
                                on_revive=reviving.revive)
                return f(**kwargs)
            except reraisable_exceptions:
                # We reraise the exceptions the user might want to handle himself
                raise
            except NotFound:
                if redeclare_on_not_found:
                    logger.warning("{} was not found, redeclaring it".format(obj_to_revive))
                    if isinstance(obj_to_revive, Queue):
                        obj_to_revive.declare()
                    elif isinstance(obj_to_revive, (kombu.Queue, kombu.Exchange)):
                        self.ensure_and_heartbeat(obj_to_revive, obj_to_revive.declare)
                    else:  # Unknown type
                        raise
                else:
                    raise
            except Exception:
                logger.error(traceback.format_exc())
                time.sleep(1)

    @property
    def default_channel(self):
        if self._default_channel is None:
            self._default_channel = self.ensure_channel()
        return self._default_channel

    def ensure_channel(self):
        return self.ensure_and_heartbeat(self, self.channel)


class EntityCache(object):
    def __init__(self,
                 max_exchange_cache_size=1000,
                 max_queue_cache_size=1000,
                 max_consumer_cache_size=1000):
        self.exchanges = LRUCache(limit=max_queue_cache_size)
        self.queues = LRUCache(limit=max_queue_cache_size)
        self.consumers = LRUCache(limit=max_consumer_cache_size)

    def get_consumer(self, tag_prefix):
        return self.consumers.get(tag_prefix)

    def get_queue(self, queue_name):
        return self.queues.get(queue_name)

    def get_exchange(self, exchange_name):
        return self.exchanges.get(exchange_name)

    def get_consumer_by_tag(self, tag):
        # Try to find the tag_prefix from the consumer tag
        if TAGS_SEPARATOR not in tag:
            return self.consumers.get(tag)
        split = tag.split(TAGS_SEPARATOR)
        if len(split) == 2:
            consumer_tag = split[0] + TAGS_SEPARATOR
            return self.consumers.get(consumer_tag)
        return None

    def add(self, entity):
        if isinstance(entity, (Queue, kombu.Queue)):
            self.queues[entity.name] = entity
        elif isinstance(entity, kombu.Exchange):
            self.exchanges[entity.name] = entity
        elif isinstance(entity, (LRUConsumer, kombu.Consumer)):
            self.consumers[entity.tag_prefix] = entity
        else:
            raise Exception("EntityCache doesn't handle type {} for variable {}. Cannot be added.".format(type(entity), entity))

    def remove(self, entity):
        if isinstance(entity, (Queue, kombu.Queue)):
            return self.queues.pop(entity.name, None)
        elif isinstance(entity, kombu.Exchange):
            return self.exchanges.pop(entity.name, None)
        elif isinstance(entity, (LRUConsumer, kombu.Consumer)):
            return self.consumers.pop(entity.tag_prefix, None)
        raise Exception("EntityCache doesn't handle type {} for variable {}. Cannot be removed.".format(type(entity), entity))


class Client(object):
    '''
    A client that caches entities and makes sure reconnections are done.
    '''
    def __init__(self, amqp_url, cache_kwargs=None, connection_kwargs=None):
        cache_kwargs = cache_kwargs or {}
        connection_kwargs = connection_kwargs or {}
        self.cache = EntityCache(**cache_kwargs)
        self.ensured_connection = EnsuredConnection(amqp_url,
                                                    cache=self.cache,
                                                    **connection_kwargs)

        logger.info("New connection to %s" % self.ensured_connection.as_uri())

        self._producer = None
        self.ensure_and_hearbeat = self.ensured_connection.ensure_and_heartbeat

    @property
    def producer(self):
        # Lazy initialization to avoid connecting when declaring the Client
        if self._producer is None:
            self._producer = Producer(self.ensured_connection)
        return self._producer

    @property
    def connected(self):
        return self.ensured_connection.connected

    def connect(self):
        self.ensured_connection.connect()

    def __get_or_declare(self, key,
                         cache_get_func,
                         declare_func,
                         exc_to_raise,
                         force_redeclare=False,
                         raise_if_not_cached=False, *args, **kwargs):
        if not force_redeclare:
            entity = cache_get_func(key)
            if entity is not None:
                return entity
            elif raise_if_not_cached:
                raise exc_to_raise()

        entity = declare_func(*args, **kwargs)
        self.cache.add(entity)
        logger.info("Declared {}".format(entity))
        return entity

    # Queues functions

    def get_cached_queue(self, queue_name,
                         routing_key=None,
                         exchange=None,
                         exclusive=False,
                         queue_arguments=None,
                         passive=False,
                         durable=True,
                         auto_delete=False,
                         no_declare=False,
                         force_redeclare=False,
                         raise_if_not_cached=False):

        if exchange is None:
            exchange = self.get_cached_exchange(DEFAULT_EXCHANGE, 'direct')

        if routing_key is None:
            routing_key = queue_name

        return self.__get_or_declare(
            queue_name,
            self.cache.get_queue,
            Queue,
            QueueNotCached,
            force_redeclare=force_redeclare,
            raise_if_not_cached=raise_if_not_cached,
            # Queue args below
            ensured_connection=self.ensured_connection,
            name=queue_name,
            routing_key=routing_key,
            exchange=exchange,
            passive=passive,
            durable=durable,
            exclusive=exclusive,
            auto_delete=auto_delete,
            no_declare=no_declare,
            queue_arguments=queue_arguments
        )

    def force_declare_queue(self, queue_name, **kwargs):
        return self.get_cached_queue(queue_name, force_redeclare=True, **kwargs)

    def get_cached_tmp_queue(self,
                             routing_key=None,
                             exchange=None,
                             exclusive=False,
                             passive=False,
                             queue_expiration=QUEUE_EXPIRATION,
                             message_expiration=MESSAGE_EXPIRATION,
                             no_declare=False,
                             force_redeclare=False,
                             raise_if_not_cached=False):

        if routing_key is None:
            # Cannot rely on generated queues because
            # it either bind to default exchange with a routing key or
            # bind to a non default exchange without routing key. (too bad)
            routing_key = 'tmp.' + str(uuid.uuid4())

        return self.get_cached_queue(queue_name=routing_key,
                                     routing_key=routing_key,
                                     exchange=exchange,
                                     passive=passive,
                                     durable=False,
                                     exclusive=exclusive,
                                     auto_delete=True,
                                     no_declare=no_declare,
                                     queue_arguments={
                                         "x-expires": queue_expiration,
                                         "x-message-ttl": message_expiration,
                                     },
                                     force_redeclare=force_redeclare,
                                     raise_if_not_cached=raise_if_not_cached)

    def force_declare_tmp_queue(self, **kwargs):
        return self.get_cached_tmp_queue(force_redeclare=True, **kwargs)

    # LRUConsumer functions

    def get_cached_lru_consumer(self,
                                queues,
                                tag_prefix=None,
                                force_redeclare=False,
                                raise_if_not_cached=False,
                                **kwargs):
        if tag_prefix is None:
            tag_prefix = default_tag_prefix()

        return self.__get_or_declare(
            tag_prefix,
            self.cache.get_consumer,
            LRUConsumer,
            ConsumerNotCached,
            force_redeclare=force_redeclare,
            raise_if_not_cached=raise_if_not_cached,
            # LRUConsumer args below
            ensured_connection=self.ensured_connection,
            queues=queues,
            tag_prefix=tag_prefix,
            **kwargs
        )

    def force_declare_lru_consumer(self, queues, tag_prefix=None, **kwargs):
        return self.get_cached_lru_consumer(queues, tag_prefix=tag_prefix,
                                            force_redeclare=True, **kwargs)

    # Exchanges and send functions

    def __create_exchange(self, exchange_name, exchange_type):
        # Use get_cached_exchange or force_declare_exchange instead of this function
        exchange = kombu.Exchange(exchange_name, type=exchange_type,
                                  channel=self.ensured_connection)
        self.ensure_and_hearbeat(exchange, exchange.declare)
        return exchange

    def get_cached_exchange(self, exchange_name, exchange_type='direct', force_redeclare=False, raise_if_not_cached=False):
        return self.__get_or_declare(
            exchange_name,
            self.cache.get_exchange,
            self.__create_exchange,
            ExchangeNotCached,
            force_redeclare=force_redeclare,
            raise_if_not_cached=raise_if_not_cached,
            # Exchange args below
            exchange_name=exchange_name,
            exchange_type=exchange_type,
        )

    def force_declare_exchange(self, exchange_name, **kwargs):
        return self.get_cached_exchange(exchange_name, force_redeclare=True, **kwargs)

    def send(self, data, routing_key, exchange=None, encoder=None, **properties):

        if exchange is None:
            exchange = self.get_cached_exchange(DEFAULT_EXCHANGE, 'direct')

        if encoder:
            data = encoder(data)

        if 'correlation_id' not in properties:
            properties['correlation_id'] = str(uuid.uuid4())

        self.ensure_and_hearbeat(self.producer,
                                 self.producer.publish,
                                 body=data,
                                 exchange=exchange,
                                 routing_key=routing_key,
                                 retry=False,  # retry is done by ensure_and_heartbeat
                                 **properties)

        return properties.get('correlation_id')

    def send_binary(self, binary_data, routing_key, exchange=None, **properties):
        properties['content_encoding'] = 'binary'
        properties['content_type'] = 'application/octet-stream'
        return self.send(binary_data,
                         routing_key=routing_key,
                         exchange=exchange,
                         **properties)

    def send_to_queue(self, queue, *args, **kwargs):
        return self.send(*args, routing_key=queue.routing_key, exchange=queue.exchange, **kwargs)

    def remove_from_cache(self, entity):
        return self.cache.remove(entity)


class RPCStream(object):
    '''
    Represents a RPC stream.
    Push messages to the command_queue and consume the response from the response_queue.
    This class is not thread safe and you are responsible to call get_next_response to avoid the correlation_ids list to grow.
    '''

    def __init__(self, amqp_client, command_queue_name, response_queue_name=None, exchange_name=None, exchange_type='direct', max_cache_msg=100, msg_wrapper=None, keep_response_order=True):
        self.amqp_client = amqp_client
        self.msg_wrapper = msg_wrapper
        self.keep_response_order = keep_response_order
        self.amqp_exchange = self.amqp_client.force_declare_exchange(exchange_name,
                                                                     exchange_type=exchange_type)
        self.command_queue = self.amqp_client.force_declare_queue(command_queue_name, exchange=self.amqp_exchange)
        if response_queue_name is None:
            self.response_queue = self.amqp_client.force_declare_tmp_queue(exchange=self.amqp_exchange)
        else:
            self.response_queue = self.amqp_client.force_declare_queue(response_queue_name, exchange=self.amqp_exchange)
        self.consumer = self.amqp_client.force_declare_lru_consumer([self.response_queue],
                                                                    max_cache_msg=max_cache_msg,
                                                                    msg_wrapper=msg_wrapper)
        self.consumer.consume()
        self.correlation_ids = []

    def remove_command_queue(self):
        self.amqp_client.remove_from_cache(self.command_queue)
        self.command_queue.delete()

    def send_binary(self, binary_data):
        correlation_id = self.amqp_client.send_binary(binary_data,
                                                      routing_key=self.command_queue.routing_key,
                                                      exchange=self.amqp_exchange,
                                                      reply_to=self.response_queue.name)
        if self.keep_response_order:
            self.correlation_ids.append(correlation_id)
        return correlation_id

    def get_next_response(self, timeout=float('inf'), drain_events_timeout=0.005):
        correlation_id = None
        if self.keep_response_order:
            correlation_id = self.correlation_ids.pop(0)

        msg = self.consumer.get(correlation_id=correlation_id,
                                timeout=timeout,
                                drain_events_timeout=drain_events_timeout)
        if msg is None:
            if self.keep_response_order:
                self.correlation_ids.insert(0, correlation_id)
        return msg

    def close(self):
        if self.amqp_client is not None:
            # Cancel the consumer
            # Remove the response queue if it temporary
            # Doesn't delete the command queue, you must do it manually
            self.amqp_client.remove_from_cache(self.consumer)
            self.consumer.cancel()

            if not self.response_queue.durable:
                self.amqp_client.remove_from_cache(self.response_queue)
                self.response_queue.delete()

            self.amqp_client = None

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def __del__(self):
        self.close()


class RPCClient(object):
    '''
    A client that always use the same exchange and provides functions to help doing RPC.
    This class is not thread safe. You might need to create one client that pushes commands and one that consume.
    '''

    def __init__(self, amqp_url, exchange_name='v0.3.direct', exchange_type='direct'):
        self.amqp_client = Client(amqp_url)
        self.amqp_exchange = self.amqp_client.force_declare_exchange(exchange_name,
                                                                     exchange_type=exchange_type)

    def new_stream(self, command_queue_name, **kwargs):
        kwargs['exchange_name'] = kwargs.get('exchange_name', self.amqp_exchange.name)
        kwargs['exchange_type'] = kwargs.get('exchange_type', self.amqp_exchange.type)
        return RPCStream(self.amqp_client, command_queue_name, **kwargs)

    # Below low level functions to have more control on the RPC

    def new_queue(self, queue_name=None):
        # Declare a queue, if queue_name is None, declare a temporary queue
        if queue_name is None:
            return self.amqp_client.force_declare_tmp_queue(exchange=self.amqp_exchange)
        return self.amqp_client.force_declare_queue(queue_name, exchange=self.amqp_exchange)

    def new_consuming_queue(self, queue_name=None, max_cache_msg=100, msg_wrapper=None):
        # Declare the queue and a consumer
        queue = self.new_queue(queue_name)
        consumer = self.amqp_client.force_declare_lru_consumer([queue], max_cache_msg=max_cache_msg, msg_wrapper=msg_wrapper)
        consumer.consume()
        return queue, consumer

    @contextmanager
    def tmp_consuming_queue(self, **kwargs):
        queue, consumer = self.new_consuming_queue(queue_name=None, **kwargs)
        yield queue, consumer
        self.remove_consumer(consumer)
        self.remove_queue(queue)

    def remove_consumer(self, consumer):
        self.amqp_client.remove_from_cache(consumer)
        consumer.cancel()

    def remove_queue(self, queue):
        # Remove any type of queue
        self.amqp_client.remove_from_cache(queue)
        queue.delete()

    def remove_consuming_queue(self, queue, consumer):
        # Cancel consumer and remove queue
        # Remove them both from the cache to avoid being redeclared later
        self.remove_consumer(consumer)
        self.remove_queue(queue)

    def send_binary(self, binary_data, command_queue_name, **properties):
        return self.amqp_client.send_binary(binary_data,
                                            routing_key=command_queue_name,
                                            exchange=self.amqp_exchange,
                                            **properties)

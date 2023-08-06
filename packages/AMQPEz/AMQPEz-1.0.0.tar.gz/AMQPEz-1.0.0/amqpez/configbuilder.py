from . import AMQPEzConfig
import pika as p

class AMQPEzConfigBuilder:
    def __init__(self):
        self.target_config = AMQPEzConfig()
        self.connection_set = None

    def add_connection_params(self, host, port = 5672, vhost = '/'):
        if self.connection_set: raise ValueError("Cannot set connection parameters twice")
        self.connection_set = 'default'
        self.target_config.host = host
        self.target_config.port = port
        self.target_config.vhost = vhost
        return self

    def add_connection_url(self, url):
        if self.connection_set: raise ValueError("Cannot set connection parameters twice")
        self.connection_set = 'url'
        self.pikaparams = p.URLParameters(url)
        return self
    
    def add_basic_credentials(self, user, password):
        self.target_config.credentials = p.PlainCredentials(user, password)
        return self

    def add_external_credentials(self, external_creds):
        self.target_config.credentials = p.ExternalCredentials(external_creds)
        return self

    def add_exchange(self, exchange, exchange_type = 'direct', routing_key = ''):
        self.target_config.exchange = exchange
        self.target_config.exchange_type = exchange_type
        self.target_config.routing_key = routing_key
        return self

    def add_queue(self, queue):
        self.target_config.input_queue = queue
        return self

    def add_serializers(self, serializer, deserializer):
        self.target_config.serializer = serializer
        self.target_config.deserializer = deserializer
        return self

    def add_deserializer(self, deserializer):
        self.target_config.deserializer = deserializer
        return self

    def add_task(self, task):
        self.target_config.task = task
        return self

    def add_qos(self, prefetch_count):
        self.target_config.prefetch_count = prefetch_count
        return self

    def build(self):
        if self.connection_set == 'default':
             self.target_config.pikaparams = p.ConnectionParameters(
                host =  self.target_config.host,
                virtual_host =  self.target_config.vhost,
                port =  self.target_config.port,
                credentials =  self.target_config.credentials
            )
        return self.target_config
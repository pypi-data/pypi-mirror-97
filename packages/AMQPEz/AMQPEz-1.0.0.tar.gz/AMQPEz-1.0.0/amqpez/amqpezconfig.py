import pika as p
class AMQPEzConfig:
    def __init__(self, host = "localhost", 
                       input_queue = "amqpez_input", 
                       exchange = "amqpez_exchange",
                       task = lambda x:x,
                       user = "guest",
                       password = "guest",
                       exchange_type = "direct",
                       routing_key = "",
                       deserializer = lambda x:x, 
                       serializer = lambda x:x,
                       prefetch_count = 1,
                       vhost = '/',
                       port = 5672):
        self.host = host
        self.deserializer = deserializer
        self.serializer = serializer
        self.input_queue = input_queue
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.routing_key = routing_key
        self.task = task
        self.prefetch_count = prefetch_count


        self.credentials = p.PlainCredentials(user, password)

        self.pikaparams = p.ConnectionParameters(
                host =  self.host,
                virtual_host =  vhost,
                port =  port,
                credentials =  self.credentials
            )

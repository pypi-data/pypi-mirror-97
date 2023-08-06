import pika as p
import logging
import functools

class AMQPEz:
    def __init__(self, configuration):
        self.config_ = configuration
        self.logger = self.initialize_logger_()
        
        self.consuming = False
        self.draining = False

    def start(self):
        self.connection_ = self.create_connection_()
        self.connection_.ioloop.start()

    def stop(self):
        self.logger.info("Stopping...")
        if not self.draining:
            self.draining = True
            if self.consuming:
                self.stop_consuming_()
                self.connection_.ioloop.start()
            else:
                self.connection_.ioloop.stop()
            self.logger.info("Stopped")

    def create_connection_(self):
        return p.SelectConnection(
            parameters = self.config_.pikaparams,
            on_open_callback=self.on_connection_opened_,
            on_open_error_callback=self.on_connection_open_error_,
            on_close_callback=self.on_connection_closed_
        )

    def on_connection_opened_(self, connection): 
        self.logger.info("Connection opened")

        connection.channel(on_open_callback=self.on_channel_openened_)

    def on_connection_open_error_(self, connection, error):
        self.logger.error("Connection opening errored with the following %s"%error)

    def on_connection_closed_(self, connection, reason):
        if self.draining:
            self.connection_.ioloop.stop()
            self.logger.info("Connection closed expectedly")
        else:
            self.logger.info("Connection closed with the following reason: %s"%reason)

    def on_channel_openened_(self, channel):
        self.logger.info("Opened channel")
        # register exit callback
        self.channel_ = channel

        self.channel_.add_on_close_callback(self.on_channel_closed_)

        self.assert_topology_()

    def on_channel_closed_(self, channel, reason):
        self.logger.info("Channel closed because of %s"%reason)
        
        self.consuming = False

        if self.connection_.is_closing or self.connection_.is_closed:
            self.logger.warn("Tried to close an already closing connection")
        else:
            self.logger.info("Closing connection")
            self.connection_.close()

    def assert_topology_(self): 
        if self.config_.input_queue and self.config_.exchange:
            self.channel_.exchange_declare(
                exchange=self.config_.exchange,
                exchange_type=self.config_.exchange_type,
                callback = lambda _:
                self.channel_.queue_declare(queue=self.config_.input_queue, callback=self.on_topology_asserted_)
            )
        else:
            self.channel_.queue_declare(queue=self.config_.input_queue, callback=self.on_topology_asserted_)
            
    def on_topology_asserted_(self, frame):
        self.logger.info("Topology asserted")
        #self.channel_.confirm_delivery(self.on_message_published) # for publisher confirms
        self.channel_.basic_qos(prefetch_count=self.config_.prefetch_count, 
            callback=lambda _:self.start_consuming_())

    def on_message_published(self, info):
        ## in the future this would be nice to do publisher confirms
        pass

    def start_consuming_(self):
        self.logger.info("Starting consumption")
        self.channel_.add_on_cancel_callback(self.on_consumer_cancelled_)

        self.consumer_tag_ = self.channel_.basic_consume(
            self.config_.input_queue, self.handle_message_
        )
        self.consuming = True

    def stop_consuming_(self):
        if self.channel_: self.channel_.basic_cancel(self.consumer_tag_, self.on_cancelled)

    def on_cancelled(self, frame):
        self.consuming = False
        self.channel_.close()
        self.logger.info("Closed channel")

    def handle_message_(self, channel, deliver, props, message):
        deserialized = self.config_.deserializer(message)
        self.logger.info("Got message %s"%deserialized)

        result = self.config_.task(deserialized)

        if not result: self.channel_.basic_nack(deliver.delivery_tag); return

        serialized = self.config_.serializer(result)

        self.logger.info("Produced message %s"%result)


        if self.config_.exchange: # produce output
            self.channel_.basic_publish(self.config_.exchange, self.config_.routing_key, serialized)

            self.channel_.basic_ack(deliver.delivery_tag) # delete this incase of publisher confirms
        else:
            self.channel_.basic_ack(deliver.delivery_tag)

    def on_consumer_cancelled_(self, frame):
        self.logger.info("Consumer cancelled")
        if self.channel_: self.channel_.close()

    def initialize_logger_(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
        ch.setFormatter(formatter)

        logger.addHandler(ch)

        return logger

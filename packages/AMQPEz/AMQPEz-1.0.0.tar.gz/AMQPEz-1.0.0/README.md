# AMQPEz
Personal library for spinning up quick AMQP shoveling applications, which allows for mid-transit transforms, contrary to rabbitmq-shovel. See this [Example](examples/addfive.py).
## Install
Simply run
```sh
pip3 install AMQPEz
```
## Basics
Essentially you build your configuration 
```python3
conf = AMQPEzConfigBuilder() \
        .add_connection_params("localhost") \
        .add_basic_credentials("guest", "guest") \
        .add_exchange("test_exchange") \
        .add_queue('test_queue') \
        .add_serializers(serialize, deserialize) \
        .add_task(lambda x: x+5) \
        .add_qos(1) \
        .build() 
```
And start your shovel, which runs the specified task (here we add 5).
```python3
amqpez = AMQPEz(conf)
try:
    amqpez.start()
except KeyboardInterrupt:
    amqpez.stop()
```
The consumer is quite similar to a very standard pika async consumer. It will include ISID tracking to tackle publish network timeouts in a future update. This also works seemlessly with protobuf, since you essentially plug all serialization.
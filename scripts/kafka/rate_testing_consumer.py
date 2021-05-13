from kafka import KafkaConsumer

consumerConfig = {
    'bootstrap_servers': '192.168.39.2:9092',
    #'auto_offset_reset': 'earliest',
}

consumer = KafkaConsumer('test_rate', **consumerConfig)

msg_recv = 0

try:
    for msg in consumer:
        msg_recv += 1
except KeyboardInterrupt:
    print("stopping consumer")
    print(msg_recv)

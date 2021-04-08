from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='192.168.39.2:9092')

for i in range(10):
    producer.send('test_topic', b'whoaoaoaoao')
    print(f'sent {i}')

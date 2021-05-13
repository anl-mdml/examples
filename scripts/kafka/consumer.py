from kafka import KafkaConsumer
consumer = KafkaConsumer('test_topic', bootstrap_servers='192.168.39.2:9092')

for msg in consumer:
    print(msg)

from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='192.168.39.2:9092')

dat = bytes("0123456789"*1000,'utf-8')
for i in range(1001):
    producer.send('test_rate', dat)
producer.close()

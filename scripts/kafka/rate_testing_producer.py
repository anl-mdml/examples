from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='192.168.39.2:9092')

dat = bytes("testing data transfer rate",'utf-8')
for i in range(1):
    producer.send('test_rate', dat)

from kafka import KafkaConsumer
import json

def get_messages(topic):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        group_id=None
    )
    return [json.loads(msg.value.decode()) for msg in consumer]

m1 = get_messages("saida_main")
m2 = get_messages("saida_feature")

if m1 != m2:
    print("As branches produzem resultados diferentes:")
    print("main:", m1)
    print("feature:", m2)
    exit(1)
else:
    print("As branches são comportamentalmente idênticas!")
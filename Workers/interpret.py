import os
import sys
import json
import openai
from openai import OpenAI
from dotenv import load_dotenv
from kafka import KafkaConsumer, KafkaProducer, TopicPartition
# from grpc.interpretation_pb2 import interpretation

load_dotenv()
debug = bool(os.environ.get("debug"))

INTP_RECV_BROKER = 'localhost:9092'
INTP_RECV_TOPIC = 'Interpretation'

INTP_RESP_BROKER = 'localhost:9093'
INTP_RESP_TOPIC = 'InterpretationResponse'

BACKRGOUND_PROMPT = "You are a docter, skilled in explaining complex medical terms to patients whom with no professional backgroud. You will directly give your explanation with middle school level semantics in {}."

client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY"),
)

def get_response(language, userInput):
    try:
        if debug: print("start to acquire response...")
        _response = client.chat.completions.create(
            model = "gpt-3.5-turbo-0125",
            messages = [
                {
                    "role":"system",
                    "content": BACKRGOUND_PROMPT.format(language),
                },
                {
                    "role":"user",
                    "content": userInput,
                }
            ]
        )
        response = _response.choices[0].message.content
        if debug:
            print(response)
        return True, response
    except openai.APIConnectionError as e:
        return False, "Failed to connect to OpenAI API"
    except openai.RateLimitError as e:
        return False, "Exceed current quota"
    except Exception as e:
        return False, e.__context__

def main():
    p_num = [int(arg) for arg in sys.argv[1:]]
    consumer = KafkaConsumer(
        bootstrap_servers = [INTP_RECV_BROKER],
        max_poll_records = 1)
    consumer.assign([TopicPartition(INTP_RECV_TOPIC, p) for p in p_num])
    producer = KafkaProducer(
        bootstrap_servers = [INTP_RESP_BROKER],
        acks = "all",
        retries = 10
    )
    while True:
        batch = consumer.poll(1000)
        for _, messages in batch.items():
            for message in messages:
                interpretation_msg = interpretation()
                interpretation_msg.ParseFromString(message.value)
                language = interpretation_msg.language
                userInput = interpretation_msg.content
                status, response = get_response(language, userInput)
                proto_interpretation = interpretation(status = ("Successful" if status else "Failed"), langauge = language, content = response)
                proto_value = proto_interpretation.SerializeToString()
                producer.send(INTP_RESP_TOPIC, value = proto_value)
        

if __name__ == '__main__':
    main()
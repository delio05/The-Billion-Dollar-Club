import os
import sys
import csv
from dotenv import load_dotenv
from kafka import KafkaConsumer, TopicPartition
from grpc.feedback_pb2 import feedback

load_dotenv()
debug = bool(os.environ.get("debug"))

totalFeedback = 0
positiveFeedback = 0

FDBK_RECV_BROKER = 'localhost:9094'
FDBK_RECV_TOPIC = 'Feedback'

def main():
    p_num = [int(arg) for arg in sys.argv[1:]]
    consumer = KafkaConsumer(
        bootstrap_servers = [FDBK_RECV_BROKER])
    consumer.assign([TopicPartition(FDBK_RECV_TOPIC, p) for p in p_num])
    while True:
        batch = consumer.poll(1000)
        for _, messages in batch.items():
            for message in messages:
                feedback_msg = feedback()
                feedback_msg.ParseFromString(message.value)
                attitude = feedback_msg.attitude
                userFeedback = feedback_msg.userFeedback
                fields = [attitude, userFeedback]

                with open("data/feedback.csv", "a") as f:
                    writer = csv.writer(f)
                    writer.writerow(fields)

                
                totalFeedback += 1
                if attitude == 'positive':
                    positiveFeedback += 1
                if debug: 
                    print("Current total feedback: " + totalFeedback + " with positive feedback rate: " + 100*(positiveFeedback/totalFeedback))
    

if __name__ == '__main__':
    main()
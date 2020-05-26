import time
import pika


class AIServer:
    def __init__(self, rabbitmq_url, prefetch_count, input_queue_name, output_queue_name):
        self.input_queue_name = input_queue_name
        self.output_queue_name = output_queue_name
        self.pika_channel = pika.BlockingConnection(pika.URLParameters(rabbitmq_url)).channel()
        self.pika_channel.basic_qos(prefetch_count=prefetch_count)
        self.pika_channel.queue_declare(queue=input_queue_name, durable=True)
        self.pika_channel.queue_declare(queue=output_queue_name, durable=True)

    def main(self, wait_time, queue_size):
        self.__load_model__()
        while True:
            body_list, delivery_tag_list = self.__get_message_list__(queue_size)
            if not body_list:
                time.sleep(wait_time)
                continue
            result_list = self.__predict__(body_list)
            for idx in range(len(result_list)):
                self.__put_message__(result_list[idx])
                self.pika_channel.basic_ack(deivery_tag=delivery_tag_list[idx])

    def __load_model__(self):
        pass

    def __predict__(self, body_list):
        return []

    def __get_message_list__(self, queue_size):
        return_list = []
        delivery_tag_list = []
        while True:
            method_frame, _, body = self.pika_channel.basic_get(self.input_queue_name)
            if method_frame:
                return_list.append(body)
                delivery_tag_list.append(method_frame.delivery_tag)
                if len(return_list) >= queue_size:
                    return return_list, delivery_tag_list
            else:
                return return_list, delivery_tag_list

    def __put_message__(self, message):
        self.pika_channel.basic_publish(
            routing_key=self.output_queue_name,
            body=message,
            exchange="",
            properties=pika.BasicProperties(delivery_mode=2),
        )

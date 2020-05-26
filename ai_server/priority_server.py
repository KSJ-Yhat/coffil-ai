from ai_server.ai_server import AIServer
import json

EXAMPLE_JSON = {
    "url": "http://abc.com/",
    "id": "abcd",
    "previous_score": 10,
    "rule_base_score": 20,
    "ai_priority_score": 0,
    "aging_score": 40,
}


class PriorityPredictor(AIServer):
    def __load_model__(self):
        pass

    def __predict__(self, body_list):
        json_list = []
        for body in body_list:
            json_list.append(json.loads(body))

        batch_list = []
        for j in json_list:
            batch_list.append(j["url"])

        # TODO: batch predict
        predict_result = []
        message_list = []
        for idx, j in enumerate(json_list):
            j["ai_priority_score"] = predict_result[idx]
            message_list.append(json.dumps(j))
        return message_list

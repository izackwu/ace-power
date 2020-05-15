import json
import random
import time
from locust import HttpLocust, TaskSet, task, between


class UserBehavior(TaskSet):
    __Q_LIST = []
    __Q_FILENAME = 'names.txt'

    def setup(self):
        with open(self.__Q_FILENAME, 'r') as f:
            for line in f:
                self.__Q_LIST.append(line.strip('\n'))

    @task
    def random_query(self):
        q = self._get_q()
        while True:
            with self.client.get('/search/{}'.format(q), catch_response=True) as response:
                data = json.loads(response.content)
                if data["status"]:
                    break
                else:
                    time.sleep(data["waiting"])
                    # response.failure("No immediately available results")

    def _get_q(self):
        return random.choice(self.__Q_LIST)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5.0, 9.0)
    host = "http://localhost:8000"


if __name__ == "__main__":
    import os

    # ps -ef|grep locust |grep -v grep|awk '{print $2}'|xargs kill
    # os.system("nohup locust -f locust_test.py >> test.log &")
    os.system("locust -f locust_test.py")

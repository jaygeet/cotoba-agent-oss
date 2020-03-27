"""
Copyright (c) 2020 COTOBA DESIGN, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
# Emulating the following curl request in locust
#  curl 'http://localhost:5000/api/v1.0/ask?question=hello+world&sessionid=1234567890'

import random
from urllib.parse import urlencode
from locust import HttpLocust, TaskSet

questions = [
    "ASKWIKIPEDIA KEITH STERLING",
    "ASKWIKIPEDIA AIML",
    "ASKWIKIPEDIA PYTHON PROGRAMMING",
    "ASKWIKIPEDIA Edinburgh Festival Fringe",
    "ASKWIKIPEDIA FanDuel"
]

sessionids = [
    "111111111",
    "222222222",
    "333333333",
    "444444444",
    "555555555",
    "666666666",
    "777777777"
]


def ask(l):
    question_no = random.randint(0, len(questions)-1)
    sessionid_no = random.randint(0, len(sessionids)-1)

    data = {"question": questions[question_no],
            "sessionid": sessionids[sessionid_no]
            }
    url = "/api/v1.0/ask?" + urlencode(data)

    with l.client.get(url) as response:
        print("[%d] - [%s]" % (response.status_code, response.content))
        if response.status_code != 200:
            response.failure("Invalid bot response")


class UserBehavior(TaskSet):
    tasks = {ask: 1}


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 5000
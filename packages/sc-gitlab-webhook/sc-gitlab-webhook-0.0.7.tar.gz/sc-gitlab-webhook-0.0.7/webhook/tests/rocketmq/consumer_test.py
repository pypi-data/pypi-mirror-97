# The MIT License (MIT)
#
# Copyright (c) 2021 Scott Lau
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import logging
import time

from rocketmq.client import PushConsumer, ConsumeStatus
from scutils import log_init


class Consumer:

    def callback(self, msg):
        logging.getLogger(__name__).info("%s, %s", msg.id, msg.body)
        return ConsumeStatus.CONSUME_SUCCESS

    def consume(self):
        consumer = PushConsumer('CID_XXX')
        consumer.set_name_server_address('127.0.0.1:9876')
        consumer.subscribe('YOUR-TOPIC', self.callback)
        consumer.start()

        while True:
            time.sleep(3600)
        consumer.shutdown()


if __name__ == '__main__':
    log_init()
    consumer = Consumer()
    consumer.consume()

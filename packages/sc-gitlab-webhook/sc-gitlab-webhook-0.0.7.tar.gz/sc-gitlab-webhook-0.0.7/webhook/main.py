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

"""The Main routine

Copyright (c) 2021 Scott Lau
"""

import logging

from scutils import Singleton
from scutils import log_init

from webhook import server
from webhook.producer import ScProducer
from webhook.utils import config


class Runner(metaclass=Singleton):
    _producer: ScProducer = None

    def __init__(self):
        self._producer = ScProducer()

    def run(self):
        dev_mode = False
        try:
            dev_mode = config.get("dev.dev_mode")
        except AttributeError:
            pass
        logging.getLogger(__name__).info('program is running in development mode: {}'.format(dev_mode))
        # start producer
        self._producer.start()
        # start flask server
        server_ip = config.get("server.ip")
        server_port = config.get("server.port")
        server.run(host=server_ip, port=server_port)
        # stop producer
        self._producer.shutdown()
        return 0


def main():
    try:
        log_init()
        state = Runner().run()
    except Exception as e:
        logging.getLogger(__name__).exception('An error occurred.', exc_info=e)
    else:
        return state

    return 0


if __name__ == '__main__':
    main()

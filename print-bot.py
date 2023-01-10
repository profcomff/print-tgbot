# print-bot
# for https://vk.com/profcomff

# Marakulin Andrey @annndruha
# 2021
import time
import logging
from threading import Thread

import core.chat as chat

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')

    chat_thread = Thread(target=chat.chat_loop)
    chat_thread.start()

    time.sleep(1)
    logging.info("=== BOT START ===")

    chat_thread.join()

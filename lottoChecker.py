#-*- coding: utf-8 -*-

import key
import time
import threading
import lottoFunc as func
from telegram.ext import Updater, MessageHandler, Filters

# https://t.me/lottochecker_bot

def main():
    # updater : , dispatcher : 
    updater = Updater(token=key.token, use_context=True)
    dispatcher = updater.dispatcher

    # 입력받은 메시지 유형이 text(message) 인 경우, echo 함수 실행
    echo_handler = MessageHandler(Filters.text, func.echo)
    dispatcher.add_handler(echo_handler)

    # polling (handler/dispatcher loop)
    updater.start_polling()
    updater.idle()

    # Threading
    # t = threading.Thread(target=func, args=(1,))
    # t.start()


if __name__ == "__main__":
    main()
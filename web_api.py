from socket import socket, getaddrinfo
from time import sleep
from utils import url_encode
from credentials import SERVER_IP, SERVER_PORT
from constants import OK, WEB_OK


def search_user(user_card: str) -> tuple[int, str]:
    encoded_data = url_encode(user_card).encode()
    addr_info = getaddrinfo(SERVER_IP, SERVER_PORT)

    addr = addr_info[-1][-1]
    print("Connect address:", addr)

    while True:
        soc = socket()
        try:
            soc.connect(addr)
        except:
            continue
        soc.send(b"GET /search-user?user-card=" + encoded_data + b" HTTP/1.0\r\n\r\n")
        res = soc.recv(4096).decode()
        if len(res) > 200:
            start_index = res.find("{")
            stop_index = res.find("}", start_index) + 2
            print("RES:", res, len(res))
            data = dict(eval(res[start_index:stop_index]))

            status = data.get("status")
            message = data.get("message")

            # y = 40 + font_height + MENU_ITEM_MARGIN_TOP
            if status != "error":
                if status == "success":
                    return OK, "Your slot is empty"
                elif status == "warning":
                    return -1, "Your slot is taken"
            else:
                return OK + 1, "That card is not registered into the system"
        soc.close()
        sleep(1)

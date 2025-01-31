import random
from time import sleep

from websockets.sync.client import connect

def hello():
    with connect("ws://localhost:8765") as websocket:
        random_number = random.randint(1, 100)
        while True:
            websocket.send(f"Hello world! {random_number}")
            websocket.send(f"Hello world! {random_number}")
            message = websocket.recv()
            print(f"Received: {message}")
            sleep(0.5)


hello()
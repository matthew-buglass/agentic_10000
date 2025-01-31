import random
from time import sleep

from websockets.sync.client import connect
# Read through this tutorial to see if there is a better way https://theredrad.medium.com/designing-a-distributed-system-for-an-online-multiplayer-game-basics-part-1-17c149245bd2
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
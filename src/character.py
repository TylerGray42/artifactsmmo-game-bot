import time
import requests
import jsonpath_ng as jp

class Character:
    def __init__(self, name:str, token:str):
        self.server = "https://api.artifactsmmo.com"
        self.name = name
        self.token = token
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

        self.cooldown_query = jp.parse("$..cooldown.total_seconds")
        self.destination_query = jp.parse("$..destination")

    def __send_request(self, action:str, data=None):
        url = self.server + "/my/" + self.name + "/action/" + action

        response = requests.post(url, headers=self.headers, json=data).json()

        # print(response)

        destination = None

        for match in self.destination_query.find(response):
            destination = match.value

        if destination:
            print("Destination Info:\n"
                f"Name: {destination.get('name', 'Unknown')}\n"
                f"Coordinates: (X: {destination.get('x', 'Unknown')}, Y: {destination.get('y', 'Unknown')})\n"
                f"Content: {destination.get('content', 'Unknown')}")

        cooldown = 0

        for match in self.cooldown_query.find(response):
            cooldown = match.value

        print(f"---\nCooldown: {cooldown} sec\n---")
        time.sleep(cooldown)


    def move(self, x:int, y:int):
        data = {"x": x, "y": y}
        self.__send_request("move", data)

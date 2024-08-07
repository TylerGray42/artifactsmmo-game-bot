import time
import requests
from .response_handler import ResponseHandler


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

        self.response_handler = ResponseHandler()


    def __send_request(self, action:str, data=None):
        url = self.server + "/my/" + self.name + "/action/" + action
        response = requests.post(url, headers=self.headers, json=data)
        try:
            response = response.json()
        except:
            print(f"\n\n\n{response}\n\n")
            return
        self.response_handler.handle_response(action, response)


    def get_info(self):
        url = self.server + "/characters/" + self.name
        response = requests.get(url, headers=self.headers).json()
        print(response)


    def move(self, x:int, y:int):
        data = {"x": x, "y": y}
        self.__send_request("move", data)


    def fight(self):
        self.__send_request("fight")


    def gathering(self):
        self.__send_request("gathering")


    def equip(self, code:str, slot:str):
        data = {"code": code, "slot": slot}
        self.__send_request("equip", data)


    def unequip(self, slot:str):
        data = {"slot": slot}
        self.__send_request("unequip", data)


    def crafting(self, code:str, quantity:int = 1):
        data = {"code": code, "quantity": quantity}
        self.__send_request("crafting", data)

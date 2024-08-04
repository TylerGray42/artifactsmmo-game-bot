import time
import jsonpath_ng as jp


class ResponseHandler:
    def __init__(self):
        self.cooldown_query = jp.parse("$..cooldown.total_seconds")
        self.destination_query = jp.parse("$..destination")
        self.fight_query = jp.parse("$..fight.xp,gold,drops,result")
        self.gathering_query = jp.parse("$..details.xp,items")


    def handle_response(self, action:str, response: dict):
        match action:
            case "move":
                self.__handle_move(response)
            case "fight":
                self.__handle_fight(response)
            case "gathering":
                self.__handle_gathering(response)
            case _:
                pass

        self.__handle_cooldown(response)


    def __handle_move(self, response: dict):
        destination = None

        for match in self.destination_query.find(response):
            destination = match.value

        if destination:
            print("Destination Info:\n"
                f"  Name: {destination.get('name', 'Unknown')}\n"
                f"  Coordinates: (X: {destination.get('x', 'Unknown')}, Y: {destination.get('y', 'Unknown')})\n"
                f"  Content: {destination.get('content', 'Unknown')}")


    def __handle_fight(self, response: dict):
        xp, gold, drops, result = [match.value for match in self.fight_query.find(response)]
        print("Fight Info:\n"
            f"  Result: {result}\n"
            f"  XP gained: {xp}, Gold: {gold}\n"
            f"  Drops: {drops}")


    def __handle_gathering(self, response: dict):
        xp, items = [match.value for match in self.gathering_query.find(response)]
        print("Gathering Info:\n"
            f"  XP gained: {xp}\n"
            f"  Items: {items}")


    def __handle_cooldown(self, response: dict):
        cooldown = 0

        for match in self.cooldown_query.find(response):
            cooldown = match.value

        print(f"---\nCooldown: {cooldown} sec ({time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})\n---")
        time.sleep(cooldown)

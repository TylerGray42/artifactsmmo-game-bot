import time
import jsonpath_ng as jp


class ResponseHandler:
    def __init__(self):
        self.error_query = jp.parse("$.error.code,message,data")

        self.cooldown_query = jp.parse("$..cooldown.total_seconds")
        self.destination_query = jp.parse("$..destination")
        self.fight_query = jp.parse("$..fight.xp,gold,drops,result")
        self.gathering_query = jp.parse("$..details.xp,items")
        self.unequip_query = jp.parse("$..item.name,code,level,type,subtype,description,effects")
        self.equip_query = jp.parse("$..item.name,code,level,type,subtype,description,effects")
        self.crafting_query = jp.parse("$..details.xp,items")

        self.character_info_query = jp.parse("$.data.name,level,hp,xp,max_xp,gold,speed,x,y")
        self.character_skills_query = jp.parse("$.data.mining_level,mining_xp,mining_max_xp,\
                                    woodcutting_level,woodcutting_xp,woodcutting_max_xp,\
                                    fishing_level,fishing_xp,fishing_max_xp,\
                                    weaponcrafting_level,weaponcrafting_xp,weaponcrafting_max_xp,\
                                    gearcrafting_level,gearcrafting_xp,gearcrafting_max_xp,\
                                    jewelrycrafting_level,jewelrycrafting_xp,jewelrycrafting_max_xp,\
                                    cooking_level,cooking_xp,cooking_max_xp")
        self.character_stats_query = jp.parse("$.data.haste,critical_strike,stamina,\
                                    attack_fire,dmg_fire,res_fire,\
                                    attack_earth,dmg_earth,res_earth,\
                                    attack_water,dmg_water,res_water,\
                                    attack_air,dmg_air,res_air")
        self.character_equipment_query = jp.parse("$.data.weapon_slot,shield_slot,\
                                    helmet_slot,body_armor_slot,leg_armor_slot,boots_slot,\
                                    ring1_slot,ring2_slot,amulet_slot,\
                                    artifact1_slot,artifact2_slot,artifact3_slot,\
                                    consumable1_slot,consumable1_slot_quantity,consumable2_slot,consumable2_slot_quantity")
        self.character_task_query = jp.parse("$.data.task,task_type,task_progress,task_total")
        self.character_inventory_query = jp.parse("$.data.inventory_max_items,inventory")
        self.all_quantity_query = jp.parse("$..inventory[*].quantity")


    def handle_response(self, action:str, response: dict):
        error = [match.value for match in self.error_query.find(response)]
        if error:
            self.__handle_error(error)
            return

        match action:
            case "move":
                self.__handle_move(response)
            case "fight":
                self.__handle_fight(response)
            case "gathering":
                self.__handle_gathering(response)
            case "equip":
                self.__handle_equip(response)
            case "unequip":
                self.__handle_unequip(response)
            case "crafting":
                self.__handle_crafting(response)
            case "character_info":
                self.__handle_character_info(response)
            case "skills":
                self.__handle_character_skills(response)
            case "stats":
                self.__handle_character_stats(response)
            case "equipment":
                self.__handle_character_equipment(response)
            case "task":
                self.__handle_character_task(response)
            case "inventory":
                self.__handle_character_inventory(response)
            case _:
                pass

        self.__handle_cooldown(response)


    def __handle_error(self, error: list):
        code, message, *data = error
        print("Error:\n"
            f"  Code: {code}, Message: {message}, Data: {data}")


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


    def __handle_equip(self, response: dict):
        name, code, level, type, subtype, description, effects = [match.value for match in self.equip_query.find(response)]
        print("Equip Item:\n"
            f"  Name: {name}, Code: {code}, Level: {level}\n"
            f"  Description: {description}\n"
            f"  Type: {type}, Subtype: {subtype}\n"
            f"  Effects: {effects}")


    def __handle_unequip(self, response: dict):
        name, code, level, type, subtype, description, effects = [match.value for match in self.unequip_query.find(response)]
        print("Unequip Item:\n"
            f"  Name: {name}, Code: {code}, Level: {level}\n"
            f"  Description: {description}\n"
            f"  Type: {type}, Subtype: {subtype}\n"
            f"  Effects: {effects}")


    def __handle_crafting(self, response: dict):
        xp, items = [match.value for match in self.crafting_query.find(response)]
        print("Crafted Items:\n"
            f"  XP gained: {xp}\n"
            f"  Items: {items}")


    def __handle_character_info(self, response: dict):
        name, level, hp, xp, max_xp, gold, speed, x, y = [match.value for match in self.character_info_query.find(response)]
        print("Character's Info:\n"
            f"   Name: {name}, Level {level} ({xp}/{max_xp} XP)\n"
            f"   HP: {hp}\n"
            f"   Gold: {gold}\n"
            f"   Speed: {speed}\n"
            f"   Coordinates: ({x},{y})")


    def __handle_character_skills(self, response: dict):
        values = [match.value for match in self.character_skills_query.find(response)]

        mining = values[0:3]  # [mining_level, mining_xp, mining_max_xp]
        woodcutting = values[3:6]  # [woodcutting_level, woodcutting_xp, woodcutting_max_xp]
        fishing = values[6:9]  # [fishing_level, fishing_xp, fishing_max_xp]
        weaponcrafting = values[9:12]  # [weaponcrafting_level, weaponcrafting_xp, weaponcrafting_max_xp]
        gearcrafting = values[12:15]  # [gearcrafting_level, gearcrafting_xp, gearcrafting_max_xp]
        jewelrycrafting = values[15:18]  # [jewelrycrafting_level, jewelrycrafting_xp, jewelrycrafting_max_xp]
        cooking = values[18:21]  # [cooking_level, cooking_xp, cooking_max_xp]

        print("Character's Skills:\n"
            f"   {'Mining'.ljust(15)} (Level {mining[0]}): {str(mining[1]).rjust(4)}/{mining[2]}\n"
            f"   {'Woodcutting'.ljust(15)} (Level {woodcutting[0]}): {str(woodcutting[1]).rjust(4)}/{woodcutting[2]}\n"
            f"   {'Fishing'.ljust(15)} (Level {fishing[0]}): {str(fishing[1]).rjust(4)}/{fishing[2]}\n"
            f"   {'Weaponcrafting'.ljust(15)} (Level {weaponcrafting[0]}): {str(weaponcrafting[1]).rjust(4)}/{weaponcrafting[2]}\n"
            f"   {'Gearcrafting'.ljust(15)} (Level {gearcrafting[0]}): {str(gearcrafting[1]).rjust(4)}/{gearcrafting[2]}\n"
            f"   {'Jewelrycrafting'.ljust(15)} (Level {jewelrycrafting[0]}): {str(jewelrycrafting[1]).rjust(4)}/{jewelrycrafting[2]}\n"
            f"   {'Cooking'.ljust(15)} (Level {cooking[0]}): {str(cooking[1]).rjust(4)}/{cooking[2]}")


    def __handle_character_stats(self, response: dict):
        values = [match.value for match in self.character_stats_query.find(response)]

        fire = values[3:6]  # [attack_fire, dmg_fire, res_fire]
        earth = values[6:9]  # [attack_earth, dmg_earth, res_earth]
        water = values[9:12]  # [attack_water, dmg_water, res_water]
        air = values[12:15]  # [attack_air, dmg_air, res_air]

        print("Character's Stats:\n"
            "   Attributes:\n"
            f"    - Haste           : {values[0]}\n"
            f"    - Critical Strike : {values[1]}\n"
            f"    - Stamina         : {values[1]}\n\n"
            "   Elements:\n"
            "   Fire:\n"
            f"   - Attack: {fire[0]}, Damage: {fire[1]}%, Resistance: {fire[2]}%\n"
            "   Earth:\n"
            f"    - Attack: {earth[0]}, Damage: {earth[1]}%, Resistance: {earth[2]}%\n"
            "   Water:\n"
            f"    - Attack: {water[0]}, Damage: {water[1]}%, Resistance: {water[2]}%\n"
            "   Air:\n"
            f"    - Attack: {air[0]}, Damage: {air[1]}%, Resistance: {air[2]}%\n")


    def __handle_character_equipment(self, response: dict):
        values = [match.value for match in self.character_equipment_query.find(response)]

        main = values[0:2] # [weapon_slot, shield_slot]
        body = values[2:6] # [helmet_slot, body_armor_slot, leg_armor_slot, boots_slot]
        jewelry = values[6:9] # [ring1_slot, ring2_slot, amulet_slot]
        artifacts = values[9:12] # [artifact1_slot, artifact2_slot, artifact3_slot]
        consumables = values[12:16] # [consumable1_slot, consumable1_slot_quantity, consumable2_slot, consumable2_slot_quantity]

        print("Character's Equipment:\n"
            "   Main:\n"
            f"    - weapon: {main[0] if main[0] else "- Empty -"}\n"
            f"    - shield: {main[1] if main[1] else "- Empty -"}\n"
            "   Armor:\n"
            f"    - helmet: {body[0] if body[0] else "- Empty -"}\n"
            f"    - body_armor: {body[1] if body[1] else "- Empty -"}\n"
            f"    - leg_armor: {body[2] if body[2] else "- Empty -"}\n"
            f"    - boots: {body[3] if body[3] else "- Empty -"}\n"
            "   Jewelry:\n"
            f"    - ring1: {jewelry[0] if jewelry[0] else "- Empty -"}\n"
            f"    - ring2: {jewelry[1] if jewelry[1] else "- Empty -"}\n"
            f"    - amulet: {jewelry[2] if jewelry[2] else "- Empty -"}\n"
            "   Artifacts:\n"
            f"    - artifact1: {artifacts[0] if artifacts[0] else "- Empty -"}\n"
            f"    - artifact2: {artifacts[1] if artifacts[1] else "- Empty -"}\n"
            f"    - artifact3: {artifacts[2] if artifacts[2] else "- Empty -"}\n"
            "   Consumables:\n"
            f"    - consumable1: {consumables[0] if consumables[0] else "- Empty -"} ({consumables[1]})\n"
            f"    - consumable2: {consumables[2] if consumables[2] else "- Empty -"} ({consumables[3]})\n")


    def __handle_character_task(self, response: dict):
        name, type, progress, total = [match.value for match in self.character_task_query.find(response)]

        print("Character's Task:\n"
            f"   Task: {name}\n"
            f"   Type: {type}\n"
            f"   Progress: {progress}/{total}\n")


    def __handle_character_inventory(self, response: dict):
        max_items, inventory = [match.value for match in self.character_inventory_query.find(response)]
        total_quantity = sum(item['quantity'] for item in inventory)
        max_length = max(len(item["code"]) for item in inventory if item["code"])

        print(f"Character's Inventory ({total_quantity}/{max_items}):")
        for item in inventory:
            item_name = item["code"] if item["code"] else "- Empty -"
            quantity_str = f"({item['quantity']})" if item["quantity"] > 0 else ""

            print(f"   [{item['slot']:02}]: {item_name:<{max_length+4}} {quantity_str}")


    def __handle_cooldown(self, response: dict):
        cooldown = 0

        for match in self.cooldown_query.find(response):
            cooldown = match.value

        print(f"---\nCooldown: {cooldown} sec ({time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})\n---")
        time.sleep(cooldown)

import os
from dotenv import load_dotenv
from src.character import Character
from src.comand_parser import CommandParser

load_dotenv()

SERVER = "https://api.artifactsmmo.com"
TOKEN = os.getenv("TOKEN")
CHARACTER_NAME = os.getenv("CHARACTER_NAME")

if not TOKEN:
    raise ValueError("Token not found")

if not CHARACTER_NAME:
    raise ValueError("Character_name not found")


if __name__ == "__main__":
    with open("input.txt", "r", encoding="utf-8") as file:
        script = file.read()

    parser = CommandParser()
    character = Character(CHARACTER_NAME, TOKEN)

    parser.parse(script)
    parser.execute(character)

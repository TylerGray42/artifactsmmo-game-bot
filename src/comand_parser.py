from .character import Character


class CommandParser:
    def __init__(self):
        self.commands = []

    def parse(self, script:str):
        lines = script.strip().split('\n')
        stack = []

        for line in lines:
            line = line.strip()
            if line.startswith("repeat"):
                _, count = line.split()
                stack.append(("loop", int(count), []))
            elif line.startswith("end"):
                if stack and stack[-1][0] == "loop":
                    command = stack.pop()
                    if stack:
                        stack[-1][2].append(command)
                    else:
                        self.commands.append(command)
            else:
                parts = line.split()
                command = (parts[0], parts[1:] if len(parts) > 1 else [])
                if stack:
                    stack[-1][2].append(command)
                else:
                    self.commands.append(command)


    def execute(self, character: Character):
        for command in self.commands:
            self.__execute_command(command, character)


    def __execute_command(self, command: tuple, character: Character):
        cmd, args, *subcommands = command
        match cmd:
            case "move":
                x, y = map(int, args)
                character.move(x, y)
            case "loop":
                count = args
                subcommands = subcommands[0]
                for _ in range(count):
                    for subcommand in subcommands:
                        self.__execute_command(subcommand, character)
            case "fight":
                character.fight()
            case "info":
                character.get_info()
            case "gathering":
                character.gathering()
            case _:
                pass

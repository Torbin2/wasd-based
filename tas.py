#
# Platformer TAS Movie Format
#
# !ptm
# !gameversion [Version of the game]
# !input-start
# (here goes the inputs, e.g. "A.S..", ".DS..", ".....", "AD..T", "ADSRT")
# !input-end
import json
import os
import pygame

MINIMUM_INPUT_LENGTH = 7


class Input:

    def __init__(self, inputs: list):
        print("inputs", inputs)

        if inputs.__len__() < MINIMUM_INPUT_LENGTH:
            print(f"warn: inputs are {inputs.__len__()} long")

        self.w = inputs[0]
        self.a = inputs[1]
        self.s = inputs[2]
        self.d = inputs[3]
        self.b = inputs[4]
        self.l = inputs[5]
        self.e = inputs[6]

    def to_string(self) -> str:
        return (f"{'W' if self.w else '.'}"
                f"{'A' if self.a else '.'}"
                f"{'S' if self.s else '.'}"
                f"{'D' if self.d else '.'}"
                f"{'B' if self.b else '.'}"
                f"{'L' if self.l else '.'}"
                f"{'E' if self.e else '.'}")

class TASHandler:

    def __init__(self):

        self.movie = TASMovie()
        self.frame = 0
        self.frame_advance = False
        self.loading_savestate = False
        self.default_clock_speed = 30
        self.clock_speed = self.default_clock_speed
        self.physics = True

        with open("tasconfig.txt", "r") as f:
            self.mode = f.read()

    def init_movie(self):
        if self.mode == "write":
            self.movie.write_header()
        elif self.mode == "read":
            self.frame_advance = False
            self.movie.read_inputs()

    def finish_movie(self):
        if self.mode == "write":
            self.movie.write_end()

    def handle_input(self, keys):

        if self.mode == "write":

            if self.loading_savestate:

                self.frame_advance = False

                if self.frame >= self.movie.inputs.__len__() - 1:
                    self.clock_speed = self.default_clock_speed
                    self.frame_advance = True
                    self.loading_savestate = False

                    print("ong", self.frame)

                    self.frame += 1

                    print("adding", self.frame)
                    return
            else:
                self.movie.write_input([keys[pygame.K_w],
                                        keys[pygame.K_a],
                                        keys[pygame.K_s],
                                        keys[pygame.K_d],
                                        keys[pygame.K_RSHIFT],
                                        keys[pygame.K_RETURN],
                                        keys[pygame.K_SLASH]])

    def can_accept_input_default(self) -> bool:
        return self.mode == "write" and not self.loading_savestate

    def may_fire_keydown_event(self, key: str) -> bool:

        print("Check at frame", self.frame, "actual movie len", self.movie.inputs.__len__())

        if self.movie.inputs is None:
            return False

        if self.frame <= 0:
            return False

        return not eval(f"self.movie.inputs[self.frame - 1].{key.lower()}")

class TASMovie:

    def __init__(self):
        self.gameversion = "0.1"
        self.filename = "test.wtm"
        self.seed = 0
        self.studio = []
        self.inputs = []

    def set_seed(self, seed: int):
        self.seed = seed

    def write_header(self):

        if self.filename in os.listdir("."):
            os.remove(self.filename)

        with open(self.filename, "a") as f:

            f.write("!wtm\n")
            f.write(f"!gameversion {self.gameversion}\n")
            f.write(f"!seed {self.seed}\n")
            f.write("!input-start\n")
            f.close()

    def write_end(self):
        with open(self.filename, "a") as f:
            f.write("!input-end")
            f.close()

    def write_input(self, inputs: list[bool, bool, bool, bool, bool]):

        self.inputs.append(Input(inputs))

        with open(self.filename, "a") as f:
            f.write(f"{'W' if inputs[0] else '.'}"
                    f"{'A' if inputs[1] else '.'}"
                    f"{'S' if inputs[2] else '.'}"
                    f"{'D' if inputs[3] else '.'}"
                    f"{'B' if inputs[4] else '.'}"
                    f"{'L' if inputs[5] else '.'}"
                    f"{'E' if inputs[6] else '.'}\n")
            f.close()

    def set_inputs(self, inputs):

        with open(self.filename, 'w+') as f:

            f.seek(0)
            f.truncate()
            f.write("!wtm\n")
            f.write(f"!gameversion {self.gameversion}\n")
            f.write(f"!seed {self.seed}\n")
            f.write("!input-start\n")

            for i in range(len(inputs)):

                input: Input = inputs[i]

                f.write(f"{input.to_string()}\n")

            f.close()

    def remove_input(self, frame):
        with open(self.filename, 'r+') as f:

            lines = f.readlines()

            res = []

            for i in range(len(lines)):
                if i <= frame - 1 + 4: # here you have to remove 4 because of the headers
                    res.append(lines[i])

            f.seek(0)
            f.truncate()
            f.writelines(res)
            f.close()

    def read_inputs(self):

        with open(self.filename, "r+") as f:

            contents = f.readlines()

            print(contents)

            started = False
            finished = False

            for i in range(len(contents)):

                line = contents[i]

                if i == 0:
                    if line.startswith("!wtm"):
                        continue
                    else:
                        raise KeyError("wasd-based TAS Movie should always start with !ptm")

                if i == 1:
                    if line.startswith("!gameversion"):
                        try:
                            self.gameversion = line.split(" ")[1]
                            continue
                        except:
                            raise ValueError(f"Malformed wasd-based TAS Movie file found! check !gameversion line {i}")
                    else:
                        raise KeyError('wasd-based TAS Movie should include "gameversion" attribute')

                if i == 2:
                    if line.startswith("!seed"):
                        try:
                            self.seed = int(line.split(" ")[1])
                            continue
                        except:
                            raise ValueError(f"Malformed wasd-based TAS Movie file found! check !seed line {i}")
                    else:
                        raise KeyError('wasd-based TAS Movie should include "seed" attribute')


                if line.startswith("!input-start"):
                    print("Start of the inputs")
                    started = True
                    continue

                if line.startswith("!input-end"):
                    finished = True
                    print("End of the inputs")
                    continue
                else:
                    if started and not finished:
                        self.inputs.append(self.parse(line))


    def write_savestate(self, slot: int):

        if not os.path.isdir("saves"):
            os.mkdir("saves")

        filename = f"{slot}.wsv"

        with open("saves/" + filename, "w") as f:
            f.write("!wsv\n")
            f.write("!input-start\n")

            for input_ in self.inputs:
                f.write(f"{input_.to_string()}\n")

            f.write("!input-end")
            f.close()

    def parse_lines_of_savestate(self, slot: int):

        filename = f"{slot}.wsv"

        if filename not in os.listdir("./saves"):
            return None

        with open("saves/" + filename, "r+") as f:

            lines = f.readlines()
            inputs = []
            started = False

            for i in range(len(lines)):

                line = lines[i]

                if i == 0:
                    if line.startswith("!wsv"):
                        continue
                    else:
                        raise KeyError(f"wasd-based savestate file should always start with !wsv, instead got {line}")

                if line.startswith("!input-start"):
                    started = True
                    print("starting line")
                    continue

                if line.startswith("!input-end"):

                    print("end line")

                    if self.inputs is None:
                        print("none??")
                        assert False, ""

                    self.inputs = inputs
                    self.set_inputs(self.inputs)

                    if slot == 0:
                        self.studio = self.inputs

                    print("LEN:", inputs.__len__())

                    return inputs
                else:

                    if started:
                        print(f"parse {line}")
                        inputs.append(self.parse(line))



    def parse(self, line: str):

        res = []

        for c in line:

            if c == "\n":
                continue

            if c == ".":
                res.append(False)
            else:
                res.append(True)

        while len(res) < MINIMUM_INPUT_LENGTH:
            res.append(False)

        return Input(res)
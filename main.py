import pyxel
import random
import copy
import enum

TIME = 60
PLAYER_X = 2
PLAYER_Y = 2

SQUARE_SIZE = 20

SCREEN_WIDTH = 200
SCREEN_HEIGHT = 120

GAME_SCREEN_WIDTH = 160
GAME_SCREEN_HEIGHT = 120


class Scene(enum.Enum):
    TITLE = 0
    GAME = 1
    GAME_CLEAR = 2
    GAME_OVER = 3


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        pyxel.load('resource.pyxel')

        self.player = Player()
        self.houses = []
        self.target_houses = []
        self.presents = []
        self.time = 0
        self.scene = Scene.TITLE

        pyxel.run(self.update, self.draw)

    def update(self):
        self.check_deliver_present()
        self.check_clear_or_gameover()
        self.countdown_time()
        self.player.update()

    def draw(self):
        pyxel.cls(0)
        self.draw_ui()
        self.draw_game()
        self.draw_text()

    def check_deliver_present(self):
        if self.scene == Scene.GAME:
            if pyxel.btnp(pyxel.KEY_SPACE) and self.target_houses:
                for house in self.houses:
                    if self.player.x == house.x and self.player.y == house.y:
                        if house.roof == self.target_houses[0].roof and house.door == self.target_houses[0].door and house.color == self.target_houses[0].color:
                            pyxel.play(0, 0)
                            self.target_houses.pop(0)
                            self.presents.append(
                                Present(self.player.x, self.player.y))
                        else:
                            pyxel.play(0, 1)

    def check_clear_or_gameover(self):
        if self.scene == Scene.TITLE and pyxel.btnp(pyxel.KEY_SPACE):
            self.reset()
            self.scene = Scene.GAME
        elif self.scene == Scene.GAME and not self.target_houses:
            self.scene = Scene.GAME_CLEAR
        elif self.scene == Scene.GAME and self.time <= 0:
            self.scene = Scene.GAME_OVER
        elif (self.scene == Scene.GAME_CLEAR or self.scene == Scene.GAME_OVER) and pyxel.btnp(pyxel.KEY_SPACE):
            self.reset()
            self.scene = Scene.GAME

    def countdown_time(self):
        if self.scene == Scene.GAME:
            if pyxel.frame_count % pyxel.DEFAULT_FPS == 0:
                self.time -= 1

    def draw_ui(self):
        cursor_x = int(167 + (TIME - self.time) / TIME * 20)
        if not self.scene == Scene.TITLE:
            pyxel.rect(160, 0, 200, 160, 6)
            pyxel.text(172, 2, 'TIME', 0)
            # pyxel.text(176, 10, f'{self.time}', 0)
            pyxel.line(169, 20, 189, 20, 5)  # 直線
            pyxel.blt(cursor_x, 14, 0, 0, 64, 8, 8, 0)  # 矢印
            pyxel.blt(161, 17, 0, 8, 72, 8, 8, 0)  # 月
            pyxel.blt(191, 17, 0, 0, 72, 8, 8, 0)  # 太陽
            pyxel.text(172, 60, 'NEXT', 0)
            pyxel.rect(170, 70, 190, 90, 0)
            if self.target_houses:
                self.target_houses[0].x = 172
                self.target_houses[0].y = 72
                self.target_houses[0].draw()
                pyxel.text(172, 92, f'{10 - len(self.target_houses)}/10', 0)

    def draw_game(self):
        if not self.scene == Scene.TITLE:
            for house in self.houses:
                house.draw()

            for present in self.presents:
                present.draw()

            self.player.draw()

    def draw_text(self):
        if self.scene == Scene.TITLE:
            pyxel.blt(60, 20, 0, 0, 32, 64, 16, 0)
            pyxel.blt(124, 20, 0, 0, 48, 16, 16, 0)
            pyxel.text(60, 60, 'Press space to start', 7)
        elif self.scene == Scene.GAME_CLEAR:
            pyxel.rect(20, 20, 140, 100, 5)
            pyxel.text(60, 40, 'GAME CLEAR', 7)
            pyxel.text(68, 60, f'TIME:{60 - self.time}', 7)
            pyxel.text(40, 80, 'Press space to retry', 7)
        elif self.scene == Scene.GAME_OVER:
            pyxel.rect(20, 20, 140, 100, 5)
            pyxel.text(60, 40, 'GAME OVER', 7)
            pyxel.text(40, 80, 'Press space to retry', 7)

    def reset(self):
        self.player = Player()
        self.time = 60

        self.houses.clear()
        self.target_houses.clear()
        self.presents.clear()

        for roof_num in range(2):
            for door_num in range(3):
                for color_num in range(8):
                    self.houses.append(House(roof_num, door_num, color_num))

        tmp_houses = copy.deepcopy(self.houses)
        random.shuffle(tmp_houses)
        self.target_houses = tmp_houses[:10]

        random.shuffle(self.houses)

        for index, house in enumerate(self.houses):
            house.x = SQUARE_SIZE * int(index % 8) + 2
            house.y = SQUARE_SIZE * int(index / 8) + 2


class House:
    def __init__(self, roof, door, color):
        self.x = 0
        self.y = 0
        self.roof = roof
        self.door = door
        if color == 0:
            self.color = 8
        elif color == 4:
            self.color = 9
        elif color == 7:
            self.color = 10
        else:
            self.color = color

    def draw(self):
        roof_x = self.x
        roof_y = self.y
        roof_u = 16 * self.roof
        roof_v = 16
        roof_width = 16
        roof_height = 8

        color_x1 = self.x + 2
        color_y1 = self.y + 8
        color_x2 = color_x1 + 11
        color_y2 = color_y1 + 8

        door_x = self.x
        door_y = self.y + 8
        door_u = 16 * self.door
        door_v = 24
        door_width = 16
        door_height = 8

        pyxel.rect(color_x1, color_y1, color_x2, color_y2, self.color)
        pyxel.blt(roof_x, roof_y, 0, roof_u, roof_v,
                  roof_width, roof_height, 0)
        pyxel.blt(door_x, door_y, 0, door_u, door_v,
                  door_width, door_height, 0)


class Present:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        x = self.x + 4
        y = self.y + 9
        u = 0
        v = 8
        w = 16
        h = 8
        pyxel.blt(x, y, 0, u, v, w, h, 0)


class Player:
    def __init__(self):
        self.x = PLAYER_X
        self.y = PLAYER_Y

    def update(self):
        if pyxel.btnp(pyxel.KEY_UP) and self.y >= SQUARE_SIZE:
            self.y -= SQUARE_SIZE
        elif pyxel.btnp(pyxel.KEY_DOWN) and self.y < GAME_SCREEN_HEIGHT - SQUARE_SIZE:
            self.y += SQUARE_SIZE
        elif pyxel.btnp(pyxel.KEY_LEFT) and self.x >= SQUARE_SIZE:
            self.x -= SQUARE_SIZE
        elif pyxel.btnp(pyxel.KEY_RIGHT) and self.x < GAME_SCREEN_WIDTH - SQUARE_SIZE:
            self.x += SQUARE_SIZE

    def draw(self):
        x = self.x + 2
        y = self.y
        u = 0
        v = 0
        w = 16
        h = 8
        pyxel.blt(x, y, 0, u, v, w, h, 0)


App()

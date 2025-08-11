import time
import pyautogui as pg
from human_mouse import MouseController
import random
import math

class Manager:
    def __init__(self):
        self.mouse = MouseController()
        x_time, y_time = (random.uniform(0.05, 0.4), random.uniform(0.05, 0.4))
        self.max_time = max(x_time, y_time)
        self.min_time = min(x_time, y_time)

    @staticmethod
    def press_key(key: str):
        try:
            pg.press(key)
        except:
            print("Non valid key")

    def move_to_img(self, image: str):
        try:
            a, b, c, d = pg.locateOnScreen(image)
            self.move_to(a, b, a + c, b + d)
        except:
            print("Image not found")

    def move_to(self, x0, y0, x1, y1) -> None:
        x, y = self.__point_in_area(x0, y0, x1, y1)
        self.move(x, y)

    def move(self, target_x: int, target_y: int) -> None:
        x, y = pg.position()

        this_distance = self.__distance(x, y, target_x, target_y)

        if this_distance < 100:
            self.mouse.move(target_x, target_y)
            return

        center_x, center_y = self.__temp_point(x, y, target_x, target_y)
        final_x, final_y = self.__aux_point(center_x, center_y, random.randint(10, 30))
        self.mouse.move(final_x, final_y)

        time.sleep(random.uniform(0.2, 0.7))
        self.move(target_x, target_y)

    def clic(self) -> None:
        time.sleep(random.uniform(0.05, 0.2))
        self.mouse.perform_click()

    def double_clic(self):
        self.clic()
        self.clic()

    @staticmethod
    def scroll(x: int) -> None:
        pg.scroll(x)

    def type_text(self, text: str) -> None:
        words = text.split(" ")

        time_interval = self.__new_time_interval()

        pending_errors = []
        indexer = 0

        for word in words:
            for char in word:
                if random.randint(1, 2) == 1:
                    self.__typing_error(char)
                else:
                    if self.__introduce_error(char):
                        pending_errors.append(indexer)

                pg.press(char)

                # randomly change time interval
                if random.randint(1, 10) == random.randint(1, 10):
                    time_interval = self.__new_time_interval()

                time.sleep(random.uniform(*time_interval))
                indexer = indexer + 1
                # resolve pending errors
                self.__resolve_pending_errors(pending_errors, indexer, False)

            if random.randint(1, 2) == 1:
                self.__typing_error(" ")
            else:
                if self.__introduce_error(" "):
                    pending_errors.append(indexer)
            pg.write(" ")
            indexer = indexer + 1

        self.__resolve_pending_errors(pending_errors, indexer - 1, True)
        return

    @staticmethod
    def __temp_point(x0, y0, x1, y1) -> tuple[int, int]:
        t = random.uniform(0.25, 0.75)
        x = x0 + t * (x1 - x0)
        y = y0 + t * (y1 - y0)
        return round(x), round(y)

    @staticmethod
    def __distance(x0, y0, x1, y1) -> int:
        return round(math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2))

    @staticmethod
    def __aux_point(x_center, y_center, r) -> tuple[int, int]:
        theta = random.uniform(0, 2 * math.pi)
        x = x_center + r * math.cos(theta)
        y = y_center + r * math.sin(theta)
        return round(x), round(y)

    @staticmethod
    def __point_in_area(x0, y0, x1, y1) -> tuple[int, int]:
        x_min = min(x0, x1)
        x_max = max(x0, x1)
        y_min = min(y0, y1)
        y_max = max(y0, y1)

        x = random.uniform(x_min, x_max)
        y = random.uniform(y_min, y_max)
        return round(x), round(y)

    def __typing_error(self, char: str) -> None:
        if self.__introduce_error(char):
            time.sleep(random.uniform(0.1, 0.3))
            pg.press("backspace")
            time.sleep(random.uniform(0.1, 0.3))
        return

    def __introduce_error(self, char: str) -> bool:
        if self.__error_prob():
            pg.write(random.choice(self.keyboard_adjacent_keys[char.lower()]))
            return True
        return False

    def __resolve_pending_errors(self, indexes: list, current_index: int, resolve_everything: bool) -> None:
        while random.randint(1, 2) == random.randint(1, 2) or resolve_everything:
            if not len(indexes) > 0:
                return

            fix_index = random.choice(indexes)
            indexes.remove(fix_index)
            delta_positions = current_index - fix_index
            time_interval = self.__new_time_interval()

            self.__move_writing_cursor('left', delta_positions)

            pg.press('backspace')
            time.sleep(random.uniform(*time_interval))

            self.__move_writing_cursor('right', delta_positions)

    def __move_writing_cursor(self, direction: str, times: int) -> None:
        time_interval = self.__new_time_interval()
        for i in range(0, times):
            pg.press(direction)
            time.sleep(random.uniform(*time_interval))

            if random.randint(1, 10) == random.randint(1, 10):
                time_interval = self.__new_time_interval()

    def __new_time_interval(self) -> tuple[float, float]:
        x_time = random.uniform(self.min_time, self.max_time)
        y_time = random.uniform(self.min_time, self.max_time)

        self.__try_change_time_limits()

        return min(x_time, y_time), max(x_time, y_time)

    def __try_change_time_limits(self) -> None:
        if random.randint(1, 30) == random.randint(1, 30):
            x_time, y_time = (random.uniform(0.05, 0.4), random.uniform(0.05, 0.4))
            self.max_time = max(x_time, y_time)
            self.min_time = min(x_time, y_time)


    @staticmethod
    def __error_prob() -> bool:
        lim = random.randint(10, 50)
        if random.randint(1, lim) == random.randint(1, lim):
            return True

        return False

    keyboard_adjacent_keys: dict = {
        # First
        '1': ['2', 'q', 'w', '`', '~', '!'],
        '2': ['1', '3', 'q', 'w', 'e', '@'],
        '3': ['2', '4', 'w', 'e', 'r', '#'],
        '4': ['3', '5', 'e', 'r', 't', '$'],
        '5': ['4', '6', 'r', 't', 'y', '%'],
        '6': ['5', '7', 't', 'y', 'u', '^'],
        '7': ['6', '8', 'y', 'u', 'i', '&'],
        '8': ['7', '9', 'u', 'i', 'o', '*'],
        '9': ['8', '0', 'i', 'o', 'p', '('],
        '0': ['9', '-', 'o', 'p', '[', ')'],
        '-': ['0', '=', 'p', '[', ']', '_'],
        '=': ['-', '[', ']', '\\', '+'],

        # Second
        'q': ['1', '2', 'w', 'a', 's', 'Q'],
        'w': ['1', '2', '3', 'q', 'e', 'a', 's', 'd', 'W'],
        'e': ['2', '3', '4', 'w', 'r', 's', 'd', 'f', 'E'],
        'r': ['3', '4', '5', 'e', 't', 'd', 'f', 'g', 'R'],
        't': ['4', '5', '6', 'r', 'y', 'f', 'g', 'h', 'T'],
        'y': ['5', '6', '7', 't', 'u', 'g', 'h', 'j', 'Y'],
        'u': ['6', '7', '8', 'y', 'i', 'h', 'j', 'k', 'U'],
        'i': ['7', '8', '9', 'u', 'o', 'j', 'k', 'l', 'I'],
        'o': ['8', '9', '0', 'i', 'p', 'k', 'l', ';', 'O'],
        'p': ['9', '0', '-', 'o', '[', 'l', ';', '\'', 'P'],
        '[': ['0', '-', '=', 'p', ']', ';', '\'', '\\', '{'],
        ']': ['[', '=', '\\', '\'', '}'],
        '\\': [']', '=', '|'],

        # third
        'a': ['q', 'w', 's', 'z', 'x', 'A'],
        's': ['q', 'w', 'e', 'a', 'd', 'z', 'x', 'c', 'S'],
        'd': ['w', 'e', 'r', 's', 'f', 'x', 'c', 'v', 'D'],
        'f': ['e', 'r', 't', 'd', 'g', 'c', 'v', 'b', 'F'],
        'g': ['r', 't', 'y', 'f', 'h', 'v', 'b', 'n', 'G'],
        'h': ['t', 'y', 'u', 'g', 'j', 'b', 'n', 'm', 'H'],
        'j': ['y', 'u', 'i', 'h', 'k', 'n', 'm', ',', 'J'],
        'k': ['u', 'i', 'o', 'j', 'l', 'm', ',', '.', 'K'],
        'l': ['i', 'o', 'p', 'k', ';', ',', '.', '/', 'L'],
        ';': ['o', 'p', '[', 'l', '\'', '.', '/', ':'],
        '\'': ['p', '[', ']', ';', '"'],

        # fourth
        'z': ['a', 's', 'x', 'Z'],
        'x': ['a', 's', 'd', 'z', 'c', 'X'],
        'c': ['s', 'd', 'f', 'x', 'v', 'C'],
        'v': ['d', 'f', 'g', 'c', 'b', 'V'],
        'b': ['f', 'g', 'h', 'v', 'n', 'B'],
        'n': ['g', 'h', 'j', 'b', 'm', 'N'],
        'm': ['h', 'j', 'k', 'n', ',', 'M'],
        ',': ['j', 'k', 'l', 'm', '.', '<'],
        '.': ['k', 'l', ';', ',', '/', '>'],
        '/': ['l', ';', '.', '?'],

        # special chars
        ' ': ['c', 'v', 'b', 'n', 'm', ',', '.', '/'],
        '\t': ['q', 'a', 'z'],
        '\n': ['\\', "'", ']', '=', '+'],

        # symbols
        '!': ['1', '2', '@', '~'],
        '@': ['2', '3', '!', '#', 'q', 'Q'],
        '#': ['3', '4', '@', '$', 'w', 'W'],
        '$': ['4', '5', '#', '%', 'e', 'E'],
        '%': ['5', '6', '$', '^', 'r', 'R'],
        '^': ['6', '7', '%', '&', 't', 'T'],
        '&': ['7', '8', '^', '*', 'y', 'Y'],
        '*': ['8', '9', '&', '(', 'u', 'U'],
        '(': ['9', '0', '*', ')', 'i', 'I'],
        ')': ['0', '-', '(', '_', 'o', 'O'],
        '_': ['-', '=', ')', '+', 'p', 'P'],
        '+': ['=', '_', '{', '}'],

        # symbols
        '~': ['1', '!', '`'],
        '`': ['1', '~'],
        '{': ['[', ']', '+', '}', 'P'],
        '}': [']', '{', '|', "'", '"'],
        '|': ['\\', '}', ']'],
        ':': [';', '"', 'L'],
        '"': ['\'', ':', '?', ';'],
        '<': [',', 'm', '.', '>'],
        '>': ['.', '<', '/', '?'],
        '?': ['/', '>', '"']
    }
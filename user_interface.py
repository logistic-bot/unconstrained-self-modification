from typing import List
import logging
import curses
logger = logging.getLogger(__name__)

class ListRenderer:
    def __init__(self, renderer, x_pos : int, y_pos : int, items : List[str] = [], max_length : int = None):
        # TODO: if the user changes self.items, self.max_length is not correct anymore. Use @property and self._max_length

        if max_length is None:
            max_length = max([len(item) for item in items])
        self.max_length = max_length

        self.y_pos = y_pos
        self.x_pos = x_pos
        self.items = items
        self.renderer = renderer

        self._selected = True
        self.indent_selected = False
        self.index = 0

        logger.info("Created new ListRenderer at ({}, {})")

        self.draw()

    def select_next(self):
        self.select(self.index + 1)
        self.draw()

    def select_previous(self):
        self.select(self.index - 1)
        self.draw()

    def check_input(self, key):
        if self.selected:
            if key == "KEY_DOWN":
                self.select_next()
            elif key == "KEY_UP":
                self.select_previous()

    def select(self, index : int):
        try:
            assert index < len(self.items)
            assert index >= 0
            self.index = index
        except AssertionError:
            logger.warning("Tried to select item at index {} but item does not exist. Items: {}", index, self.items)
        self.draw()

    @property
    def selected_item(self):
        return self.items[self.index]

    def selected():
        def fget(self):
            return self._selected
        def fset(self, value):
            self._selected = value
            self.draw()
        return locals()
    selected = property(**selected())

    def draw(self):
        # draw the list
        for index, item in enumerate(self.items):
            self.renderer.addtext(self.x_pos, self.y_pos + index, " " * (self.max_length + 1))
            self.renderer.addtext(self.x_pos, self.y_pos + index, item)

        self.highlight_selected()

    def highlight_selected(self):
        # highlight selected
        if self.selected: # if selected
            self.renderer.addtext(self.x_pos, self.y_pos + self.index, " " * self.max_length)

            if self.indent_selected:
                self.renderer.addtext(self.x_pos + 1, self.y_pos + self.index, self.selected_item, curses.A_BOLD | curses.A_REVERSE)
            else:
                self.renderer.addtext(self.x_pos, self.y_pos + self.index, self.selected_item, curses.A_BOLD | curses.A_REVERSE)
        else: # if not selected
            self.renderer.addtext(self.x_pos, self.y_pos + self.index, self.selected_item, curses.A_DIM | curses.A_REVERSE)

    def set_selected(self, selected : bool = True):
        self.selected = selected

"""
j = create_list(["Test1","Test2","Test3"], vertical=true, offx = 5, offy = 5, x = 5, y = 2)
j.create_border()
j.set_title("Save File", 1)

j.draw()

j.check_key_pressed(key)

if j.check_selected():
    j.set_active(False)
    h.set_active(True)
"""

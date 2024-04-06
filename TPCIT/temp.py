import numpy as np
from enum import Enum
import re

bsplit = re.compile(r'B(\d+)x(\d+)\|(.*)')
bparse = re.compile(r'([EWP])(\d+)')
nodeparse = re.compile(r'\((\d+),(\d+)\)')

class Tile(Enum):
    EMPTY = 0
    WALL = 1
    PLAYER = 2
    ENEMY = 3

tiledict = {
    'E': Tile.EMPTY,
    'W': Tile.WALL,
    'P': Tile.PLAYER,
    'X': Tile.ENEMY,
    'x': Tile.ENEMY
}

class Player:
    def __init__(self, row, col):
        self.row = row
        self.col = col

class Enemy:
    def __init__(self, desc, nodes):
        self.desc = desc
        self.nodes = nodes
        self.row, self.col = self.nodes[0]
        self.dest = 1

    def move(self):
        if (self.row, self.col) == self.nodes[self.dest]:
            self.dest = (self.dest + 1) % len(self.nodes)
        if self.row < self.nodes[self.dest][0]:
            self.row += 1
        elif self.row > self.nodes[self.dest][0]:
            self.row -= 1
        if self.col < self.nodes[self.dest][1]:
            self.col += 1
        elif self.col > self.nodes[self.dest][1]:
            self.col -= 1

class Game:
    def __init__(self, levelstring):
        nodestrings = levelstring.split('\n')
        boardstring = nodestrings.pop(0)

        res = bsplit.match(boardstring)
        rows, cols, tilestr = res.groups()
        self.dim = (int(rows), int(cols))
        self.tiles = np.zeros(self.dim[0] * self.dim[1])
        self.enemies = []

        for nodestring in nodestrings:
            desc, nodes = nodestring.split(' ')
            nodes = [(int(row), int(col)) for row, col in nodeparse.findall(nodes)]
            self.enemies.append(Enemy(desc, nodes))

        head = 0
        for tiletype, count in bparse.findall(tilestr):
            self.tiles[head: head + int(count)] = tiledict[tiletype].value
            head += int(count)
        self.tiles = self.tiles.reshape(self.dim)
        [self.p_row], [self.p_col] = np.where(self.tiles == Tile.PLAYER.value)

    def enemy_tick(self):
        for enemy in self.enemies:
            enemy.move()

    def try_move(self, direction):
        newrow, newcol = self.p_row, self.p_col
        if direction == 'U':
            newrow -= 1
        elif direction == 'D':
            newrow += 1
        elif direction == 'L':
            newcol -= 1
        elif direction == 'R':
            newcol += 1
        if 0 <= newrow < self.dim[0] and 0 <= newcol < self.dim[1] and self.tiles[newrow, newcol] != Tile.WALL.value:
            self.tiles[self.p_row, self.p_col] = Tile.EMPTY.value
            self.tiles[newrow, newcol] = Tile.PLAYER.value
            self.p_row, self.p_col = newrow, newcol
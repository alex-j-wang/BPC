import numpy as np
import pygame
import re
import os
import ast

script_dir = os.path.dirname(__file__)
levels_dir = os.path.join(script_dir, 'levels')

CIT = (160, 144) # Width and height of CIT display
TPS = 10 # Ticks per second
PLAYERSPEED = 5 # Tiles per second
ENEMYSPEED = 2.5 # Tiles per second
PLAYERSIZE = 0.75 # Size of player in tiles
ENEMYSIZE = 0.35 # Radius of enemy in tiles
COINSIZE = 0.25 # Radius of coin in tiles

bsplit = re.compile(r'B(\d+)x(\d+)\nW ?(.*)\nC ?(.*)\nG ?(.*)')
cptparse = re.compile(r'\(([\d:]+), ?([\d:]+)\)')
nparse = re.compile(r'V([\d\.-]+) (.*)')
cparse = re.compile(r'V([\d\.-]+) \(([\d\.]+), ?([\d\.]+)\) R([\d\.]+) A([\d\.]+)')
wparse = cptparse

class Player:
    def __init__(self, row, col, ratio):
        self.pos = (col * ratio - ratio / 2, row * ratio - ratio / 2) # Center of player, precise
        self.rect = pygame.Rect(self.pos[0] - PLAYERSIZE * ratio // 2,
                                self.pos[1] - PLAYERSIZE * ratio // 2,
                                PLAYERSIZE * ratio, PLAYERSIZE * ratio)
        self.spawn = self.pos

    def move(self, dx, dy):
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)
        self.pos = (self.pos[0] % CIT[0], self.pos[1] % CIT[1])
        self.rect.center = self.pos

class NodeEnemy:
    def __init__(self, vm, nodes, ratio):
        nodes = np.array(nodes)[:, ::-1] * ratio - ratio / 2
        self.idx = 0
        self.pos = nodes[self.idx]
        self.static = nodes.shape[0] <= 1
        
        if not self.static:
            differences = np.concatenate([nodes[1:], nodes[:1]], axis=0) - nodes
            self.distances = np.linalg.norm(differences, axis=1)
            self.velocities = differences / self.distances[:, None]
            self.dist = self.distances[self.idx]
            self.ppt = ENEMYSPEED * vm * ratio / TPS # Pixels per tick

    def move(self):
        if self.static:
            return
        if self.dist <= self.ppt:
            self.pos += self.velocities[self.idx] * self.dist # Move to node
            self.idx = (self.idx + 1) % len(self.velocities) # Update index
            self.pos += self.velocities[self.idx] * (self.ppt - self.dist)
            self.dist = self.distances[self.idx] + self.dist - self.ppt
        else:
            self.pos += self.velocities[self.idx] * self.ppt
            self.dist -= self.ppt

class CircleEnemy:
    def __init__(self, vm, row, col, radius, angle, ratio):
        self.center = np.array([col, row]) * ratio - ratio / 2
        self.radius = radius * ratio
        self.angle = angle * np.pi / 180
        self.pos = self.center + self.radius * np.array([np.cos(self.angle), np.sin(self.angle)])
        self.rpt = ENEMYSPEED * vm * ratio / self.radius / TPS # Radians per tick

    def move(self):
        self.angle = (self.angle + self.rpt) % (2 * np.pi)
        self.pos = self.center + self.radius * np.array([np.cos(self.angle), np.sin(self.angle)])

class Game:
    def __init__(self, level=1):
        self.level = level
        self.load_level()

    def load_level(self):
        with open(os.path.join(levels_dir, f'L{self.level}.txt')) as f:
            levelstring = f.read()
        boardstring, entitystring = levelstring.split('\n\n', 1)
        entitystring = entitystring.split('\n')
        
        # Parse the boardstring
        ncols, nrows, wallstrs, checkstrs, coinstrs = bsplit.match(boardstring).groups()
        ncols, nrows = int(ncols), int(nrows)
        assert CIT[0] % ncols == 0 and CIT[1] % nrows == 0 and \
            (CIT[0] // ncols) == (ratio := CIT[1] // nrows)
        self.ratio = ratio
        self.dim = (nrows, ncols)

        # Parse the wall and checkpoint strings
        self.wallrects = to_wallrects(wallstrs, ratio)
        self.checkpointrects = to_checkpointrects(checkstrs, ratio)
        coinstrs = ast.literal_eval(coinstrs)
        if coinstrs:
            self.coins = (np.array(coinstrs) * ratio - ratio / 2)[:, ::-1].tolist()
        else:
            self.coins = []
        self.reached = [False] * len(self.checkpointrects)
        self.savedcoins = self.coins.copy()

        # Parse the entitystring
        self.draw = True
        self.enemies = []
        for entitystr in entitystring:
            if not entitystr:
                continue
            name, behavior, args = entitystr.split(' ', 2) # Args are MATLAB-indexed
            match behavior:
                case 'MANUAL':
                    assert name == 'P'
                    params = ast.literal_eval(args)
                    self.player = Player(*params, ratio)
                case 'NODE':
                    assert name == 'E'
                    params = nparse.match(args).groups()
                    nodes = ast.literal_eval(params[1])
                    self.enemies.append(NodeEnemy(float(params[0]), nodes, ratio))
                case 'CIRCLE':
                    assert name == 'E'
                    params = cparse.match(args).groups()
                    self.enemies.append(CircleEnemy(*map(int, params), ratio))
                case 'WALL':
                    assert name == 'W'
                    row, rowstr = wparse.match(args).groups()
                    self.wallrects.extend(make_row(int(row) - 1, rowstr, ratio))
                case 'OFF':
                    assert name == 'DRAW'
                    self.draw = False
                case default:
                    raise ValueError(f'Invalid movement type: {behavior}')

    def player_tick(self, dr, dc):
        if (not dr and not dc):
            return
        dx, dy = dc * PLAYERSPEED * self.ratio / TPS, dr * PLAYERSPEED * self.ratio / TPS
        if (dx and dy):
            dx /= np.sqrt(2)
            dy /= np.sqrt(2)
        
        self.player.move(dx, 0)
        for wallrect in self.wallrects:
            if self.player.rect.colliderect(wallrect):
                if dx < 0:
                    self.player.rect.left = wallrect.right
                else:
                    self.player.rect.right = wallrect.left
                self.player.pos = (self.player.rect.centerx, self.player.pos[1])
                break
        
        self.player.move(0, dy)
        for wallrect in self.wallrects:
            if self.player.rect.colliderect(wallrect):
                if dy < 0:
                    self.player.rect.top = wallrect.bottom
                else:
                    self.player.rect.bottom = wallrect.top
                self.player.pos = (self.player.pos[0], self.player.rect.centery)
                break

        for i, checkpointrect in enumerate(self.checkpointrects):
            if self.player.rect.colliderect(checkpointrect):
                self.reached[i] = True
                self.player.spawn = checkpointrect.center
                self.savedcoins = self.coins.copy()
                break

    def enemy_tick(self):
        hit = False
        for enemy in self.enemies:
            enemy.move()
            if intersects(self.player.rect, enemy.pos, ENEMYSIZE * self.ratio):
                hit = True
        if hit:
            self.player.pos = self.player.spawn
            self.player.rect.center = self.player.spawn
            self.coins = self.savedcoins.copy()
    
    def coin_tick(self):
        for coin in self.coins:
            if intersects(self.player.rect, coin, COINSIZE * self.ratio):
                self.coins.remove(coin)

def intersects(rect, center, r):
    circle_distance_x = abs(center[0] - rect.centerx)
    circle_distance_y = abs(center[1] - rect.centery)

    if circle_distance_x > rect.w / 2.0 + r or circle_distance_y > rect.h / 2.0 + r:
        return False
    if circle_distance_x <= rect.w / 2.0 or circle_distance_y <= rect.h / 2.0:
        return True
    
    corner_x = circle_distance_x - rect.w / 2.0
    corner_y = circle_distance_y - rect.h / 2.0
    corner_distance_sq = corner_x**2.0 + corner_y**2.0
    return corner_distance_sq <= r**2.0

def make_row(row, rowstr, ratio):
    if rowstr == ':':
        return [pygame.Rect(0, row * ratio, CIT[0], ratio)] 
    rects = []
    for segment in rowstr.split(','):
        if ':' in segment:
            start, end = map(int, segment.split(':'))
            rects.append(pygame.Rect((start - 1) * ratio, row * ratio, (end + 1 - start) * ratio, ratio))
        else:
            rects.append(pygame.Rect((int(segment) - 1) * ratio, row * ratio, ratio, ratio))
    return rects

def to_wallrects(rowstrs, ratio):
    rects = []
    rowstrs = rowstrs.split('|')
    for row, rowstr in enumerate(rowstrs):
        if not rowstr:
            continue
        rects.extend(make_row(row, rowstr, ratio))
    return rects

def to_checkpointrects(cptstrs, ratio):
    rects = []
    for rowstr, colstr in cptparse.findall(cptstrs):
        if ':' in rowstr:
            rs, re = map(int, rowstr.split(':'))
        else:
            rs = re = int(rowstr)
        if ':' in colstr:
            cs, ce = map(int, colstr.split(':'))
        else:
            cs = ce = int(colstr)
        rects.append(pygame.Rect((cs - 1) * ratio, (rs - 1) * ratio, (ce - cs + 1) * ratio, (re - rs + 1) * ratio))
    return rects

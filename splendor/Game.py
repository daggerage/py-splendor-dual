import random
COLOR_RED=1
COLOR_GREEN=2
COLOR_BLUE=3
COLOR_BLACK=4
COLOR_WHITE=5
COLOR_GOLD=6
COLOR_PEARL=7
COLOR_ANY=8
COLORS=[
    COLOR_RED,
    COLOR_GREEN,
    COLOR_BLUE,
    COLOR_BLACK,
    COLOR_WHITE,
    COLOR_GOLD,
    COLOR_PEARL,
]

SKILL_NONE=10
SKILL_TAKE=11
SKILL_STEAL=12
SKILL_REFRESH=13

RES_FAIL=20
RES_OK=21
RES_GIVE_PREVILEGE=22

class Gem:
    def __init__(self, color: int):
        self.color = color

class Gems:
    def __init__(self, gem_list=None):
        if gem_list is None:
            gem_list = []
        self.gem_list = gem_list

    def add(self, gem:Gem|Gems):
        if isinstance(gem, Gem):
            self.gem_list.append(gem)
        elif isinstance(gem, Gems):
            self.gem_list.extend(gem.gem_list)

    def remove(self, gem):
        self.gem_list.remove(gem)

    def count(self, color:int):
        return sum(1 for gem in self.gem_list if gem.color == color)
    
    def shuffle(self):
        random.shuffle(self.gem_list)

    def add_value(self, cards:Cards):
        new_gems = Gems(self.gem_list)
        for card in cards.card_list:
            values = card.gem_values
            new_gems.add(values)

class GemBoard:
    # 5*5的宝石盘
    def __init__(self):
        b = []
        for i in range(4):
            b.append(Gem(COLOR_RED))
            b.append(Gem(COLOR_GREEN))
            b.append(Gem(COLOR_BLUE))
            b.append(Gem(COLOR_BLACK))
            b.append(Gem(COLOR_WHITE))
        for i in range(3):
            b.append(Gem(COLOR_GOLD))
        for i in range(2):
            b.append(Gem(COLOR_PEARL))
        b.shuffle()
        self.gems = b
        self.gem_bag = Gems()

    def at(self, y,x):
        return self.gems[y*5+x]
    
    def is_connected_and_no_empty(self, pos1:int, pos2:int=None, pos3:int=None):
        if pos2 is None and pos3 is None:
            return True
        # 转换成y,x
        y1, x1 = pos1 // 5, pos1 % 5
        op = [(y1, x1)]
        if pos2 is not None:
            y2, x2 = pos2 // 5, pos2 % 5
            op.append((y2, x2))
        if pos3 is not None:
            y3, x3 = pos3 // 5, pos3 % 5
            op.append((y3, x3))
        op.sort(key=lambda p: p[0])
        for p in op:
            if self.at(p[0], p[1])==0:
                return False
            
        if len(op)==1:
            return True
        
        dy12 = op[1][0] - op[0][0]
        dx12 = op[1][1] - op[0][1]
        if dy12>1 or dx12>1:
            return False
        if len(op)==2:
            return True
        
        dy23 = op[2][0] - op[1][0]
        dx23 = op[2][1] - op[1][1]
        if dy12 == dy23 and dx12 == dx23:
            return True
        else:
            return False
        

    def take(self, pos1:int, pos2:int=None, pos3:int=None):
        # 必须拿连着的，横/竖/斜
        if not self.is_connected_and_no_empty(pos1, pos2, pos3):
            return (RES_FAIL, None)
        gems = [self.gems[pos1]]
        if pos2 is not None:
            gems.append(self.gems[pos2])
        if pos3 is not None:
            gems.append(self.gems[pos3])
        return (RES_OK, gems)
        

class Card:
    def __init__(self, name, level, score:int, gem_costs:Gems, gem_values:Gems, prestige:int):
        self.name = name
        self.level = level
        self.score = score
        self.gem_costs = gem_costs
        self.gem_values = gem_values
        self.prestige = prestige


class Cards:
    def __init__(self, card_list=None):
        if card_list is None:
            card_list = []
        self.card_list = card_list

    def add(self, card):
        self.card_list.append(card)

    def remove(self, card):
        self.card_list.remove(card)

    def shuffle(self):
        random.shuffle(self.card_list)

    def draw(self):
        if len(self.card_list) == 0:
            return None
        return self.card_list.pop(random.randint(0, len(self.card_list) - 1))

class PlayerCards(Cards):
    def count_values(self, color:int):
        return sum(1 for card in self.card_list if card.gem_values.count(color) > 0)
    def count_score(self, color:int=None):
        if color is None:
            return sum(card.score for card in self.card_list)
        else:
            return sum(card.score for card in self.card_list if card.gem_values.count(color) > 0)
    def count_prestige(self):
        return sum(card.prestige for card in self.card_list)


class Character:
    def __init__(self, name, skill:int, score:int):
        self.name = name
        self.skill = skill
        self.score = score

class Player:
    def __init__(self, name):
        self.name = name
        self.gems: Gems = Gems()
        self.cards: PlayerCards = PlayerCards()
        self.characters: list[Character] = []
        self.previlege = 0

    def can_afford(self, card:Card):
        self.gems
        self.cards.

    def buy_card(self, card:Card, payment:Gems):
        pass

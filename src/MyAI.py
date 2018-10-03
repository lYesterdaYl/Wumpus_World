# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent

class MyAI ( Agent ):

    def __init__ ( self ):
        self._current_status = {}
        self._world_map = World_Map()



    def store_information(self, stench, breeze, glitter, bump, scream):
        self._current_status['stench'] = stench
        self._current_status['breeze'] = breeze
        self._current_status['glitter'] = glitter
        self._current_status['bump'] = bump
        self._current_status['scream'] = scream


        print(self._current_status)

    def found_gold(self):
        if(self._current_status['glitter']):
            return True
        else:
            return False

    def getAction( self, stench, breeze, glitter, bump, scream ):
        self.store_information(stench, breeze, glitter, bump, scream)
        self._world_map.update_current_position(self._current_status)
        # self._world_map.swap_position()
        self._world_map.show_map()


class World_Map:
    def __init__(self):
        self._x = 0
        self._y = 0
        self._map = [["" for x in range(4)] for x in range(4)]

        self._current_direction = ''
        self._number_of_move = 0
        self._current_status = {}

        self._safe_position = [[False for x in range(4)] for y in range(4)]
        self._breeze_position = [[False for x in range(4)] for y in range(4)]
        self._stench_position = [[False for x in range(4)] for y in range(4)]
        self._Pit_position = [[False for x in range(4)] for y in range(4)]
        self.current_position = (0, 0)

    def moveTo(self, dx, dy):
        x, y = self.current_position
        # go left
        if dx < x:
            if self._current_direction == 'right':
                Agent.Action.TURN_RIGHT
                Agent.Action.TURN_RIGHT
            if self._current_direction == 'up':
                Agent.Action.TURN_LEFT
            if self._current_direction == 'down':
                Agent.Action.TURN_RIGHT
            self._current_direction = 'left'
            Agent.Action.FORWARD
            self.current_position = (x - 1, y)
            self._number_of_move += 1
        # go right
        if dx > x:
            if self._current_direction == 'left':
                Agent.Action.TURN_LEFT
                Agent.Action.TURN_LEFT
            if self._current_direction == 'up':
                Agent.Action.TURN_RIGHT
            if self._current_direction == 'down':
                Agent.Action.TURN_LEFT
            self._current_direction = 'right'
            Agent.Action.FORWARD
            self.current_position = (x + 1, y)
            self._number_of_move += 1
        # go up
        if dy > y:
            if self._current_direction == 'left':
                Agent.Action.TURN_RIGHT
            if self._current_direction == 'right':
                Agent.Action.TURN_LEFT
            if self._current_direction == 'down':
                Agent.Action.TURN_LEFT
                Agent.Action.TURN_LEFT
            self._current_direction = 'up'
            Agent.Action.FORWARD
            self.current_position = (x, y + 1)
            self._number_of_move += 1
        # go down
        if dy < y:
            if self._current_direction == 'left':
                Agent.Action.TURN_RIGHT
            if self._current_direction == 'right':
                Agent.Action.TURN_LEFT
            if self._current_direction == 'down':
                Agent.Action.TURN_LEFT
                Agent.Action.TURN_LEFT
            self._current_direction = 'down'
            Agent.Action.FORWARD
            self.current_position = (x, y - 1)
            self._number_of_move += 1

    def show_map(self):
        # self._map[0][1] = 2
        print("world map is ", self._map)
        # print(self._map[0][0])

    def swap_position(self):
        temp = self._map[0]
        self._map[0] = self._map[3]
        self._map[3] = temp

        temp = self._map[1]
        self._map[1] = self._map[2]
        self._map[2] = temp

    def update_current_position(self, current_status):
        status_list = self._map[self._x][self._y].split(" ")

        if current_status['stench'] and 'S' not in status_list: self._map[self._x][self._y] += ' S '
        if current_status['breeze'] and 'B' not in status_list: self._map[self._x][self._y] += ' B '
        if current_status['glitter'] and 'G' not in status_list: self._map[self._x][self._y] += ' G '
        self._current_status = current_status

    def analysis(self):
        if (self._number_of_move == 0 and self._current_status['breeze'] == True):
            return Agent.Action.CLIMB



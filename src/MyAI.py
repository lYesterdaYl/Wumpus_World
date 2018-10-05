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
        self.tmp=[]


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

        if len(self._world_map.actionlist) == 0:
            result = self._world_map.analysis()
            print("result = ", result)
            if result[0] == 'ACTION':
                return self._world_map.actionlist.pop(0)
            elif result[0] == 'MOVEMENT':
                print("movement: ", self._world_map.actionlist)
                if self._world_map.actionlist == []:
                    self._world_map.moveTo(result[1][0],result[1][1])
                    return self._world_map.actionlist.pop(0)
        else:
            return self._world_map.actionlist.pop(0)


class World_Map:
    def __init__(self):
        self._x = 0
        self._y = 0
        self._map = [["" for x in range(4)] for x in range(4)]

        self._current_direction = 'right'
        self._number_of_move = 0
        self._current_status = {}

        self.has_visited = []
        self.available_position = {}

        self._store_point = {}

        self._safe_position = [[False for x in range(4)] for y in range(4)]
        self._breeze_position = [[False for x in range(4)] for y in range(4)]
        self._stench_position = [[False for x in range(4)] for y in range(4)]
        self._Pit_position = [[False for x in range(4)] for y in range(4)]
        self.current_position = (0, 0)
        self.actionlist=[]

    def moveTo(self, dx, dy):
        print('direction',self._current_direction)
        x, y = self.current_position
        # go left
        if dx < x:
            if self._current_direction == 'right':
                self.actionlist.append(Agent.Action.TURN_RIGHT)
                self.actionlist.append(Agent.Action.TURN_RIGHT)
            if self._current_direction == 'up':
                self.actionlist.append(Agent.Action.TURN_LEFT)
            if self._current_direction == 'down':
                self.actionlist.append(Agent.Action.TURN_RIGHT)
            self._current_direction = 'left'
            self.actionlist.append(Agent.Action.FORWARD)
            self.current_position = (x - 1, y)
            self._number_of_move += 1
        # go right
        if dx > x:
            if self._current_direction == 'left':
                self.actionlist.append(Agent.Action.TURN_LEFT)
                self.actionlist.append(Agent.Action.TURN_LEFT)
            if self._current_direction == 'up':
                self.actionlist.append(Agent.Action.TURN_RIGHT)
            if self._current_direction == 'down':
                self.actionlist.append(Agent.Action.TURN_LEFT)
            self._current_direction = 'right'
            self.actionlist.append(Agent.Action.FORWARD)
            self.current_position = (x + 1, y)
            self._number_of_move += 1
        # go up
        if dy > y:
            if self._current_direction == 'left':
                self.actionlist.append(Agent.Action.TURN_RIGHT)
            if self._current_direction == 'right':
                self.actionlist.append(Agent.Action.TURN_LEFT)
            if self._current_direction == 'down':
                self.actionlist.append(Agent.Action.TURN_LEFT)
                self.actionlist.append(Agent.Action.TURN_LEFT)
            self._current_direction = 'up'
            self.actionlist.append(Agent.Action.FORWARD)
            self.current_position = (x, y + 1)
            self._number_of_move += 1
        # go down
        if dy < y:
            if self._current_direction == 'left':
                self.actionlist.append(Agent.Action.TURN_RIGHT)
            if self._current_direction == 'right':
                self.actionlist.append(Agent.Action.TURN_LEFT)
            if self._current_direction == 'up':
                self.actionlist.append(Agent.Action.TURN_LEFT)
                self.actionlist.append(Agent.Action.TURN_LEFT)
            self._current_direction = 'down'
            self.actionlist.append(Agent.Action.FORWARD)
            self.current_position = (x, y - 1)
            self._number_of_move += 1
        print('move:' , self.actionlist)

    def show_map(self):
        # self._map[0][1] = 2
        print("world map is ", self._map)
        # print(self._map[0][0])

    def update_current_position(self, current_status):
        if current_status['stench']: self._map[self.current_position[0]][self.current_position[1]] += ' S '
        if current_status['breeze']: self._map[self.current_position[0]][self.current_position[1]] += ' B '
        if current_status['glitter']: self._map[self.current_position[0]][self.current_position[1]] += ' G '

        self._current_status = current_status

    def show_map(self):
        # self._map[0][1] = 2
        print("world map is ", self._map)
        # print(self._map[0][0])

    def update_current_position(self, current_status):
        print("update_current_position status = ", current_status)
        status_list = self._map[self.current_position[0]][self.current_position[1]].split(" ")

        if current_status['stench'] and 'S' not in status_list: self._map[self.current_position[0]][self.current_position[1]] += ' S '
        if current_status['breeze'] and 'B' not in status_list: self._map[self.current_position[0]][self.current_position[1]] += ' B '
        if current_status['glitter'] and 'G' not in status_list: self._map[self.current_position[0]][self.current_position[1]] += ' G '
        self._current_status = current_status

    #get next forward cordinate for moveTo
    def get_current_direction_forward_position(self):
        if self._current_direction == 'right':
            return (self.current_position[0] + 1, self.current_position[1])
        elif self._current_direction == 'left':
            return (self.current_position[0] - 1, self.current_position[1])
        elif self._current_direction == 'up':
            return (self.current_position[0], self.current_position[1] + 1)
        elif self._current_direction == 'down':
            return (self.current_position[0], self.current_position[1] - 1)

    def check_current_position_available_direction(self):
        self.available_position[self.current_position] = []
        print("available position status", self._current_status)
        if not self._current_status['stench'] and not self._current_status['breeze']:
            if (self.current_position[0] + 1, self.current_position[1]) not in self.has_visited:
                self.available_position[self.current_position].append((self.current_position[0] + 1, self.current_position[1]))
            if (self.current_position[0] - 1, self.current_position[1]) not in self.has_visited and self.current_position[0] - 1 >= 0:
                self.available_position[self.current_position].append((self.current_position[0] - 1, self.current_position[1]))
            if (self.current_position[0], self.current_position[1] + 1) not in self.has_visited:
                self.available_position[self.current_position].append((self.current_position[0], self.current_position[1] + 1))
            if (self.current_position[0], self.current_position[1] - 1) not in self.has_visited and self.current_position[1] - 1 >= 0:
                self.available_position[self.current_position].append((self.current_position[0], self.current_position[1] - 1))


    def analysis(self):
        print("action list = ", self.actionlist)
        self.has_visited.append(self.current_position)

        if self.current_position == (0, 0) and self._current_status['breeze'] == True:
            self.actionlist.append(Agent.Action.CLIMB)
            return ['ACTION']

        if self.current_position not in self.available_position.keys():
            self.check_current_position_available_direction()

        print("has visited = ", self.has_visited)
        print("available position = ", self.available_position)
        print("available position keys = ", self.available_position.keys())
        print("current position = ", self.current_position)
        print("current status = ", self._current_status)

        if len(self.available_position[self.current_position]) > 0:
            print(1)
            next_spot = self.available_position[self.current_position].pop()
            # self.available_position[self.current_position].append(next_spot)
            return ['MOVEMENT', next_spot]
        else:
            print(2)
            next_spot = self.has_visited.pop()
            next_spot = self.has_visited.pop()

            return ['MOVEMENT', next_spot]

        # #if forward position has't visited yet, visit it.
        # if self.get_current_direction_forward_position() not in self.has_visited and not self._current_status['stench'] and not self._current_status['breeze']:
        #     self.has_visited.append(self.get_current_direction_forward_position())
        #     return ['MOVEMENT', self.get_current_direction_forward_position()]




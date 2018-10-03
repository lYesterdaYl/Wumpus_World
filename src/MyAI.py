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
        self._current_direction = ''
        self._number_of_move = 0
        self._current_status = {}
        self._world_map = World_Map()

    def store_information(self, stench, breeze, glitter, bump, scream):
        self._current_status['stench'] = stench
        self._current_status['breeze'] = breeze
        self._current_status['glitter'] = glitter
        self._current_status['bump'] = bump
        self._current_status['scream'] = scream
        print(self._current_status)


    def analysis(self):
        if(self._number_of_move == 0 and self._current_status['breeze'] == True):
            return Agent.Action.CLIMB

    def found_gold(self):
        if(self._current_status['glitter']):
            return True
        else:
            return False

    def getAction( self, stench, breeze, glitter, bump, scream ):
        self.store_information(stench, breeze, glitter, bump, scream)
        self._world_map.update_current_position(self._current_status)
        self._world_map.show_map()

        feedback = self.analysis()


        self._number_of_move += 1
        return feedback

class World_Map:

    def __init__(self):
        self._x = 0
        self._y = 0
        self._map = [["" for x in range(4)] for x in range(4)]

    def show_map(self):
        # self._map[0][1] = 2
        print("world map is ", self._map)
        # print(self._map[0][0])

    def update_current_position(self, current_status):
        if current_status['stench']: self._map[self._x][self._y] += ' S '
        if current_status['breeze']: self._map[self._x][self._y] += ' B '
        if current_status['glitter']: self._map[self._x][self._y] += ' G '


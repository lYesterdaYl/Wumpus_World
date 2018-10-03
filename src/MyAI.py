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

    def store_information(self, stench, breeze, glitter, bump, scream):
        self._current_status['stench'] = stench
        self._current_status['breeze'] = breeze
        self._current_status['glitter'] = glitter
        self._current_status['bump'] = bump
        self._current_status['scream'] = scream
        print(self.__current_status)


    def analysis(self):
        if(self.__number_of_move == 0 and self.__current_status['breeze'] == True):
            return Agent.Action.CLIMB



    def getAction( self, stench, breeze, glitter, bump, scream ):
        self.store_information(stench, breeze, glitter, bump, scream)

        feedback = self.analysis()


        self.__number_of_move += 1
        return feedback

class Map:

    def __init__(self):
        self._x = 0
        self._y = 0
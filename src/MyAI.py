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
        self.__current_direction = ''
        self.__number_of_move = 0
        self.__current_status = {}

    def store_information(self, stench, breeze, glitter, bump, scream):
        self.__current_status['stench'] = stench
        self.__current_status['breeze'] = breeze
        self.__current_status['glitter'] = glitter
        self.__current_status['bump'] = bump
        self.__current_status['scream'] = scream
        print(self.__current_status)


    def analysis(self):
        if(self.__number_of_move == 0 and self.__current_status['breeze'] == True):
            return Agent.Action.CLIMB



    def getAction( self, stench, breeze, glitter, bump, scream ):
        self.store_information(stench, breeze, glitter, bump, scream)

        feedback = self.analysis()


        self.__number_of_move += 1
        return feedback

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
            # result = self._world_map.analysis()
            # path = self._world_map.localsearch(1,0)
            # print("action path",path)
            # if path != None:
            #     for a in path:
            #         self._world_map.moveTo(a[0],a[1])
            #     return self._world_map.actionlist.pop(0)
            # else: print("none")
            result = self._world_map.analysis()
            print("result = ", result)
            if result[0] == 0:
                return self._world_map.actionlist.pop(0)
            if result[0] == 'ACTION':
                return self._world_map.actionlist.pop(0)
            elif result[0] == 'GRAB':
                if self._world_map.actionlist == []:
                    self._world_map.actionlist.append(Agent.Action.GRAB)
                    #x,y =result[2].pop()
                    return self._world_map.actionlist.pop(0)
            elif result[0] == 'MOVEMENT':
                if self._world_map.actionlist == []:
                    self._world_map.moveTo(result[1][0],result[1][1])
                    print("movement: ", self._world_map.actionlist)
                    return self._world_map.actionlist.pop(0)
        else:
            return self._world_map.actionlist.pop(0)


class World_Map:
    def __init__(self):
        self.max_x = 10
        self.max_y = 10
        self._map = [["" for x in range(10)] for x in range(10)]

        self.has_gold = False

        self._current_direction = 'right'
        self._number_of_move = 0
        self._current_status = {}

        self.has_visited = []
        self.explored = [[False for x in range(10)] for x in range(10)]
        self.explored[0][0] = True
        self.available_position = {}

        self._store_point = {}

        self._safe_position = [[False for x in range(4)] for y in range(4)]
        self._breeze_position = [[False for x in range(4)] for y in range(4)]
        self._stench_position = [[False for x in range(4)] for y in range(4)]
        self._Pit_position = [[False for x in range(4)] for y in range(4)]
        self.current_position = (0, 0)
        self.actionlist=[]

    def bumped(self):
        if self._current_status['bump'] and self._current_direction == 'up':
            self.max_y=self.current_position[1]
            self.current_position = (self.current_position[0],self.current_position[1] -1)
        if self._current_status['bump'] and self._current_direction == 'right':
            self.max_x=self.current_position[0]
            self.current_position = (self.current_position[0]-1,self.current_position[1])


    def make_neighbor(self,x,y):
        neighbor_list=[]
        up = (x, y+1)
        neighbor_list.append(up)
        down = (x, y-1)
        neighbor_list.append(down)
        right = (x+1, y)
        neighbor_list.append(right)
        left = (x-1, y)
        neighbor_list.append(left)
        safe_neighbor=[]

        for p in neighbor_list:
            for a in self.available_position.values():
                if p in a:
                    safe_neighbor.append(p)
                    break
            if self.explored[p[0]][p[1]] or p in self.available_position.keys():
                if p not in safe_neighbor:
                    safe_neighbor.append(p)
        return safe_neighbor

    def calculate_cost(self,dx,dy,goal):
        #using A* search: h(n)+g(n) find the shorst path
        x, y = self.current_position
        cost=0
        #estimated cost h(n)
        if dx < x:
            if self._current_direction == 'right':
                cost = 2
            if self._current_direction == 'up':
                cost = 1
            if self._current_direction == 'down':
                cost = 1
        if dx > x:
            if self._current_direction == 'left':
                cost = 2
            if self._current_direction == 'up':
                cost = 1
            if self._current_direction == 'down':
                cost = 1
        if dy > y:
            if self._current_direction == 'left':
                cost = 1
            if self._current_direction == 'right':
                cost = 1
            if self._current_direction == 'down':
                cost = 2
        if dy < y:
            if self._current_direction == 'left':
                cost = 1
            if self._current_direction == 'right':
                cost = 1
            if self._current_direction == 'up':
                cost = 2
        #calculate actual path cost g(n)
        cost += (abs(goal[0]-dx)+abs(goal[1]-dy))
        return cost


    def localsearch(self, dx, dy):
        #find the a lowest cost path to the position

        count = 0
        mincost_node=()
        temp=[self.current_position]
        path=[self.current_position]
        while True:
            mincost = 100
            a = temp.pop()
            #random restart
            #print("p!",a)
            neighbor = self.make_neighbor(a[0],a[1])
            print("local search neighbot",neighbor)
            for n in neighbor:
                if n not in path:
                    cost = self.calculate_cost(n[0],n[1],(dx,dy))
                    if cost<mincost:
                        mincost = cost
                        mincost_node = n
            print("mincost_node",mincost_node,a)
            if mincost_node == a:
                break
            temp.append(mincost_node)
            path.append(mincost_node)
            if mincost_node == (dx,dy):
                path.pop(0)
                print("local_search", path)
                return path
            count += 1

        return None




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
                self.actionlist.append(Agent.Action.TURN_LEFT)
            if self._current_direction == 'right':
                self.actionlist.append(Agent.Action.TURN_RIGHT)
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
            if (self.current_position[0], self.current_position[1] + 1) not in self.has_visited and self.current_position[1] + 1 < self.max_y:
                self.available_position[self.current_position].append((self.current_position[0], self.current_position[1] + 1))
            if (self.current_position[0] + 1, self.current_position[1]) not in self.has_visited and self.current_position[0] + 1 < self.max_x:
                self.available_position[self.current_position].append((self.current_position[0] + 1, self.current_position[1]))
            if (self.current_position[0] - 1, self.current_position[1]) not in self.has_visited and self.current_position[0] - 1 >= 0:
                self.available_position[self.current_position].append((self.current_position[0] - 1, self.current_position[1]))
            if (self.current_position[0], self.current_position[1] - 1) not in self.has_visited and self.current_position[1] - 1 >= 0:
                self.available_position[self.current_position].append((self.current_position[0], self.current_position[1] - 1))

    def analysis(self):
        # if self._number_of_move > 30:
        #     self.has_gold = True
        print("action list = ", self.actionlist)
        self.bumped()
        #if the player has gold, go home and climb
        if self.has_gold and self.current_position == (0, 0):
            self.actionlist.append(Agent.Action.CLIMB)
            return ['ACTION']
        elif self.has_gold:
            path = self.localsearch(0, 0)
            print("action path", path)
            if path != None:
                temp = self._current_direction
                for a in path:
                    self.moveTo(a[0], a[1])
                self.current_direction=temp

            #return ['MOVEMENT', next_spot]

        #pop out all the duplicate locations that were visited current location
        if self.current_position in self.has_visited:
            while self.has_visited[-1] != self.current_position:
                self.has_visited.pop()
        else:
            self.has_visited.append(self.current_position)

        if self.current_position == (0, 0) and self._current_status['breeze'] == True:
            self.actionlist.append(Agent.Action.CLIMB)
            return ['ACTION']


        if self.current_position == (0, 0) and self._current_status['stench'] == True:
            self.actionlist.append(Agent.Action.CLIMB)
            # self.actionlist.append(Agent.Action.SHOOT)
            return ['ACTION']


        if self._current_status['glitter'] == True:
            self.has_gold = True
            return ['GRAB',(0, 0),self.has_visited]


        if self.current_position not in self.available_position.keys():
            self.check_current_position_available_direction()

        print("has visited = ", self.has_visited)
        print("available position = ", self.available_position)
        print("available position values = ", self.available_position.values())
        print("current position = ", self.current_position)
        print("current status = ", self._current_status)

        while len(self.available_position[self.current_position]) > 0:
            print(1)
            next_spot = self.available_position[self.current_position].pop()
            x,y=next_spot
            #if is a visited node continue the while loop
            #if is  unvisited return
            if self.explored[x][y] == False:
                self.explored[x][y] = True
                # self.available_position[self.current_position].append(next_spot)
                return ['MOVEMENT', next_spot]
        if len(self.available_position[self.current_position]) == 0:
            print(2)
            if self.current_position == (0,0) or len(self.has_visited)<2:
                self.actionlist.append(Agent.Action.CLIMB)
                return ['ACTION']
            # empty =True
            # unvisited = self.available_position.values()
            # for a in unvisited:
            #     if a !=[]:
            #         empty =False
            # if empty == True:
            #     path = self.localsearch(0, 0)
            #     if path != None:
            #         temp = self._current_direction
            #         for a in path:
            #             self.moveTo(a[0], a[1])
            #         self._current_direction=temp
            #         return [0]
            # m=100
            # next_spot=()
            # for nq in unvisited:
            #     for n in nq:
            #         if n!=[]:
            #             cost = (abs(n[0]-self.current_position[0])+abs(n[1]-self.current_position[1]))
            #             print("n", n, cost, m)
            #             if cost<m and n!= self.current_position and self.explored[n[0]][n[1]] !=True:
            #                 m=cost
            #                 next_spot=n
            # print("next_spot", next_spot)
            # if next_spot==():
            #     path = self.localsearch(0, 0)
            #     if path != None:
            #         temp = self._current_direction
            #
            #         for a in path:
            #             self.moveTo(a[0], a[1])
            #
            #         self._current_direction=temp
            #         return [0]
            #
            #
            # path = self.localsearch(next_spot[0],next_spot[1])
            # print("action path", path)
            # for k in list(self.available_position.keys()):
            #     if next_spot in self.available_position[k]:
            #         self.available_position[k].remove(next_spot)
            # if path != None:
            #     temp = self._current_direction
            #
            #     for a in path:
            #         self.moveTo(a[0], a[1])
            #
            #     self._current_direction=temp
            # self.explored[next_spot[0]][next_spot[1]] = True
            # return [0]
            next_spot = self.has_visited.pop()
            next_spot = self.has_visited.pop()
            return ['MOVEMENT', next_spot]





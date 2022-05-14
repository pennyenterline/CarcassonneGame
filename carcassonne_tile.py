'''

 Author: Penny Enterline
 Class: CSC 120 Spring 2022
 Description: Implements the tile class for the
              Carcassonne game

'''

class CarcassoneTile:
    '''
    composed of different methods
    for classifying the board
    tiles
    '''
    def __init__(self, tile):
        '''
        constructor class
        '''
        self._tile = tile
    def get_edge(self, side):
        '''
        returns a string which indicates
        what is on that side of the tile
        '''
        if 'c' in self._tile[side]:
            return 'city'
        elif self._tile[side] == 'r':
            return 'grass+road'
        elif self._tile[side] == 'g':
            return 'grass'
    def edge_has_road(self, side):
        '''
        returns True or False, based on whether
        that edge has a road.
        '''
        if self._tile[side] == 'r':
            return True
        else:
            return False
    def edge_has_city(self, side):
        '''
        returns True or False, based on whether
        that edge has a city.
        '''
        if 'c' in self._tile[side]:
            return True
        else:
            return False
    def has_crossroads(self):
        '''
        returns True or False, based on whether that
        tile has a “crossroads” in the middle of it
        '''
        i = 0
        for side in self._tile:
            if side == 'r':
                i += 1
        if i >= 3:
            return True
        return False
    def road_get_connection(self, from_side):
        '''
        returns the side that a given
        road is connected to
        '''
        i = 0
        for side in self._tile:
            if side == 'r':
                i += 1
        if i >= 3:
            return -1
        else:
            z = 0
            for nside in self._tile:
                if nside == 'r' and z != from_side:
                    return z
                z += 1
    def city_connects(self, sideA, sideB):
        '''
        returns True or False, based on
        whether or not the two sides are
        both cities and they are connected
        '''
        if self._tile[sideA] == self._tile[sideB]:
            if self._tile[sideA] == 'c+':
                return True
        if sideA == sideB:
            return True
        return False
    def rotate(self):
        new_tile = self._tile
        temp_last = self._tile[3]
        new_list = [temp_last]
        i = 0
        for side in new_tile:
            if i < 3:
                new_list.append(side)
            i += 1
        return CarcassoneTile(new_list)



tile01 = CarcassoneTile(['c', 'r', 'g', 'r'])
tile02 = CarcassoneTile(['c+', 'c+', 'g', 'c+'])
tile03 = CarcassoneTile(['r', 'r', 'r', 'r'])
tile04 = CarcassoneTile(['c', 'r', 'r', 'g'])
tile05 = CarcassoneTile(['c+', 'c+', 'c+', 'c+'])
tile06 = CarcassoneTile(['r', 'g', 'r', 'g'])
tile07 = CarcassoneTile(['g', 'c', 'g', 'c'])
tile08 = CarcassoneTile(['g', 'c+', 'g', 'c+'])
tile09 = CarcassoneTile(['c+', 'c+', 'g', 'g'])
tile10 = CarcassoneTile(['g', 'r', 'r', 'r'])
tile11 = CarcassoneTile(['c+', 'r', 'r', 'c+'])
tile12 = CarcassoneTile(['c', 'g', 'r', 'r'])
tile13 = CarcassoneTile(['c', 'r', 'r', 'r'])
tile14 = CarcassoneTile(['c', 'c', 'g', 'g'])
tile15 = CarcassoneTile(['g', 'g', 'r', 'r'])
tile16 = CarcassoneTile(['c', 'g', 'g', 'g'])

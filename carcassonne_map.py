'''

 Author: Penny Enterline
 Class: CSC 120 Spring 2022
 Description: Implements the map class for the
              Carcassonne game

'''

from carcassonne_tile import *

class CarcassonneMap:
    '''
        composed of different methods
        for creating and editing
        the game board
        '''
    def __init__(self):
        '''
        constructor class
        '''
        self._board = {
            (0, 0): tile01
        }

    def get_all_coords(self):
        '''
        dumps all the coordinates
        of the tiles
        '''
        border = set()
        for tile in self._board:
            if self._board[tile] is not None:
                border.add(tile)
        return border

    def find_map_border(self):
        '''
        finds the border of the game,
        all the of the places that
        could have tiles added to
        them
        '''
        border = set()
        coords = list(self._board.keys())
        for coord in coords:
            if self._board[coord] is not None:
                N = (coord[0], coord[1] + 1)
                E = (coord[0] + 1, coord[1])
                S = (coord[0], coord[1] - 1)
                W = (coord[0] - 1, coord[1])
                if N not in self._board:
                    self._board[N] = None
                if E not in self._board:
                    self._board[E] = None
                if S not in self._board:
                    self._board[S] = None
                if W not in self._board:
                    self._board[W] = None
        for tile in self._board:
            if self._board[tile] is None:
                border.add(tile)
        return border

    def get(self, x, y):
        '''
        gets the tile at a certain x,y
        if there is no tile, return None
        '''
        try:
            if self._board[(x, y)] is not None:
                return self._board[(x, y)]
            else:
                return None
        except KeyError:
            return None

    def add(self, x, y, tile, confirm=True, tryOnly=False):
        '''
        Adds a given tile, at the given x,y location
        Returns True if the tile was added to the map,
        or False if there was some reason
        it could not be added.
        '''
        check = [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]
        adjacency = False
        for index in check:
            if index in self._board:
                try:
                    if isinstance(self._board[index], CarcassoneTile):
                        adjacency = True
                except KeyError:
                    pass
        if adjacency:
            # checks to see if the sides match up
            valid_to_add = True
            directions = [2, 3, 0, 1]
            for i in range(0, 4):
                if check[i] in self._board:
                    if tile is not None and self._board[check[i]] is not None:
                        if not (tile.get_edge(i) ==
                                self._board[check[i]].get_edge(directions[i]) or None):
                            valid_to_add = False
            if confirm and not tryOnly:
                if valid_to_add:
                    self._board[(x, y)] = tile
                return valid_to_add
            elif confirm and tryOnly:
                return valid_to_add
            elif not confirm and not tryOnly:
                self._board[(x, y)] = tile
                return True
            self.find_map_border()
        else:
            return False

    def trace_road_one_direction(self, x, y, side):
        '''
        traces the road in one direction
        x is the x value of the starting tile
        y is the y value of the starting tile
        side is the side that the road is on
        returns a sequence of tuples which represent
        the entire path
        '''
        coords = (x, y)
        if side == 0:
            next_tile_edge = 2
            cur_tile_edge = 0
            path = self.road_recurse(coords, (x, y, next_tile_edge, 0),
                                     cur_tile_edge)
        elif side == 1:
            next_tile_edge = 3
            cur_tile_edge = 1
            path = self.road_recurse(coords, (x, y, next_tile_edge, 0),
                                     cur_tile_edge)
        elif side == 2:
            next_tile_edge = 0
            cur_tile_edge = 2
            path = self.road_recurse(coords, (x, y, next_tile_edge, 0),
                                     cur_tile_edge)
        else:
            next_tile_edge = 1
            cur_tile_edge = 3
            path = self.road_recurse(coords, (x, y, next_tile_edge, 0),
                                     cur_tile_edge)
        return path

    def road_recurse(self, start_coord, coord, cur_tile_edge):
        '''
        helper function for trace road one direction
        returns the path for the road
        '''
        path = []
        x = coord[0]
        y = coord[1]
        next_tile_edge = coord[2]
        start_check = coord[3]
        cur_tile = self._board[(x, y)]
        try:
            next_tile = None
            if cur_tile_edge == 0:
                next_tile = self._board[(x, y + 1)]
            elif cur_tile_edge == 1:
                next_tile = self._board[(x + 1, y)]
            elif cur_tile_edge == 2:
                next_tile = self._board[(x, y - 1)]
            elif cur_tile_edge == 3:
                next_tile = self._board[(x - 1, y)]
        except KeyError:
            next_tile = None
        if next_tile is None:
            return []
        if next_tile.has_crossroads():
            if cur_tile_edge == 0:
                path.append((x, y + 1, next_tile_edge, -1))
            elif cur_tile_edge == 1:
                path.append((x + 1, y, next_tile_edge, -1))
            elif cur_tile_edge == 2:
                path.append((x, y - 1, next_tile_edge, -1))
            elif cur_tile_edge == 3:
                path.append((x - 1, y, next_tile_edge, -1))
            return path
        if next_tile.get_edge(next_tile_edge) == \
                cur_tile.get_edge(cur_tile_edge):
            dir = 0
            for i in range(0, 4):
                if next_tile.get_edge(i) == 'grass+road' \
                        and i != next_tile_edge:
                    dir = i
            if cur_tile_edge == 0:
                path.append((x, y + 1, next_tile_edge, dir))
                y += 1
            elif cur_tile_edge == 1:
                path.append((x + 1, y, next_tile_edge, dir))
                x += 1
            elif cur_tile_edge == 2:
                path.append((x, y - 1, next_tile_edge, dir))
                y -= 1
            elif cur_tile_edge == 3:
                path.append((x - 1, y, next_tile_edge, dir))
                x -= 1
            if start_check == 1 and start_coord == (x, y):
                return path
            if dir == 0:
                path = path + self.road_recurse(start_coord, (x, y, 2, 1), dir)
            elif dir == 1:
                path = path + self.road_recurse(start_coord, (x, y, 3, 1), dir)
            elif dir == 2:
                path = path + self.road_recurse(start_coord, (x, y, 0, 1), dir)
            elif dir == 3:
                path = path + self.road_recurse(start_coord, (x, y, 1, 1), dir)
        return path

    def trace_road(self, x, y, side):
        """
        traces the road in both directions
        x is the x value of the starting tile
        y is the y value of the starting tile
        side is the side that the road is on
        returns a sequence of tuples which represent
        the entire path
        """
        # assign variables
        cur_tile = self._board[(x, y)]
        directions = []
        paths = []
        return_path = []
        other_dir = -2
        # checks which sides have roads
        for i in range(0, 4):
            if cur_tile.get_edge(i) == 'grass+road':
                directions.append(i)
        # checks to see where the connections are
        for i in directions:
            if i != side:
                other_dir = i
        if len(directions) > 2:
            return [(x, y, -1, side)] +\
                   self.trace_road_one_direction(x, y, side)
        # uses the previous trace road function
        # to find both ends
        for dir_ in directions:
            path = self.trace_road_one_direction(x, y, dir_)
            paths.append(path)
        if len(paths[0]) == len(paths[1]):
            if not paths[0] or not paths[1]:
                pass
            else:
                end_one = paths[0][-1]
                end_two = paths[1][-1]
                if (end_one[0] == x and end_one[1] == y)\
                        and (end_two[0] == x and end_two[1] == y):
                    if side == 0 or side == 1:
                        return paths[0]
                    elif side == 2 or side == 3:
                        return paths[-1]
        if side == directions[0]:
            paths[1] = paths[1][::-1]
            paths = paths[::-1]
        else:
            paths[0] = paths[0][::-1]
        count = 0
        for direction in range(len(paths)):
            if count == 1:
                if side == 0:
                    return_path.append((x, y, other_dir, side))
                elif side == 1:
                    return_path.append((x, y, other_dir, side))
                elif side == 2:
                    return_path.append((x, y, other_dir, side))
                else:
                    return_path.append((x, y, other_dir, side))
            for i in range(len(paths[direction])):
                return_path.append(paths[direction][i])
            count += 1
        for coord in range(len(return_path)):
            if return_path[coord][0] == x and return_path[coord][1] == y:
                break
            else:
                return_path[coord] = (return_path[coord][0],
                                      return_path[coord][1],
                                      return_path[coord][3],
                                      return_path[coord][2])
        return return_path

    def trace_city(self, x, y, side):
        '''
        finds all of the parts of the city
        returns a tuple with two elements:
        a Boolean and the set of edges
        x is the x value of the starting tile
        y is the y value of the starting tile
        side is the side that the city is on
        '''
        # declare variables
        city = [(x, y, side)]
        confirm = [(x, y, side)]
        complete_city = True
        while confirm:
            temp = -1
            if confirm:
                temp = confirm[0]
            if len(confirm) >= 1:
                confirm = confirm[1:]
            x = temp[0]
            y = temp[1]
            from_dir = temp[2]
            cur_tile = self._board[x, y]
            # checks to see when the edge is city
            for i in range(0, 4):
                if cur_tile.get_edge(i) == 'city':
                    if cur_tile.city_connects(from_dir, i)\
                            and (x, y, i) not in city:
                        confirm.append((x, y, i))
                        city.append((x, y, i))
            # checks to see if the next tile exists
            # as well as its direction
            try:
                next_tile = None
                if from_dir == 0:
                    next_tile = self._board[(x, y + 1)]
                elif from_dir == 1:
                    next_tile = self._board[(x + 1, y)]
                elif from_dir == 2:
                    next_tile = self._board[(x, y - 1)]
                elif from_dir == 3:
                    next_tile = self._board[(x - 1, y)]
            except KeyError:
                next_tile = None
            # checks to see if the next tile has a city
            if next_tile is None:
                complete_city = False
            else:
                if from_dir == 0 and (x, y + 1, 2) not in city:
                    confirm.append((x, y + 1, 2))
                    city.append((x, y + 1, 2))
                elif from_dir == 1 and (x + 1, y, 3) not in city:
                    confirm.append((x + 1, y, 3))
                    city.append((x + 1, y, 3))
                elif from_dir == 2 and (x, y - 1, 0) not in city:
                    confirm.append((x, y - 1, 0))
                    city.append((x, y - 1, 0))
                elif from_dir == 3 and (x - 1, y, 1) not in city:
                    confirm.append((x - 1, y, 1))
                    city.append((x - 1, y, 1))
        return complete_city, sorted(city)

ALLOWABLE_TERRAINS = ["mountain", "desert", "sea", "field"]
ALLOWABLE_DEVELOPMENTS = ["none", "farmland", "town", "village"]
ALLOWABLE_TRANSPORT = ["none", "road", "canal"]
ALLOWABLE_POPS = ["hunter-gatherers", "farmers", "craftsmen", "nobles"]
ALLOWABLE_RESOURCES = ["pop-cap", "commodities"]

class Tile:
    """Class for storign information on a tile.

    Args:
        terrain (str): Terrain type, must be from ALLOWABLE_TERRAINS list.
        development (str): Name of the development (e.g. village, town, city) the tile is a part of
        market (str): Name of the market that the tile is in.
        transport (str): Type of transport on tile. Must be from ALLOWABLE_TRANSPORT list.
        pop (dict): Population size, as a dictionary. Key is the population type, value is the number. Keys must be from ALLOWABLE_POPS list.

    """
    
    def __init__(self, terrain, development, market, transport, pop, resources):
        if not (terrain in ALLOWABLE_TERRAINS):
            raise ValueError(f"Terrain must be in the list {ALLOWABLE_TERRAINS}")
        else:
            self.terrain = terrain

        self.development = development
        self.market = market
        self.transport = transport
        self.pop = pop
        self.resources = resources


class Development:
    def __init__(self, name, type):
        self.name = name

        if not (type in ALLOWABLE_DEVELOPMENTS):
            raise ValueError(f"Development 'type' must be in the list {ALLOWABLE_DEVELOPMENTS}")
        else:
            self.type = type

class Market:
    def __init__(self, name, commodities = 0):
        self.name = name
        self.commodities = commodities



class Game:
    def __init__(self, n_x, n_y):
        """Class for storing all the information on a map grid.

        Args:
            n_x (int): Number of x points (width).
            n_y (int): Number of y points (height).
        """
        
        self.grid = [ [None]*n_x for i in range(n_y)]          # This generates a list full of 'None' objects, with dimensions n_x by n_y.
        self.cities = []
        self.markets = []

    def generate_map(self):
        # Incomplete
        pass 
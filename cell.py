from enum import Enum
import random
from mesa import Agent

class Cell(Agent):
    """Description of the grid points of the CA"""
    class CellState(Enum):
        """An enum that determines the states that the cells in our CA can be in.

        Because we use a SIR model they can either be S -- SUSCEPTIBLE, I -- INFECTED, or R -- RECOVERED
        
        We use the values to colour the cells later on (in server.py).
        """
        SUSCEPTIBLE = "grey"
        INFECTED    = "red"
        RECOVERED   = "blue"
    
    def __init__(self, position, model, initial_state = 0):
        """Create cell in given x,y position, with given initial state"""
        # Ceremony for the super class:
        super().__init__(positon,model)
        self.x,self.y           = pos
        self.state              = init_state

        # Ceremony for the framework:
        self._nextstate         = None
        self._nextinf           = None
        self._nextinfduration   = None

        # Stuff that is relevant to our model:
        self.time               = 0          # Duration infection
        self.infection_duration = 0
        self.infection          = 0.0        # Infectivity

    def step(self):
        """Compute the next state of a cell"""
        # Assume cell is unchanged, unless something happens below
        self._nextinf = self.inf
        self._nextinfduration = self.infduration
        self._nextstate = self.state
        
        # Empty squares - potential reproduction of susceptibles
        # No reproduction 
        #if self.state == 0:
        #   Susneighbors = 0
        #   neis = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False)
        #   for nei in neis:
        #       if nei.state == self.Susceptible:
        #            Susneighbors += 1
        #    if Susneighbors > 0:
        #        if random.random() < self.model.r*Susneighbors:
        #            self._nextstate = self.Susceptible

        # Susceptibles - might die or get infected
        if self.state == self.Susceptible:
            # Natural death
            #if random.random() < self.model.d:
            if False:
            #    self._nextstate = 0
            # Infection?
            else:
                neis = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False)
                tot_inf = 0.0
                for nei in neis:
                    if nei.state == self.Infected:
                        tot_inf += nei.inf
                infprob = 0.0
                if tot_inf > 0:
                    infprob = tot_inf / (tot_inf + self.model.h_inf)
                if random.random() < infprob:
                    self._nextstate = self.Infected
                    # Inherit infectivity of one infecting neighbour
                    infprobsum = 0.0
                    rand = random.uniform(0, tot_inf)
                    for nei in neis:
                        if nei.state == self.Infected:
                            infprobsum += nei.inf
                            if rand < infprobsum:
                                # Inherit pathogen characteristics from infecting neighbour
                                self._nextinf = nei.inf
                                self._nextinfduration = nei.infduration
                                break

        # Infected - might die naturally or die after disease_duration
        #Becomr R instead Empty
        #elif self.state == self.Infected:
        #    # Natural death or death by disease
        #    if random.random() < self.model.d or self.timecounter > self.infduration:
        #        self._nextstate = 0
        #        self._nextinf = 0.0
        #        self._nextinfduration = 0
        #        self.timecounter = 0
        #    # Else count how long it has been ill and apply potential mutations
        #    else:
        #        self.timecounter += 1

        elif self.state == self.Infected:
            # Natural death or death by disease
            if  self.timecounter > self.infduration:
                self._nextstate = self.Recovered
                self._nextinf = 0.0
                self._nextinfduration = 0
                self.timecounter = 0
            # Else count how long it has been ill and apply potential mutations
            else:
                self.timecounter += 1        

    def advance(self): 
        self.state = self._nextstate
        self.inf = self._nextinf
        self.infduration = self._nextinfduration

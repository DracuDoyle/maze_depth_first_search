import pygame
import random

# Window Settings
WIDTH, HEIGHT = 1200, 600
CELL_SIZE = 50
BOLD = 3
COLOR_MAZE = "white"
COLOR_PATHFINDING = "cadetblue4"
POINTS_COLOR = "darkred"

# Init Pygame
pygame.init()
window = pygame.display.set_mode( ( WIDTH, HEIGHT ) )
pygame.display.set_caption( "Laberinto - Busqueda en Profundidad" )
clock = pygame.time.Clock()

# Def Grid
cols, rows = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
Grid = []
Stack = []


# Class to represent each cell of the maze
class Cell :
    
    def __init__( self, x, y ) :
        self.x, self.y = x, y
        self.walls = { "top": True, "right": True, "bottom": True, "left": True }
        self.visited = False
        self.on_path = False  # To mark the path from start to end

    def Draw( self, surface ) :
        
        x, y = self.x * CELL_SIZE, self.y * CELL_SIZE

        if self.visited:
            pygame.draw.rect( surface, COLOR_MAZE, ( x, y, CELL_SIZE, CELL_SIZE ) )

        if self.on_path:  # Color the path differently
            pygame.draw.rect( surface, COLOR_PATHFINDING, ( x, y, CELL_SIZE, CELL_SIZE ) )
        
        # Draw Walls
        if self.walls[ "top" ] :
            pygame.draw.line( surface, "black", ( x, y ), ( x + CELL_SIZE, y ), BOLD )
        if self.walls[ "right" ] :
            pygame.draw.line( surface, "black", ( x + CELL_SIZE, y ), ( x + CELL_SIZE, y + CELL_SIZE ), BOLD )
        if self.walls[ "bottom" ] :
            pygame.draw.line( surface, "black", ( x + CELL_SIZE, y + CELL_SIZE ), ( x, y + CELL_SIZE ), BOLD )
        if self.walls[ "left" ] :
            pygame.draw.line( surface, "black", ( x, y + CELL_SIZE ), ( x, y ), BOLD )

    def Check_Neighbors( self ):
        
        Neighbors = []

        top = Get_Cell( self.x, self.y - 1 )
        right = Get_Cell( self.x + 1, self.y )
        bottom = Get_Cell( self.x, self.y + 1 )
        left = Get_Cell( self.x - 1, self.y )

        if top and not top.visited :
            Neighbors.append( top )
        if right and not right.visited :
            Neighbors.append( right )
        if bottom and not bottom.visited :
            Neighbors.append( bottom )
        if left and not left.visited :
            Neighbors.append( left )

        if Neighbors :
            return random.choice( Neighbors )
        else:
            return None


def Get_Cell( x, y ) :
    
    if x < 0 or y < 0 or x >= cols or y >= rows :
        return None
    
    return Grid[ x + y * cols ]


def Remove_Walls( current, next ) :
    
    dx = current.x - next.x
    dy = current.y - next.y

    if dx == 1 :
        current.walls[ "left" ] = False
        next.walls[ "right" ] = False
    elif dx == -1 :
        current.walls[ "right" ] = False
        next.walls[ "left" ] = False
    if dy == 1 :
        current.walls[ "top" ] = False
        next.walls[ "bottom" ] = False
    elif dy == -1 :
        current.walls[ "bottom" ] = False
        next.walls[ "top" ] = False


# Init Cell Grid
for y in range( rows ) :
    for x in range( cols ) :
        Grid.append( Cell( x, y ) )


# Settings For DFS
current_cell = Grid[ 0 ]
current_cell.visited = True
Stack.append( current_cell )


# Main Loop
running = True

while running :
    
    clock.tick( 120 )
    window.fill( "black" )

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False

    # Draw each cell in the grid
    for cell in Grid :
        cell.Draw( window )

    # DFS algorithm to create the maze
    next_cell = current_cell.Check_Neighbors()
    
    if next_cell :
        
        next_cell.visited = True
        Stack.append( current_cell )
        Remove_Walls( current_cell, next_cell )
        current_cell = next_cell

    elif Stack :
        
        current_cell = Stack.pop()

    else :

        # Maze generation is complete, move to next phase
        running = False

    pygame.display.flip()


# Define start and end points
start_cell = Grid[ 0 ]  # Top-left corner ( 0, 0 )
end_cell = Grid[ -1 ]   # Bottom-right corner ( CELL_SIZE - 1, CELL-SIZE - 1 )

# Draw start and end points
pygame.draw.rect( window, POINTS_COLOR, ( start_cell.x * CELL_SIZE, start_cell.y * CELL_SIZE, CELL_SIZE, CELL_SIZE ) )
pygame.draw.rect( window, POINTS_COLOR, ( end_cell.x * CELL_SIZE, end_cell.y * CELL_SIZE, CELL_SIZE, CELL_SIZE ) )
pygame.display.flip()

# Short delay to see start and end points before pathfinding begins
pygame.time.delay( 500 )


# Main Loop for Pathfinding Visualization
running = True
path_stack = [ start_cell ]
start_cell.on_path = True


while running:
    
    clock.tick( 60 )
    window.fill( "black" )

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False

    # Draw each cell in the grid
    for cell in Grid :
        cell.Draw( window )

    # Draw start and end points
    pygame.draw.rect( window, POINTS_COLOR, ( start_cell.x * CELL_SIZE, start_cell.y * CELL_SIZE, CELL_SIZE, CELL_SIZE ) )
    pygame.draw.rect( window, POINTS_COLOR, ( end_cell.x * CELL_SIZE, end_cell.y * CELL_SIZE, CELL_SIZE, CELL_SIZE ) )

    # DFS Pathfinding to find the path from start to end
    if path_stack :
        
        current_cell = path_stack[ -1 ]

        if current_cell == end_cell :
            running = False  # Path found

        else :
            
            # Check neighbors that are accessible (walls are down)
            neighbors = []

            if not current_cell.walls[ "top" ] :
                neighbors.append( Get_Cell( current_cell.x, current_cell.y - 1 ) )
            if not current_cell.walls[ "right" ] :
                neighbors.append( Get_Cell( current_cell.x + 1, current_cell.y ) )
            if not current_cell.walls[ "bottom" ] :
                neighbors.append( Get_Cell( current_cell.x, current_cell.y + 1 ) )
            if not current_cell.walls[ "left" ] :
                neighbors.append( Get_Cell( current_cell.x - 1, current_cell.y ) )

            next_cell = None
            for neighbor in neighbors :
                if neighbor and not neighbor.on_path :
                    next_cell = neighbor
                    break

            if next_cell :
                next_cell.on_path = True
                path_stack.append( next_cell )
            else :
                path_stack.pop() # Backtrack if no accessible neighbors

    pygame.display.flip()


# Keep the window open until the user closes it
running = True

while running :
    
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False


pygame.quit()

from __future__ import division
import turtle
turtle.up()

class MeshPoint:
    """Represents a mesh point in the grid."""
    velocity = (0, 0)
    stream_function = 0
    vorticity = 0
SIZE=100 # size of the grid: SIZE by SIZE.
# The grid of mesh points.
grid = [[MeshPoint() for i in xrange(SIZE)] for j in xrange(SIZE)]

class Vortex:
    """Represents a vortex."""
    position = (0, 0)
    velocity = (0, 0)
    vorticity = 0
    def __init__(self, position, vorticity):
        self.position = position
        self.vorticity = vorticity

# The set of all vortices.
vortices = set([Vortex(position=(1, 2), vorticity=1), Vortex(position=(2, 1), vorticity=1)]) ##temp

while True:
    # compute vorticities of the mesh points using cloud-in-cell interpolation.
    for row in grid:
        for point in row:
            point.vorticity = 0
    for vortex in vortices:
        x_coord = int(vortex.position[0]) # integral part
        y_coord = int(vortex.position[1])
        x_fraction = vortex.position[0] % 1 # fractional part
        y_fraction = vortex.position[1] % 1
        grid[x_coord][y_coord].vorticity += vortex.vorticity*(1-x_fraction)*(1-y_fraction)
        grid[x_coord][y_coord+1].vorticity += vortex.vorticity*(1-x_fraction)*y_fraction
        grid[x_coord+1][y_coord].vorticity += vortex.vorticity*x_fraction*(1-y_fraction)
        grid[x_coord+1][y_coord+1].vorticity += vortex.vorticity*x_fraction*y_fraction

    # using Poisson solver, calculate stream function from velocity
    from misctools import poisson_solve
    from numpy import matrix
    vorticity_matrix = matrix([[grid[i][j].vorticity for j in xrange(SIZE)] for i in xrange(SIZE)])
    stream_function_matrix = poisson_solve(vorticity_matrix)
    for i in xrange(SIZE):
        for j in xrange(SIZE):
            grid[i][j].stream_function = stream_function_matrix[i,j]

    # from stream function, calculate the velocity
    from misctools import differentiate
    for i in xrange(SIZE):
        for j in xrange(SIZE):
            x_slice = [point.stream_function for point in grid[i]]
            y_slice = [row[j].stream_function for row in grid]
            grid[i][j].velocity=(differentiate(y_slice)[i], -differentiate(x_slice)[j])

    #using area-weighing interpolation, calculate velocity of each vortex.
    for vortex in vortices:
        x_coord = int(vortex.position[0]) # integral part
        y_coord = int(vortex.position[1])
        x_fraction = vortex.position[0] % 1 # fractional part
        y_fraction = vortex.position[1] % 1
        velocity_x = grid[x_coord][y_coord].velocity[0]*(1-x_fraction)*(1-y_fraction) \
                   + grid[x_coord][y_coord+1].velocity[0]*(1-x_fraction)*y_fraction \
                   + grid[x_coord+1][y_coord].velocity[0]*x_fraction*(1-y_fraction) \
                   + grid[x_coord+1][y_coord+1].velocity[0]*x_fraction*y_fraction
        velocity_y = grid[x_coord][y_coord].velocity[1]*(1-x_fraction)*(1-y_fraction) \
                   + grid[x_coord][y_coord+1].velocity[1]*(1-x_fraction)*y_fraction \
                   + grid[x_coord+1][y_coord].velocity[1]*x_fraction*(1-y_fraction) \
                   + grid[x_coord+1][y_coord+1].velocity[1]*x_fraction*y_fraction
        vortex.velocity = (velocity_x, velocity_y)

    # compute next position of the vortices.
    UNIT_TIME=0.5 # time increment
    for vortex in vortices:
        vortex.position=((vortex.position[0]+vortex.velocity[0]*UNIT_TIME)%(SIZE-1), ## Periodic boundary condition
                         (vortex.position[1]+vortex.velocity[1]*UNIT_TIME)%(SIZE-1))
    
    # plot the vortices
    turtle.clear()
    for vortex in vortices:
        print vortex.position
        turtle.goto(vortex.position[0]*10, vortex.position[1]*10)
        turtle.write('o')
    print '##################'
    import msvcrt
    msvcrt.getch()
    
    import time
    time.sleep(0.5)
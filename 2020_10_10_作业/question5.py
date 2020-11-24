def matrix_rotate(matrix, degrees, clockwise = True):
    if (degrees % 360 == 90 and clockwise) or (degrees % 360 == 270 and not clockwise):
        matrix[:] = map(list, zip(*matrix[::-1]))
    elif (degrees % 360 == 180):
        matrix[:] = map(list, zip(*matrix[::-1]))
        matrix[:] = map(list, zip(*matrix[::-1]))
    elif (degrees % 360 == 270 and clockwise) or (degrees % 360 == 90 and not clockwise):
        matrix[:] = map(list, zip(*matrix[::-1]))
        matrix[:] = map(list, zip(*matrix[::-1]))
        matrix[:] = map(list, zip(*matrix[::-1]))
    else:
        matrix = matrix
    return matrix

matrix = [ [0, 1, 2], [3, 4, 5], [6, 7, 8] ]
print(matrix_rotate(matrix, 270, True))

# [ [6, 3, 0], [7, 4, 1], [8, 5, 2] ]
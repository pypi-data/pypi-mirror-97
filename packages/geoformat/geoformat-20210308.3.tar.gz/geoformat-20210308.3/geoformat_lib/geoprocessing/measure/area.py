

def shoelace_formula(ring_coordinates, absolute_value=True):
    """
    This function give the area of a boundary in the unit of coordinates.
    It is useful to use shoelace_formula to determine encoding sens of boundary coordinates
    (see ccw_or_cw_boundary)

    :param ring_coordinates: list of coordinates
    :param absolute_value: True / False
    :return: ring area (in coordinates unit)
    """
    nb_vertex = len(ring_coordinates)
    nb_edge = nb_vertex - 1

    l = [(ring_coordinates[i + 1][0] - ring_coordinates[i][0]) * (
            ring_coordinates[i + 1][1] + ring_coordinates[i][1]) for i in range(nb_edge)]

    if absolute_value:
        return abs(sum(l) / 2)
    else:
        return sum(l) / 2



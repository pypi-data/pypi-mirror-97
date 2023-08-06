def format_coordinates(coordinates_list_tuple,
                       format_to_type=list,
                       precision=None,
                       delete_duplicate_following_coordinates=False
                       ):
    """
    This function allow to :
        - change type of coordinate's storage
        - round coordinates
        - delete duplicate following coordinates in


    :param coordinates_list_tuple: tuple or list containing coordinates
    :param format_to_type: coordinate storage data type (list (by default) or tuple)
    :param precision: desired number of decimal for coordinates
    :param delete_duplicate_following_coordinates: option to delete similar coordinates that follow each other
    :return: formatted coordinates
    """
    # TODO add delete duplicated part
    if coordinates_list_tuple:
        output_coordinates_list_tuple = [None] * len(coordinates_list_tuple)
        for i_coord, coordinates in enumerate(coordinates_list_tuple):
            if isinstance(coordinates, (int, float)):
                if precision is not None:
                    coordinates = round(coordinates, precision)
                coord_tuple = coordinates
            elif isinstance(coordinates, (list, tuple)):
                # here we first format type of storage of coordinates and precision
                coord_tuple = format_coordinates(coordinates_list_tuple=coordinates,
                                                 format_to_type=format_to_type,
                                                 precision=precision,
                                                 delete_duplicate_following_coordinates=delete_duplicate_following_coordinates)
            else:
                raise TypeError('must be list or tuple containing int or float')

            # save result
            output_coordinates_list_tuple[i_coord] = coord_tuple

        # DELETE DUPLICATE FOLLOWING COORDINATES
        # in step before if we reformat precision we can create duplicate coordinates then if
        # delete_duplicate_following_coordinates is True we have to make a second scan of coordinates
        # if we are at level of part of geometry (list that contains coordinates in it)
        if delete_duplicate_following_coordinates is True and isinstance(output_coordinates_list_tuple[0], (list, tuple)) and isinstance(
                output_coordinates_list_tuple[0][0], (int, float)):
            # scan list of coordinates or list of list of coordinates (don't scan coordinate list)
            # if coordinates
            retype_to_tuple = False
            # transform tuple to list (because we need to edit coordinates)
            if isinstance(output_coordinates_list_tuple, tuple):
                retype_to_tuple = True
                output_coordinates_list_tuple = list(output_coordinates_list_tuple)

            # try to find duplicate coordinates index
            duplicate_coordinates_idx_list = []
            for idx_inside_coord, inside_coordinates in enumerate(output_coordinates_list_tuple):
                if idx_inside_coord == 0:
                    duplicate_coordinates_idx_list = []
                else:
                    # if coordinates are same that previous index of coordinates is save in
                    # duplicate_coordinates_idx_list (we delete this coordinates after the loop)
                    if previous_coordinates == inside_coordinates:
                        duplicate_coordinates_idx_list.append(idx_inside_coord)
                previous_coordinates = inside_coordinates

            # delete duplicate
            if duplicate_coordinates_idx_list:
                for idx in reversed(duplicate_coordinates_idx_list):
                    del output_coordinates_list_tuple[idx]

            # retype to tuple if output_coordinates_list_tuple is originaly a tuple
            if retype_to_tuple is True:
                output_coordinates_list_tuple = tuple(output_coordinates_list_tuple)

        # FORMAT coordinates storage type
        # reformat coordinates storage type (list or tuple)
        if format_to_type:
            output_coordinates_list_tuple = format_to_type(output_coordinates_list_tuple)
    else:
        if format_to_type == list:
            output_coordinates_list_tuple = []
        else:
            output_coordinates_list_tuple = ()

    return output_coordinates_list_tuple


def coordinates_to_2d_coordinates(coordinates_list):
    """
    Convert a coordinates list with x dimension to 2d dimension list

    :param coordinates_list: list of coordinates with 2 or more dimension
    :return: coordinates list with only 2 dimensions.
    """

    if coordinates_list:
        if isinstance(coordinates_list[0], (int, float)):
            new_coordinates = [coordinates_list[0], coordinates_list[1]]
        elif isinstance(coordinates_list[0], (tuple, list)):
            new_coordinates = [None] * len(coordinates_list)
            for i_coord, under_coordinates in enumerate(coordinates_list):
                new_coordinates[i_coord] = coordinates_to_2d_coordinates(under_coordinates)
        else:
            raise Exception('error your geometry in input is not correct')
    else:
        new_coordinates = []

    return new_coordinates
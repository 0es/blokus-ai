import numpy as np

def flip180(arr):
    new_arr = arr.reshape(arr.size)
    new_arr = new_arr[::-1]
    new_arr = new_arr.reshape(arr.shape)
    return new_arr


def flip90_left(arr):
    new_arr = np.transpose(arr)
    new_arr = new_arr[::-1]
    return new_arr


def flip90_right(arr):
    new_arr = arr.reshape(arr.size)
    new_arr = new_arr[::-1]
    new_arr = new_arr.reshape(arr.shape)
    new_arr = np.transpose(new_arr)[::-1]
    return new_arr

def remove_duplicates_2d_array(arrays_list):
    unique_arrays = []
    seen = set()

    for array in arrays_list:
        array_tuple = tuple(map(tuple, array))
        if array_tuple not in seen:
            seen.add(array_tuple)
            unique_arrays.append(array)

    return unique_arrays

def piece_states_initializer(piece_list_init):
    result = {}

    for piece in piece_list_init:
        piece_value = piece['value']
        piece_value_t = piece['value'].transpose()
        piece_states_value = [
            piece_value, flip90_right(piece_value), flip180(piece_value), flip90_left(piece_value),
            piece_value_t, flip90_right(piece_value_t), flip180(piece_value_t), flip90_left(piece_value_t)
        ]
        piece_states_value_set = remove_duplicates_2d_array(piece_states_value)

        result[piece['id']] = []

        for state in piece_states_value_set:
            result[piece['id']].append({"id": piece['id'], "size": piece['size'], "value": state})

    return result


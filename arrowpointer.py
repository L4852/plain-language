def generate_arrow_string(initial_offset: str, arrow_index: int, repeat=0):
    string = initial_offset
    string += (' ' * (arrow_index - 1))
    string += '^' * (repeat + 1) + '\n'
    return string

from math import floor, ceil

from quicktions import Fraction


def _find_nearest_quantized_value(quantized_values, values):
    output = []
    for value in values:
        nearest_quantized = min(enumerate(quantized_values), key=lambda x: abs(x[1] - value))[1]
        delta = nearest_quantized - value
        output.append((nearest_quantized, delta))
    return output


def _find_quantized_locations(positions, grid_size):
    def get_quantized(val, key):
        factor = 1 / grid_size

        if key == "min":
            output = ceil(val * factor) / factor
        elif key == "max":
            output = floor(val * factor) / factor
        else:
            raise ValueError()
        return output

    min_location = Fraction(get_quantized(min(positions), "min"))
    output = [min_location]
    max_location = Fraction(get_quantized(max(positions), "max"))

    while output[-1] < max_location:
        output.append(output[-1] + Fraction(grid_size))

    return output


def get_quantized_positions(positions, grid_size):
    def _get_quantized_locations():
        return _find_quantized_locations(positions, grid_size)

    quantized_positions = [f[0] for f in _find_nearest_quantized_value(_get_quantized_locations(), positions)]

    return quantized_positions


def get_quantized_values(vals, grid_size):
    # print("vals", vals)
    def _get_positions():
        positions = [0]
        for val in vals:
            positions.append(positions[-1] + val)
        return positions

    positions = _get_positions()
    quantized_positions = get_quantized_positions(positions, grid_size)
    quantized_vals = []
    for index, val in enumerate(vals):
        quantized_val = Fraction(quantized_positions[index + 1] - quantized_positions[index]).limit_denominator(1000)
        quantized_vals.append(quantized_val)

    return quantized_vals


def find_best_quantized_values(values, units, check_sum=True):
    if check_sum:
        new_units = []
        for unit in units:
            if sum(values) % unit == 0:
                new_units.append(unit)
        if not new_units:
            raise AttributeError('all duration_units failed check_sum')
    else:
        new_units = units
    output = values
    old_delta = None
    for unit in new_units:
        quantized_values = get_quantized_values(values, unit)
        new_delta = sum([abs(quantized - original) for quantized, original in zip(quantized_values, values)])
        if old_delta is None or new_delta < old_delta:
            old_delta = new_delta
            output = quantized_values
    return output

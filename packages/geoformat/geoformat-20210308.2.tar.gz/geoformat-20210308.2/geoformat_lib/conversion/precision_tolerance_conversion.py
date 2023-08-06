import decimal


def deduce_rounding_value_from_float(float_value):

    d = decimal.Decimal(str(float_value))

    return abs(d.as_tuple().exponent)


def deduce_precision_from_round(rounding_value):

    precision_value = (1 / 10 ** rounding_value)

    return precision_value

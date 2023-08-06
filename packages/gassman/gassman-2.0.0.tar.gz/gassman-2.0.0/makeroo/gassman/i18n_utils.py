import decimal


def parse_decimal (value, as_decimal=False):
    """
    Normalize a string containing a number.
    String reprehesentation is preferred because no operation
    is performed python side. All operation are performed dbrms side
    after NUMERIC conversion, to preserve decimals.
    Furthermore returned value must be JSON serializable,
    and Decimal it is not.

    :param value: A string containing number in unspecified / undefined locale
    :param as_decimal: Return string (False) or Decimal (True)
    :return: A string containing a number in in str(float()) syntax
             (ie. with . as decimal separator and no grouping)
             if as_decimal is False, otherwise a Decimal.
    """
    if isinstance(value, decimal.Decimal):
        return value if as_decimal else str(value)
    if type(value) in (float, int):
        return decimal.Decimal(value) if as_decimal else str(value)
    if not value:
        return None
    try:
        norm_text = value.replace(',', '.')
        d = decimal.Decimal(norm_text)
        return d if as_decimal else str(d)
    except (decimal.InvalidOperation, AttributeError):
        raise ValueError

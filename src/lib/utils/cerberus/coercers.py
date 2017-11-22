
import pendulum


def datetime_coercer(date_string):
    """Pendulum Parser for date and datetime strings"""
    dt = pendulum.parse(date_string)
    return dt


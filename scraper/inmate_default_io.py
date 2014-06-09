"""
inmate_default_io.py

This file contains our way of storing inmate data.
In version 1 of the application this was done using
a ORM. In version 2 we are just storing data in a
csv file.

"""

from inmate_data import InmateData

class InmateCsvIo(InmateData):
    pass

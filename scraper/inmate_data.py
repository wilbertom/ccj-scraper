"""
inmate_storage.py

The InmateStorage is a Java interface styled class.
Subclass it and the scraper will be able to use it to
save the data it collects. inmate.py takes an instance
of an InmateData and bridges it to the InmateDetails
class.

record format document:
https://docs.google.com/document/d/1mgC8HLHHP4qvHR-jN6GQX04abiZkJp2mNffEicCIjuw/edit

"""


class InmateData(object):
    """
    A class meant to be sub classed and used
    with the scraper or some other data
    source.

    The properties of this class mirror those of the columns
    in the record format document linked above.

    With this common interface the scraper(or whatever other
    data source) will know to call these. Your subclass can
    transform the data received from a data source. You can
    for example save it in a database with different models,
    save it to a file, keep some columns, parse others...

    This class will receive data with almost no alteration
    of that located in the Sheriff's website. The only
    changes will be some removing of whitespace.

    For an example of how to use this class see InmateDetails or
    InmateCsvIo.

    The inmateDetails class is a special implementation of this
    class. It stores and parses the data captured from the
    Sheriff's website. On the other hand InmateCsvIo takes
    data from InmateDetails and stores it in a csv.

    Here is the data flow:

    1. Scraper ask for a web page.
    2. Scraper passes the web page to an instance of InmateDetails.
    3. Scraper uses the parsed data from InmateDetails and passes it
    to InmateCsvIo.
    4. InmateCsvIo stores data.

    Of course the InmateCsvIo can replaced with something like
    InmateSqlIo, or InmateJsonSave, that's the point of having
    it be modular ;).

    """
    def __init__(self):
        self._booking_id = None
        self._booking_date = None
        self._inmate_hash = None
        self._gender = None
        self._race = None
        self._height = None
        self._weight = None
        self._age_at_booking = None
        self._housing_location = None
        self._charges = None
        self._bail_amount = None
        self._court_date = None
        self._court_location = None

    @property
    def booking_id(self):
        return self._booking_id

    @booking_id.setter
    def booking_id(self, bi):
        self._booking_id = bi

    @property
    def booking_date(self):
        return self._booking_date

    @booking_date.setter
    def booking_date(self, bd):
        self._booking_date = bd

    @property
    def inmate_hash(self):
        return self._inmate_hash

    @inmate_hash.setter
    def inmate_hash(self, ih):
        self._inmate_hash = ih

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, g):
        self._gender = g

    @property
    def race(self):
        return self._race

    @race.setter
    def race(self, r):
        self._race = r

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, h):
        self._height = h

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, w):
        self._weight = w

    @property
    def age_at_booking(self):
        return self._age_at_booking

    @age_at_booking.setter
    def age_at_booking(self, age):
        self._age_at_booking = age

    @property
    def housing_location(self):
        return self._housing_location

    @housing_location.setter
    def housing_location(self, housing):
        self._housing_location = housing

    @property
    def charges(self):
        return self._charges

    @charges.setter
    def charges(self, c):
        self._charges = c

    @property
    def bail_amount(self):
        return self._bail_amount

    @bail_amount.setter
    def bail_amount(self, amount):
        self._bail_amount = amount

    @property
    def court_date(self):
        return self._court_date

    @court_date.setter
    def court_date(self, d):
        self._court_date = d

    @property
    def court_location(self):
        return self._court_location

    @court_location.setter
    def court_location(self, location):
        self._housing_location = location

"""
inmate_details.py

The InmateDetails class is responsible for extracting and cleaning
data given an html page. From the html it will parse the
age at booking, next court date ect ect. From the fields it also
can create a hash for the Inmate.

This is a standalone class, it only has PyQuery as a requirement
it's standalone in the sense that you can do:

i = InmateDetails(request.get(inmate_page_url))

and then do whatever with the data. This class will not try to save,
and the only parsing of the raw data it does is remove leading
whitespace.

"""
from datetime import datetime
from pyquery import PyQuery
import hashlib
from inmate_data import InmateData


class InmateDetails(InmateData):
    """
    Handles the processing of the Inmate Detail information page on the
    Cook County Jail website.
    Presents a consistent named interface to the information

    Strips spurious whitespace from text content before returning them

    Dates are returned as datetime objects
    """

    def __init__(self, html):
        super(InmateDetails, self).__init__()

        inmate_doc = PyQuery(html)
        self.__columns = inmate_doc('table tr:nth-child(2n) td')

    def _column_content(self, columns_index):
        return self.__columns[columns_index].text_content().strip()

    def __convert_date(self, column_index):
        result = self.__convert_datetime(column_index)
        return result if result is None else result.date()

    def __convert_datetime(self, column_index):
        try:
            result = datetime.strptime(self._column_content(column_index),
                                       '%m/%d/%Y')
        except ValueError:
            result = None
        return result

    def _birth_date(self):
        return self.__convert_datetime(2)

    def _name(self):
        return self._column_content(1)

    def _hash_id(self):
        id_string = "%s%s%s%s" % (
            self._name().replace(" ", ""),
            self._birth_date().strftime('%m%d%Y'),
            self.race()[0],
            self.gender(),
        )
        byte_string = id_string.encode('utf-8')
        return hashlib.sha256(byte_string).hexdigest()

    def _court_house_location(self):
        return self._column_content(13)

    def _jail_id(self):
        return self._column_content(0)

    def _next_court_date(self):
        return self.__convert_datetime(12)

    def booking_id(self):
        return self._jail_id()

    def booking_date(self):
        return self.__convert_date(7)

    def inmate_hash(self):
        return self._hash_id()

    def gender(self):
        return self._column_content(4)

    def race(self):
        return self._column_content(3)

    def height(self):
        return self._column_content(5)

    def weight(self):
        return self._column_content(6)

    def age_at_booking(self):
        """
        Calculates the inmates age at the time of booking,
        code taken from http://is.gd/ep7Thb
        """
        birth_date, booking_date = self._birth_date(), self.booking_date()
        if (birth_date.month <= booking_date.month and
                birth_date.day <= booking_date.day):
            return booking_date.year - birth_date.year
        return booking_date.year - birth_date.year - 1

    def housing_location(self):
        return self._column_content(8)

    def charges(self):
        return self._column_content(11)

    def bail_amount(self):
        return self._column_content(10)

    def court_date(self):
        return self._next_court_date()

    def court_location(self):
        return self._court_house_location()
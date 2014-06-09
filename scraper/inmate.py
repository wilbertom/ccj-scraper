
from datetime import time

from utils import convert_to_int

_MIDNIGHT = time()
_NUMBER_DAYS_AGO = 5


class Inmate:
    """
    Inmate handling code lifted whole sale from inmate_utils file.
    """

    def __init__(self, inmate_id, inmate_details, monitor):
        self._inmate_id = inmate_id
        self._inmate_details = inmate_details
        self._monitor = monitor
        self._inmate = None

    @staticmethod
    def active_inmates():
        raise NotImplementedError('needs to be implemented with the new format')

    def _clear_discharged(self):
        """
        Because the Cook County Jail website has issues, we can have misclassified inmates as discharged. This
        function clears the discharge fields, so the inmate is no longer classified as being discharged.
        @return True if resurrecting inmate
        """

        # resurrected = self._inmate.discharge_date_earliest is not None
        # if resurrected:
        #     self._inmate.discharge_date_earliest = None
        #     self._inmate.discharge_date_latest = None
        #     self._inmate.in_jail = self._inmate.housing_history.latest().housing_location.in_jail
        # return resurrected
        raise NotImplementedError('needs to be implemented with the new format')

    def _debug(self, msg):
        self._monitor.debug('Inmate: %s' % msg)

    @staticmethod
    def discharge(inmate_id, monitor):
        raise NotImplementedError('discharge needs to be implemented with the new format')

    def _inmate_record_get_or_create(self):
        """
        Gets or creates inmate record based on jail_id and stores the url used to fetch the inmate info
        """
        raise NotImplementedError('_inmate_record_get_or_create needs to be implemented with the new format')

    @staticmethod
    def known_inmates_for_date(booking_date):
        """
        Returns all inmates for a given date.
        @param booking_date: booking date to search for
        @rtype : list of inmates booked on specified day
        """
        raise NotImplementedError('needs to be implemented with the new format')

    @staticmethod
    def recently_discharged_inmates():
        raise NotImplementedError('needs to be implemented with the new format')

    def save(self):
        """
        Fetches inmates detail page and creates or updates inmates record based on it,
        otherwise returns as inmate's details were not found
        """
        updated_msg = "Updated"
        try:
            self._inmate, created = self._inmate_record_get_or_create()

            if self._clear_discharged():
                updated_msg = "Resurrected"

            self._store_person_id()
            self._store_booking_date()
            self._store_physical_characteristics()
            self._store_housing_location()
            self._store_bail_info()
            self._store_charges()
            self._store_next_court_info()

            try:
                self._inmate.save()
                self._debug("%s inmate %s" % ("Created" if created else updated_msg, self._inmate_id))
            except Exception as e:
                self._debug("Could not save inmate '%s'\nException is %s" % (self._inmate_id, str(e)))

        except Exception, e:
            self._debug("Unknown exception for inmate '%s'\nException is %s" % (self._inmate_id, str(e)))

    def _store_bail_info(self):
        # Bond: If the value is an integer, it's a dollar
        # amount. Otherwise, it's a status, e.g. "* NO BOND *".
        self._inmate.bail_amount = convert_to_int(self._inmate_details.bail_amount().replace(',', ''), None)
        if self._inmate.bail_amount is None:
            self._inmate.bail_status = self._inmate_details.bail_amount().replace('*', '').strip()
        else:
            self._inmate.bail_status = None

    def _store_booking_date(self):
        self._inmate.booking_date = self._inmate_details.booking_date()

    def _store_charges(self):
        self._inmate.charge = self._inmate_details.charges()

    def _store_housing_location(self):
        self._inmate.housing_location = self._inmate_details.housing_location()

    def _store_next_court_info(self):
        self._inmate.court_info = self._inmate_details.next_court_date()

    def _store_person_id(self):
        self._inmate.person_id = self._inmate_details.hash_id()

    def _store_physical_characteristics(self):
        self._inmate.gender = self._inmate_details.gender()
        self._inmate.race = self._inmate_details.race()
        self._inmate.height = self._inmate_details.height()
        self._inmate.weight = self._inmate_details.weight()
        self._inmate.age_at_booking = self._inmate_details.age_at_booking()

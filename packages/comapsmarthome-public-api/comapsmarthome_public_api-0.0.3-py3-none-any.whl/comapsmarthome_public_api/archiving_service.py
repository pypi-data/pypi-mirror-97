#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from dateutil.parser import isoparse
from comapsmarthome_public_api.comap_smart_home import ComapSmartHome, _BASE_URL

_ARCHIVING_SERVICE_URL = _BASE_URL + "archiving"


class ArchivingService(ComapSmartHome):
    base_url = _ARCHIVING_SERVICE_URL

    def get_transmissions(self, serial_number, dt_from, dt_to):
        """Get a list of all the data transmitted by the specified product between two dates"""
        global_transmissions = []
        dt = datetime.timedelta(seconds=1)
        dt_from_parsed = isoparse(dt_from)
        params = {"serial_number": serial_number, "from": dt_from, "to": dt_to}
        url = "{}/transmissions".format(self.base_url)
        transmissions = self.get_request(url=url, headers=self.request_header, params=params)
        global_transmissions += transmissions
        trans_beg = isoparse(transmissions[-1]["reception_time"]) if len(transmissions) > 0 else dt_from_parsed
        while len(transmissions) > 0 and (trans_beg - dt_from_parsed).total_seconds() > 24*60*60:
            params["to"] = (trans_beg - dt).isoformat()
            transmissions = self.get_request(url=url, headers=self.request_header, params=params)
            global_transmissions += transmissions
            trans_beg = isoparse(transmissions[-1]["reception_time"]) if len(transmissions) > 0 else dt_from_parsed

        return global_transmissions


if __name__ == '__main__':
    from comapsmarthome_public_api.client_auth import ClientAuth

    dt_from = '2020-10-20T09:30+02:00'
    dt_to = '2020-10-20T11:00+02:00'
    serial_number = 'SERIAL_NUMBER'

    auth = ClientAuth()
    archiving = ArchivingService(auth)

    transmissions = archiving.get_transmissions(serial_number=serial_number, dt_from=dt_from, dt_to=dt_to)

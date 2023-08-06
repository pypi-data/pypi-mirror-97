from unittest import TestCase

from openmodule.models.vehicle import Vehicle


class VehicleTestCase(TestCase):
    def test_vehicle_str(self):
        # just checks that the relevant info is
        vehicle = Vehicle(id=1613386532124866889,
                          qr={"id": "someverylongqrcodeitisreallylongohyeah", "type": "qr"},
                          lpr={"id": "test", "type": "lpr", "country": {"code": "D"}})

        vehicle_str = str(vehicle)

        self.assertIn("id:4866889", vehicle_str)  # only the last 7 digits are printed because they are random enough
        self.assertIn("somevery", vehicle_str)
        self.assertIn("...", vehicle_str)  # long medium id's are truncated
        self.assertIn("test", vehicle_str)

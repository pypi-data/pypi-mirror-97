import random
from datetime import datetime
from typing import Optional, Callable

from openmodule.models.base import Direction, Gateway
from openmodule.models.presence import PresenceBaseMessage, PresenceEnterMessage, PresenceLeaveMessage, \
    PresenceForwardMessage, PresenceBackwardMessage, PresenceMedia, PresenceChangeMessage
from openmodule.models.vehicle import LPRMedium, LPRCountry, Medium, Vehicle


class VehicleBuilder:
    vehicle_id: int
    medium: PresenceMedia

    def __init__(self):
        self.vehicle_id = random.randint(0, 1000000000000000)
        self.medium = PresenceMedia()

    def vehicle(self) -> Vehicle:
        return Vehicle(
            id=self.vehicle_id,
            lpr=self.medium.lpr,
            qr=self.medium.qr,
            nfc=self.medium.nfc,
            pin=self.medium.pin,
        )

    def id(self, id: int) -> 'VehicleBuilder':
        self.vehicle_id = id
        return self

    def lpr(self, country, plate=None) -> 'VehicleBuilder':
        if country is None:
            self.medium.lpr = None
        else:
            self.medium.lpr = LPRMedium(
                id=plate,
                country=LPRCountry(code=country)
            )
        return self

    def nfc(self, id) -> 'VehicleBuilder':
        if id is None:
            self.medium.nfc = id
        else:
            self.medium.nfc = Medium(id=id, type="nfc")
        return self

    def qr(self, id) -> 'VehicleBuilder':
        if id is None:
            self.medium.qr = id
        else:
            self.medium.qr = Medium(id=id, type="qr")
        return self

    def pin(self, id) -> 'VehicleBuilder':
        if id is None:
            self.medium.pin = id
        else:
            self.medium.pin = Medium(id=id, type="pin")
        return self


class PresenceSimulator:
    current_present: Optional[VehicleBuilder] = None

    def __init__(self, gate: str, direction: Direction, emit: Callable[[PresenceBaseMessage], None]):
        self.gateway = Gateway(gate=gate, direction=direction)
        self.emit = emit

    def vehicle(self):
        return VehicleBuilder()

    def _common_kwargs(self, vehicle):
        timestamp = datetime.now().timestamp()
        return {
            "vehicle_id": vehicle.vehicle_id,
            "unsure": False,
            "present-area-name": f"{self.gateway.gate}-present",
            "last_update": timestamp,
            "name": "presence-sim",
            "source": self.gateway.gate,
            "gateway": self.gateway,
            "medium": vehicle.medium
        }

    def enter(self, vehicle: VehicleBuilder):
        if self.current_present:
            self.leave()
        self.current_present = vehicle
        self.emit(PresenceEnterMessage(**self._common_kwargs(vehicle)))

    def leave(self):
        self.emit(PresenceLeaveMessage(**self._common_kwargs(self.current_present)))
        temp = self.current_present
        self.current_present = None
        return temp

    def forward(self, vehicle: Optional[VehicleBuilder] = None):
        assert vehicle or self.current_present, "a vehicle must be present, or you have to pass a vehicle"
        if not vehicle:
            vehicle = self.leave()
        self.emit(PresenceForwardMessage(
            **self._common_kwargs(vehicle),
            **{"leave-time": datetime.now().timestamp()}
        ))

    def backward(self, vehicle: Optional[VehicleBuilder] = None):
        assert vehicle or self.current_present, "a vehicle must be present, or you have to pass a vehicle"
        if not vehicle:
            vehicle = self.leave()
        self.emit(PresenceBackwardMessage(
            **self._common_kwargs(vehicle),
            **{"leave-time": datetime.now().timestamp()}
        ))

    def change(self, vehicle: VehicleBuilder):
        assert self.current_present, "a vehicle must be present"
        assert self.current_present.id == vehicle.id, "vehicle id must stay the same"
        self.current_present = vehicle
        self.emit(PresenceChangeMessage(
            **self._common_kwargs(vehicle),
            **{"leave-time": datetime.now().timestamp()}
        ))

    def change_vehicle_and_id(self, vehicle: VehicleBuilder):
        assert self.current_present, "a vehicle must be present"
        assert self.current_present.id != vehicle.id, "vehicle id must change"
        self.current_present = vehicle
        self.emit(PresenceChangeMessage(
            **self._common_kwargs(vehicle),
            **{"leave-time": datetime.now().timestamp(), "change_vehicle_id": True}
        ))

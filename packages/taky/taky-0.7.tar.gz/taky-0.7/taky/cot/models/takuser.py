from datetime import datetime as dt
from datetime import timedelta
from dataclasses import dataclass

from lxml import etree

from .errors import UnmarshalError
from .event import Event
from .detail import Detail
from .teams import Teams
from .point import Point


@dataclass
class TAKDevice:
    os: str = None  # pylint: disable=invalid-name
    version: str = None
    device: str = None
    platform: str = None

    def __repr__(self):
        return "<TAKDevice %s (%s) on %s>" % (self.platform, self.version, self.device)

    @staticmethod
    def from_elm(elm):
        if elm.tag != "takv":
            raise UnmarshalError("Unable to load TAKDevice from %s" % elm.tag)

        return TAKDevice(
            os=elm.get("os"),
            device=elm.get("device"),
            version=elm.get("version"),
            platform=elm.get("platform"),
        )

    @property
    def as_element(self):
        ret = etree.Element("takv")
        ret.set("os", self.os or "")
        ret.set("device", self.device or "")
        ret.set("version", self.version or "")
        ret.set("platform", self.platform or "")

        return ret

    @property
    def as_xml(self):
        return etree.tostring(self.as_element)


# TODO: Extend from Detail
@dataclass
class TAKUser:
    def __init__(self):
        self.uid = None
        self.callsign = None
        self.phone = None
        self.marker = None
        self.group = None
        self.role = None

        self.point = Point()
        self.course = None
        self.speed = None

        self.battery = None

        self.device = None

        self.last_seen = None
        self.stale = None

    def __repr__(self):
        return f"<TAKUser uid={self.uid}, callsign={self.callsign}, group={self.group}>"

    def update_from_evt(self, evt):
        # Sanity check inputs
        if evt.detail is None:
            return False
        if evt.detail.elm.find("takv") is None:
            return False

        ret = False
        # Is this our first run?
        if self.uid is None:
            self.uid = evt.uid
            ret = True
        elif self.uid != evt.uid:
            return False

        self.marker = evt.etype
        self.point = evt.point
        self.last_seen = evt.start
        self.stale = evt.stale

        for elm in evt.detail.elm.iterchildren():
            if elm.tag == "takv":
                self.device = TAKDevice.from_elm(elm)
            elif elm.tag == "contact":
                self.callsign = elm.get("callsign")
                self.phone = elm.get("phone")
            elif elm.tag == "__group":
                try:
                    self.group = Teams(elm.get("name"))
                except ValueError:
                    # TODO: How to handle unknown group? Defaults to "Cyan"
                    self.group = Teams.UNKNOWN
                self.role = elm.get("role")
            elif elm.tag == "status":
                self.battery = elm.get("battery")
            elif elm.tag == "track":
                self.course = float(elm.get("course"))
                self.speed = float(elm.get("speed"))
            elif elm.tag == "uid":
                pass
            elif elm.tag == "precisionlocation":
                pass
            else:
                # self.lgr.warn("Unhandled TAKClient detail: %s", elm.tag)
                pass

        return ret

    @property
    def as_element(self):
        if self.last_seen is None:
            # TODO: What should we do if we've never been seen?
            now = dt.utcnow()
            stale = now + timedelta(seconds=20)
        else:
            now = self.last_seen
            stale = self.stale

        evt = Event(
            uid=self.uid,
            etype=self.marker or "a-f",
            how="m-g",
            time=now,
            start=now,
            stale=stale,
        )
        evt.point = self.point
        evt.detail = Detail(evt, etree.Element("detail"))
        evt.detail.elm = etree.Element("detail")
        if self.device:
            takv = etree.Element(
                "takv",
                attrib={
                    "os": self.device.os or "30",
                    "version": self.device.version or "unknown",
                    "device": self.device.device or "unknown",
                    "platform": self.device.platform or "unknown",
                },
            )
            evt.detail.elm.append(takv)

            status = etree.Element(
                "status",
                attrib={
                    "battery": self.battery or "100",
                },
            )
            evt.detail.elm.append(status)

        uid = etree.Element("uid", attrib={"Droid": self.callsign or "JENNY"})
        evt.detail.elm.append(uid)

        contact = etree.Element(
            "contact",
            attrib={
                "callsign": self.callsign or "JENNY",
                "endpoint": "*:-1:stcp",
            },
        )
        if self.phone:
            contact.set("phone", self.phone)
        evt.detail.elm.append(contact)

        group = etree.Element(
            "__group",
            attrib={
                "role": self.role or "Team Member",
                "name": self.group.value,
            },
        )
        evt.detail.elm.append(group)

        track = etree.Element(
            "track",
            attrib={
                "course": "%.1f" % (self.course or 0.0),
                "speed": "%.1f" % (self.speed or 0.0),
            },
        )
        evt.detail.elm.append(track)

        precisloc = etree.Element(
            "precisionlocation",
            attrib={
                "altsrc": "GPS",
                "geopointsrc": "GPS",
            },
        )
        evt.detail.elm.append(precisloc)

        return evt.as_element

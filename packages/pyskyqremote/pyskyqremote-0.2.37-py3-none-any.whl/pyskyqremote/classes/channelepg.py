"""Structure of a standard EPG prorgramme."""

import json
from dataclasses import dataclass, field
from datetime import datetime

from .programme import Programme


@dataclass
class ChannelEPG:
    """SkyQ Channel EPG Class."""

    sid: str = field(
        init=True, repr=True, compare=False,
    )
    channelno: str = field(
        init=True, repr=True, compare=False,
    )
    channelname: str = field(
        init=True, repr=True, compare=False,
    )
    channelImageUrl: str = field(
        init=True, repr=True, compare=False,
    )
    programmes: set = field(
        init=True, repr=True, compare=False,
    )

    def as_json(self) -> str:
        """Return a JSON string representing this Channel."""
        return json.dumps(self, cls=_ChannelEPGJSONEncoder)


def ChannelEPGDecoder(obj):
    """Decode channel object from json."""
    channelepg = json.loads(obj, object_hook=_json_decoder_hook)
    if "__type__" in channelepg and channelepg["__type__"] == "__channelepg__":
        return ChannelEPG(
            programmes=channelepg["programmes"], **channelepg["attributes"]
        )
    return channelepg


def _json_decoder_hook(obj):
    """Decode JSON into appropriate types used in this library."""
    if "starttime" in obj:
        obj["starttime"] = datetime.strptime(obj["starttime"], "%Y-%m-%dT%H:%M:%SZ")
    if "endtime" in obj:
        obj["endtime"] = datetime.strptime(obj["endtime"], "%Y-%m-%dT%H:%M:%SZ")
    if "__type__" in obj and obj["__type__"] == "__programme__":
        obj = Programme(**obj["attributes"])
    return obj


class _ChannelEPGJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ChannelEPG):
            type_ = "__channelepg__"
            programmes = obj.programmes
            attributes = {}
            for k, v in vars(obj).items():
                if k not in {"programmes"}:
                    attributes.update({k: v})
            return {
                "__type__": type_,
                "attributes": attributes,
                "programmes": programmes,
            }

        if isinstance(obj, set):
            return list(obj)

        if isinstance(obj, Programme):
            attributes = {}
            for k, v in vars(obj).items():
                if isinstance(v, datetime):
                    v = v.strftime("%Y-%m-%dT%H:%M:%SZ")
                attributes.update({k: v})

            result = {
                "__type__": "__programme__",
                "attributes": attributes,
            }
            return result

        json.JSONEncoder.default(self, obj)  # pragma: no cover

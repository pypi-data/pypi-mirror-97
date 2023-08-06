from attr import attrs, attrib, validators, asdict


# IMPORTANT: Be careful when subclassing! Setting eq=False on a class whose base class has a non-default __hash__ method will not make attrs remove that __hash__ for you. The easiest way to reset __hash__ on a class is adding __hash__ = object.__hash__ in the class body.  # noqa
@attrs(eq=False, order=False, kw_only=True)
class BaseModel(object):
    def __eq__(self, target):
        if not isinstance(target, type(self)):
            return False
        hashed_self = self.__hash__()
        hashed_target = target.__hash__()
        if hashed_self is not None and hashed_target is not None:
            return hashed_self == hashed_target
        else:
            return False

    def __ne__(self, target):
        return not self.__eq__(target)

    def __lt__(self, target):
        return self.__hash__() < target.__hash__()

    def __le__(self, target):
        return self.__hash__() <= target.__hash__()

    def __gt__(self, target):
        return self.__hash__() > target.__hash__()

    def __ge__(self, target):
        return self.__hash__() >= target.__hash__()

    def __hash__(self):
        hashed_value = hash(self.id)
        return hashed_value

    def _ignore_base_attr(self, _attr, _val):
        return (
            False
            if _attr.name == "raw_data" or (_attr.name == "id" and not _val)
            else True
        )

    def to_dict(self):
        return asdict(self, filter=self._ignore_base_attr)

    id = attrib(factory=str)
    raw_data = attrib(factory=dict)


@attrs(eq=False)
class ErrorModel(BaseModel):
    __hash__ = BaseModel.__hash__

    code = attrib(default="0")
    message = attrib(default="UNEXPECTED ERROR.")


@attrs(eq=False)
class Credential(BaseModel):
    """
    Instantiate Credential model with dynamic attributes
    depending on various keys of the credential object.
    Args:
        credential (dict): The credential object.
    Example:
        cred = Credential(
            credential={"access_key_id": "abc", "secret_access_key": "*****"}
        )
        cred.access_key_id
        cred.secret_access_key
    """

    __hash__ = BaseModel.__hash__

    credential = attrib()

    @credential.validator
    def is_valid_credential(self, attribute, value):
        # Set credential key, value as model attribute dynamically.
        if isinstance(value, dict):
            for k, v in value.items():
                setattr(self, k, v)
        else:
            raise TypeError(f"The credential must be a dictionary, not '{type(value)}'")


@attrs(eq=False)
class Location(BaseModel):
    __hash__ = BaseModel.__hash__

    lat = attrib(converter=float)
    lon = attrib(converter=float)


@attrs(eq=False)
class Temperature(BaseModel):
    __hash__ = BaseModel.__hash__

    temp_avg = attrib(default=-999, converter=float)
    temp_min = attrib(default=-999, converter=float)
    temp_max = attrib(default=-999, converter=float)


@attrs(eq=False)
class Wind(BaseModel):
    __hash__ = BaseModel.__hash__

    speed = attrib(converter=float)
    degree = attrib(converter=int)


@attrs(eq=False)
class Station(Location):
    def __hash__(self):
        hashed_value = hash(self.name)
        return hashed_value

    name = attrib(converter=str)


@attrs(eq=False)
class WeatherPoint(BaseModel):
    def __hash__(self):
        hashed_value = hash(self.station)
        return hashed_value

    station = attrib(validator=[validators.instance_of(Station)])
    status = attrib(converter=str)
    description = attrib(converter=str)
    icon = attrib(converter=str)
    time = attrib(converter=int)
    temp = attrib(validator=[validators.instance_of(Temperature)])
    pressure = attrib(converter=float)
    humidity = attrib(converter=float)
    rain = attrib(converter=float)
    wind = attrib(validator=[validators.instance_of(Wind)])
    clouds = attrib(converter=int)
    snow = attrib(converter=float)

"""Neo4j native spatial types (Point)
"""
import warnings
from neo4j.spatial import CartesianPoint, WGS84Point

from pentaquark.exceptions import PentaQuarkValidationError
from pentaquark.properties import Property


class PointObject:
    # TODO: use a python gis package instead?

    LAT_LON_CRS = "WGS-84"

    def __init__(self, x, y, crs=LAT_LON_CRS):
        self.x = float(x)
        self.y = float(y)
        self.crs = crs

    def __eq__(self, other):
        if self is None or other is None:
            return self is other
        return self.crs == other.crs and self.x == other.x and self.y == other.y

    def __str__(self):
        return f"<PointObject crs={self.crs} x={self.x} y={self.y}>"

    def to_repr(self):
        return self.x, self.y

    @property
    def latitude(self):
        if self.crs != self.LAT_LON_CRS:
            raise ValueError(f"Can not extract latitude from a point with srid={self.crs}")
        return self.y

    @property
    def longitude(self):
        if self.crs != self.LAT_LON_CRS:
            raise ValueError(f"Can not extract longitude from a point with srid={self.crs}")
        return self.x


class PointProperty(Property):
    DEFAULT_CRS = "WGS-84"
    CARTESIAN_CRS = "Cartesian"
    graphql_type = "String"

    SRID_TO_CRS = {
        4326: "WGS-84"
    }

    def __init__(self, crs=DEFAULT_CRS, **kwargs):
        super().__init__(**kwargs)
        self.crs = crs

    def _validate(self, value):
        if value is None:
            return None
        if isinstance(value, PointObject):
            if value.crs == self.crs:
                return value
            raise PentaQuarkValidationError(f"CRS mismatch '{value.crs} != {self.crs}' ")
        raise PentaQuarkValidationError(f"Invalid point: expected PointObject, found '{value.__class__.__name__}' ")

    def get_cypher_type(self):
        if self.crs == self.DEFAULT_CRS:
            return WGS84Point
        return CartesianPoint

    def to_cypher(self, value: PointObject):
        if value is None:
            return None
        p = self.get_cypher_type()(value.to_repr())
        return p

    def from_cypher(self, value):
        if value is None:
            return None
        crs = self.SRID_TO_CRS.get(value.srid, self.CARTESIAN_CRS)
        if crs != self.crs:
            warnings.warn("CRS differs", RuntimeWarning)
        return PointObject(x=value.x, y=value.y, crs=crs)

    def to_graphql(self, value):
        return f"{value.x},{value.y}"

from abc import ABC, abstractmethod
from os import PathLike
from pathlib import Path
from typing import Union

from geopandas import GeoDataFrame
import numpy
from pyproj import CRS

from .utilities import get_logger

LOGGER = get_logger('base')


class SeabedDescriptions(ABC):
    longitude_field = 'Longitude'
    latitude_field = 'Latitude'
    description_field = 'Description'

    def __init__(
        self,
        bounds: (float, float, float, float) = None,
        surveys: [str] = None,
        crs: CRS = None,
    ):
        self.bounds = bounds
        self.surveys = surveys
        self.crs = crs

    @property
    def bounds(self) -> (float, float, float, float):
        return self.__bounds

    @bounds.setter
    def bounds(self, bounds: (float, float, float, float)):
        if isinstance(bounds, numpy.ndarray):
            if len(bounds.shape) > 1:
                bounds = bounds.ravel()
        else:
            bounds = numpy.asarray(bounds)
        self.__bounds = bounds

    @property
    def crs(self) -> CRS:
        return self.__crs

    @crs.setter
    def crs(self, crs: Union[CRS, str]):
        self.__crs = CRS.from_user_input(crs) if crs is not None else None

    @classmethod
    @abstractmethod
    def all_surveys(cls) -> [str]:
        raise NotImplementedError

    @property
    def surveys(self) -> [str]:
        return self.__surveys

    @surveys.setter
    def surveys(self, surveys: [str]):
        self.__surveys = surveys if surveys is not None else self.__class__.all_surveys()

    def __getitem__(self, survey: str) -> GeoDataFrame:
        raise NotImplementedError

    @property
    @abstractmethod
    def data(self) -> GeoDataFrame:
        raise NotImplementedError

    @property
    @abstractmethod
    def descriptions(self) -> [str]:
        raise NotImplementedError

    def __iter__(self) -> GeoDataFrame:
        for survey in self.surveys:
            yield self[survey]

    def write(self, filename: PathLike, **kwargs):
        drivers = {
            '.csv': 'CSV',
            '.gpkg': 'GPKG',
            '.json': 'GeoJSON',
            '.shp': 'Esri Shapefile',
            '.gdb': 'OpenFileGDB',
            '.gml': 'GML',
            '.xml': 'GML',
        }

        if not isinstance(filename, Path):
            filename = Path(filename)

        kwargs['driver'] = drivers[filename.suffix]

        self.data.to_file(str(filename), **kwargs)

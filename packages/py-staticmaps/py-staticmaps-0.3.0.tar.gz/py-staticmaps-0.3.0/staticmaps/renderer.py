# py-staticmaps
# Copyright (c) 2020 Florian Pigorsch; see /LICENSE for licensing information

from abc import ABC, abstractmethod
import typing

from .color import Color
from .transformer import Transformer


if typing.TYPE_CHECKING:
    # avoid circlic import
    from .area import Area  # pylint: disable=cyclic-import
    from .image_marker import ImageMarker  # pylint: disable=cyclic-import
    from .line import Line  # pylint: disable=cyclic-import
    from .marker import Marker  # pylint: disable=cyclic-import
    from .object import Object  # pylint: disable=cyclic-import


class Renderer(ABC):
    def __init__(self, transformer: Transformer) -> None:
        self._trans = transformer

    def transformer(self) -> Transformer:
        return self._trans

    @abstractmethod
    def render_objects(self, objects: typing.List["Object"]) -> None:
        pass

    @abstractmethod
    def render_background(self, color: typing.Optional[Color]) -> None:
        pass

    @abstractmethod
    def render_tiles(self, download: typing.Callable[[int, int, int], typing.Optional[bytes]]) -> None:
        pass

    def render_marker_object(self, marker: "Marker") -> None:
        pass

    def render_image_marker_object(self, marker: "ImageMarker") -> None:
        pass

    def render_line_object(self, line: "Line") -> None:
        pass

    def render_area_object(self, area: "Area") -> None:
        pass

    @abstractmethod
    def render_attribution(self, attribution: typing.Optional[str]) -> None:
        pass

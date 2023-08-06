# py-staticmaps
# Copyright (c) 2020 Florian Pigorsch; see /LICENSE for licensing information

import typing

import s2sphere  # type: ignore

from .cairo_renderer import CairoRenderer
from .color import Color, RED, TRANSPARENT
from .line import Line
from .svg_renderer import SvgRenderer


class Area(Line):
    def __init__(
        self, latlngs: typing.List[s2sphere.LatLng], fill_color: Color = RED, color: Color = TRANSPARENT, width: int = 0
    ) -> None:
        Line.__init__(self, latlngs, color, width)
        if latlngs is None or len(latlngs) < 3:
            raise ValueError("Trying to create area with less than 3 coordinates")

        self._fill_color = fill_color

    def fill_color(self) -> Color:
        return self._fill_color

    def render_svg(self, renderer: SvgRenderer) -> None:
        xys = [renderer.transformer().ll2pixel(latlng) for latlng in self.interpolate()]

        polygon = renderer.drawing().polygon(
            xys,
            fill=self.fill_color().hex_rgb(),
            opacity=self.fill_color().float_a(),
        )
        renderer.group().add(polygon)

        if self.width() > 0:
            polyline = renderer.drawing().polyline(
                xys,
                fill="none",
                stroke=self.color().hex_rgb(),
                stroke_width=self.width(),
                opacity=self.color().float_a(),
            )
            renderer.group().add(polyline)

    def render_cairo(self, renderer: CairoRenderer) -> None:
        xys = [renderer.transformer().ll2pixel(latlng) for latlng in self.interpolate()]

        renderer.context().set_source_rgba(*self.fill_color().float_rgba())
        renderer.context().new_path()
        for x, y in xys:
            renderer.context().line_to(x, y)
        renderer.context().fill()

        if self.width() > 0:
            renderer.context().set_source_rgba(*self.color().float_rgba())
            renderer.context().set_line_width(self.width())
            renderer.context().new_path()
            for x, y in xys:
                renderer.context().line_to(x, y)
            renderer.context().stroke()

from itertools import product
from typing import Union, List, Tuple, Iterator, Iterable

from matplotlib.axes import Axes
from matplotlib.axis import Axis

from compound_types.built_ins import FloatIterable
from mpl_format.compound_types import Color, FontSize, StringMapper
from mpl_format.enums.line_style import LINE_STYLE
from mpl_format.text.text_utils import wrap_text, map_text


class TicksFormatter(object):

    def __init__(self, axis: str, which: str, axes: Axes):
        """
        Create a new TicksFormatter.

        :param axis: One of {'x', 'y', 'both'}
        :param which: One of {'major', 'minor', 'both'}
        :param axes: Axes to operate on.
        """
        self._axis: str = axis
        self._which = which
        self._axes: Axes = axes

    def reset(self) -> 'TicksFormatter':
        """
        Set all parameters to defaults.
        """
        self._axes.tick_params(
            axis=self._axis,
            which=self._which,
            reset=True
        )
        return self

    @property
    def _is_minor(self) -> bool:
        return self._which == 'minor'

    # region values and labels

    def set_values(self, values: FloatIterable) -> 'TicksFormatter':
        """
        Set the values of the ticks.

        :param values: List of values where the ticks should be located.
        """
        x_axis = self._axes.xaxis
        y_axis = self._axes.yaxis
        if self._axis in ('x', 'both'):
            x_axis.set_ticks(ticks=values, minor=self._is_minor)
        if self._axis in ('y', 'both'):
            y_axis.set_ticks(ticks=values, minor=self._is_minor)
        return self

    def set_labels(self, labels: Iterable[str]) -> 'TicksFormatter':
        """
        Set the labels for the ticks.

        :param labels: List of labels to annotate each tick value.
        """
        x_axis = self._axes.xaxis
        y_axis = self._axes.yaxis
        if self._axis in ('x', 'both'):
            x_axis.set_ticklabels(ticklabels=labels, minor=self._is_minor)
        if self._axis in ('y', 'both'):
            y_axis.set_ticklabels(ticklabels=labels, minor=self._is_minor)
        return self

    def get_labels(self):

        raise NotImplementedError

    # endregion

    # region direction

    def set_direction(self, direction: str) -> 'TicksFormatter':
        """
        Puts ticks inside the axes, outside the axes, or both.

        :param direction: One of {'in', 'out', 'inout', 'in_out'}
        """
        direction = {
            'in': 'in',
            'out': 'out',
            'inout': 'inout',
            'in_out': 'inout'
        }[direction]
        self._axes.tick_params(axis=self._axis, which=self._which,
                               direction=direction)
        return self

    def set_direction_in(self) -> 'TicksFormatter':
        """
        Puts ticks inside the axes.
        """
        self.set_direction('in')
        return self

    def set_direction_out(self) -> 'TicksFormatter':
        """
        Puts ticks outside the axes.
        """
        self.set_direction('out')
        return self

    def set_direction_in_out(self) -> 'TicksFormatter':
        """
        Puts ticks inside and outside the axes.
        """
        self.set_direction('in_out')
        return self

    # endregion

    def set_length(self, length: float) -> 'TicksFormatter':
        """
        Set the tick length in points.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               length=length)
        return self

    def set_width(self, width: float) -> 'TicksFormatter':
        """
        Set the tick width in points.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               width=width)
        return self

    def set_padding(self, padding: float) -> 'TicksFormatter':
        """
        Set the distance in points between tick and label.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               pad=padding)
        return self

    def set_color(self, color: Color) -> 'TicksFormatter':
        """
        Set the tick color.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               color=color)
        return self

    def set_colors(self, color: Color) -> 'TicksFormatter':
        """
        Set tick color and the label color to the same value.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               colors=color)
        return self

    def set_z_order(self, z_order: float) -> 'TicksFormatter':
        """
        Set the tick and label z-order.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               zorder=z_order)
        return self

    # region show ticks

    def show_top(self, show: bool = True) -> 'TicksFormatter':
        """
        Whether to draw ticks at the top of the plot.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               top=show)
        return self

    def show_bottom(self, show: bool = True) -> 'TicksFormatter':
        """
        Whether to draw ticks at the bottom of the plot.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               bottom=show)
        return self

    def show_left(self, show: bool = True) -> 'TicksFormatter':
        """
        Whether to draw ticks at the left of the plot.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               left=show)
        return self

    def show_right(self, show: bool = True) -> 'TicksFormatter':
        """
        Whether to draw ticks at the right of the plot.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               right=show)
        return self

    # endregion

    # region labels

    def set_label_size(self, label_size: FontSize) -> 'TicksFormatter':
        """
        Set the tick label font size in points or as a string (e.g., 'large').
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               labelsize=label_size)
        return self

    def set_label_color(self, color: Color) -> 'TicksFormatter':
        """
        Set the tick label color.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               labelcolor=color)
        return self

    def set_label_rotation(self, rotation: float) -> 'TicksFormatter':
        """
        Set the tick label rotation.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               rotation=rotation)
        return self

    def _iter_axis_minor(self) -> Iterator[Tuple[Axis, bool]]:

        axes: List[Axis] = []
        axis: Axis
        if self._axis in ('x', 'both'):
            axes.append(self._axes.xaxis)
        if self._axis in ('y', 'both'):
            axes.append(self._axes.yaxis)
        minors: List[bool] = []
        if self._which in ('minor', 'both'):
            minors.append(True)
        if self._which in ('major', 'both'):
            minors.append(False)
        for axis, minor in product(axes, minors):
            yield axis, minor

    def wrap_label_text(self, max_width: int) -> 'TicksFormatter':
        """
        Wrap the text for each tick label with new lines if it exceeds
        a given width of characters.

        :param max_width: The maximum character width per line.
        """
        for axis, minor in self._iter_axis_minor():
            tick_labels = axis.get_ticklabels(minor=minor)
            if all(t.get_text() == '' for t in tick_labels):
                continue  # non categorical tick-labels e.g. line plot
            axis.set_ticklabels(
                ticklabels=[wrap_text(text, max_width)
                            for text in tick_labels],
                minor=minor
            )
        return self

    def map_label_text(self, mapping: StringMapper) -> 'TicksFormatter':
        """
        Map the tick label text using a dictionary or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        for axis, minor in self._iter_axis_minor():
            labels = [label.get_text()
                      for label in axis.get_ticklabels(minor=minor)]
            axis.set_ticklabels(map_text(labels, mapping))
        return self

    # region show labels

    def show_top_labels(self, show: bool = True) -> 'TicksFormatter':
        """
        Whether to draw tick labels at the top of the plot.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               labeltop=show)
        return self

    def show_bottom_labels(self, show: bool = True) -> 'TicksFormatter':
        """
        Whether to draw tick labels at the bottom of the plot.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               labelbottom=show)
        return self

    def show_left_labels(self, show: bool = True) -> 'TicksFormatter':
        """
        Whether to draw tick labels at the left of the plot.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               labelleft=show)
        return self

    def show_right_labels(self, show: bool = True) -> 'TicksFormatter':
        """
        Whether to draw tick labels at the right of the plot.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               labelright=show)
        return self

    # endregion

    # endregion

    # region grid

    def set_grid_color(self, color: Color) -> 'TicksFormatter':
        """
        Set the grid line color.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               grid_color=color)
        return self

    def set_grid_alpha(self, alpha: float) -> 'TicksFormatter':
        """
        Set the transparency of grid lines: 0 (transparent) to 1 (opaque).
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               grid_alpha=alpha)
        return self

    def set_grid_line_width(self, line_width: float) -> 'TicksFormatter':
        """
        Set the width of grid lines in points.
        """
        self._axes.tick_params(axis=self._axis, which=self._which,
                               grid_linewidth=line_width)
        return self

    def set_grid_line_style(self, line_style: Union[str, LINE_STYLE]):
        """
        Set the line style of the grid lines.
        """
        self._axes.tick_params(
            axis=self._axis, which=self._which,
            grid_linestyle=LINE_STYLE.get_line_style(line_style)
        )
        return self

    # endregion

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from seaborn import JointGrid, PairGrid
from typing import TypeVar, Tuple, Union, Dict, Callable, Iterable

Color = TypeVar(
    'Color',
    str,
    Tuple[float, float, float],
    Tuple[float, float, float, float]
)
ColorIterable = Iterable[Color]
FontSize = TypeVar('FontSize', str, float, int)
LegendLocation = TypeVar('LegendLocation', str, Tuple[float, float])
PlotObject = TypeVar('PlotObject', Axes, Figure, JointGrid, PairGrid)
StringMapper = Union[Dict[str, str], Callable[[str], str]]
ColorOrColorIterable = Union[Color, ColorIterable]
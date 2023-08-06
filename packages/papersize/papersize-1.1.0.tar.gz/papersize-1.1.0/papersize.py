# Copyright Louis Paternault 2014-2021
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Paper size related data and functions

In this module:

- the default unit (input and output) is point (``pt``);
- every numbers are returned as :class:`decimal.Decimal` objects.


Constants
---------

.. autodata:: UNITS
    :annotation:

.. autodata:: SIZES
    :annotation:

.. autodata:: PORTRAIT
    :annotation:

.. autodata:: LANDSCAPE
    :annotation:

Unit conversion
---------------

.. autofunction:: convert_length

Parsers
-------

.. autofunction:: parse_length

.. autofunction:: parse_couple

.. autofunction:: parse_papersize

Paper orientation
-----------------

.. autofunction:: is_portrait

.. autofunction:: is_landscape

.. autofunction:: is_square

.. autofunction:: rotate

Exceptions
----------

.. autoclass:: PapersizeException

.. autoclass:: CouldNotParse

.. autoclass:: UnknownOrientation

"""

from __future__ import unicode_literals
from decimal import Decimal
import re

__version__ = "1.1.0"
__AUTHOR__ = "Louis Paternault (spalax@gresille.org)"
__COPYRIGHT__ = "(C) 2014-2021 Louis Paternault. GNU GPL 3 or later."

SIZES = {
    # http://www.printernational.org/iso-paper-sizes.php
    "4a0": "1682mm x 2378mm",
    "2a0": "1189mm x 1682mm",
    "a0": "841mm x 1189mm",
    "a1": "594mm x 841mm",
    "a2": "420mm x 594mm",
    "a3": "297mm x 420mm",
    "a4": "210mm x 297mm",
    "a5": "148mm x 210mm",
    "a6": "105mm x 148mm",
    "a7": "74mm x 105mm",
    "a8": "52mm x 74mm",
    "a9": "37mm x 52mm",
    "a10": "26mm x 37mm",
    "b0": "1000mm x 1414mm",
    "b1": "707mm x 1000mm",
    "b2": "500mm x 707mm",
    "b3": "353mm x 500mm",
    "b4": "250mm x 352mm",
    "b5": "176mm x 250mm",
    "b6": "125mm x 176mm",
    "b7": "88mm x 125mm",
    "b8": "62mm x 88mm",
    "b9": "44mm x 62mm",
    "b10": "31mm x 44mm",
    "a2extra": "445mm x 619mm",
    "a3extra": "322mm x 445mm",
    "a3super": "305mm x 508mm",
    "supera3": "305mm x 487mm",
    "a4extra": "235mm x 322mm",
    "a4super": "229mm x 322mm",
    "supera4": "227mm x 356mm",
    "a4long": "210mm x 348mm",
    "a5extra": "173mm x 235mm",
    "sob5extra": "202mm x 276mm",
    # http://www.engineeringtoolbox.com/office-paper-sizes-d_213.html
    "letter": "8.5in x 11in",
    "legal": "8.5in x 14in",
    "executive": "7in x 10in",
    "tabloid": "11in x 17in",
    "statement": "5in x 8.5in",
    "halfletter": "5in x 8.5in",
    "folio": "8in x 13in",
    # http://hplipopensource.com/hplip-web/tech_docs/page_sizes.html
    "flsa": "8.5in x 13in",
    # http://www.coding-guidelines.com/numbers/ndb/units/area.txt
    "flse": "8.5in x 13in",
    # http://jexcelapi.sourceforge.net/resources/javadocs/2_6_10/docs/jxl/format/PaperSize.html
    "note": "8.5in x 11in",
    "11x17": "11in x 17in",
    "10x14": "10in x 14in",
    # https://en.wikipedia.org/w/index.php?title=Paper_size&oldid=814180250
    "c0": "917mm × 1297mm",
    "c1": "648mm × 917mm",
    "c2": "458mm × 648mm",
    "c3": "324mm × 458mm",
    "c4": "229mm × 324mm",
    "c5": "162mm × 229mm",
    "c6": "114mm × 162mm",
    "c7": "81mm × 114mm",
    "c8": "57mm × 81mm",
    "c9": "40mm × 57mm",
    "c10": "28mm × 40mm",
    "juniorlegal": "5in × 8in",
    "memo": "halfletter",
    "governmentletter": "8in × 10.5in",
    "governmentlegal": "8.5in × 13in",
    "ledger": "17in x 11in",
    "arch1": "9in x 12in",
    "arch2": "12in x 18in",
    "arch3": "18in x 24in",
    "arch4": "24in x 36in",
    "arch5": "30in x 42in",
    "arch6": "36in x 48in",
    "archa": "arch1",
    "archb": "arch2",
    "archc": "arch3",
    "archd": "arch4",
    "arche1": "arch5",
    "arche": "arch6",
    "arche2": "26in x 38in",
    "arche3": "27in x 39in",
}
"""Dictionary of named sizes.

Keys are names (e.g. ``a4``, ``letter``) and values are strings,
human-readable, and parsable by :func:`parse_papersize` (e.g. ``21cm x
29.7cm``).

.. literalinclude:: ../papersize.py
   :lines: 83-166
"""

# Source: http://en.wikibooks.org/wiki/LaTeX/Lengths
UNITS = {
    "": Decimal("1"),  # Default is point (pt)
    "pt": Decimal("1"),  # point
    "mm": Decimal("7227") / Decimal("2540"),  # millimeter
    "cm": Decimal("7227") / Decimal("254"),  # centimeter
    "in": Decimal("72.27"),  # inch
    "bp": Decimal("803") / Decimal("800"),  # big point
    "pc": Decimal("12"),  # pico
    "dd": Decimal("1238") / Decimal("1157"),  # didot
    "cc": Decimal("14856") / Decimal("1157"),  # cicero
    "nd": Decimal("685") / Decimal("642"),  # new didot
    "nc": Decimal("1370") / Decimal("107"),  # new cicero
    "sp": Decimal("1") / Decimal("65536"),  # scaled point
}
"""Dictionary of units.

Keys are unit abbreviation (e.g. ``pt`` or ``cm``), and values are their value
in points (e.g. ``UNITS['pt']`` is 1, ``UNITS['pc']``] is 12), as
:class:`decimal.Decimal` objects.

.. literalinclude:: ../papersize.py
   :lines: 177-191
"""

PORTRAIT = True
"""Constant corresponding to the portrait orientation

That is, height greater than width.
"""

LANDSCAPE = False
"""Constant corresponding to the landscape orientation

That is, width greater than height.
"""

__UNITS_RE = r"({})".format("|".join(UNITS.keys()))
__SIZE_RE = r"([\d.]+){}".format(__UNITS_RE)
__PAPERSIZE_RE = r"^(?P<width>{size}) *[x× ]? *(?P<height>{size})$".format(
    size=__SIZE_RE
)

__SIZE_COMPILED_RE = re.compile("^{}$".format(__SIZE_RE).format("size"))
__PAPERSIZE_COMPILED_RE = re.compile(__PAPERSIZE_RE.format("width", "height"))


class PapersizeException(Exception):
    """All exceptions of this module inherit from this one."""


class CouldNotParse(PapersizeException):
    """Raised when a string could not be parsed.

    :param str string: String that could not be parsed.
    """

    def __init__(self, string):
        super().__init__()
        self.string = string

    def __str__(self):
        return "Could not parse string '{}'.".format(self.string)


class UnknownOrientation(PapersizeException):
    """Raised when type of argument Orientation is wrong.

    :param obj string: Object wrongly provided as an orientation.
    """

    def __init__(self, string):
        super().__init__()
        self.string = string

    def __str__(self):
        return (
            "'{}' is not one of `papersize.PORTRAIT` or `papersize.LANDSCAPE`"
        ).format(self.string)


def convert_length(length, orig, dest):
    """Convert length from one unit to another.

    :param decimal.Decimal length: Length to convert, as any object convertible
        to a :class:`decimal.Decimal`.
    :param str orig: Unit of ``length``, as a string which is a key of
        :data:`UNITS`.
    :param str dest: Unit in which ``length`` will be converted, as a string
        which is a key of :data:`UNITS`.

    Due to floating point arithmetic, there can be small rounding errors.

    >>> convert_length(0.1, "cm", "mm")
    Decimal('1.000000000000000055511151231')
    """
    return (Decimal(UNITS[orig]) * Decimal(length)) / Decimal(UNITS[dest])


def parse_length(string, unit="pt"):
    """Return a length corresponding to the string.

    :param str string: The string to parse, as a length and a unit, for
        instance ``10.2cm``.
    :param str unit: The unit of the return value, as a key of :data:`UNITS`.
    :return: The length, in an unit given by the ``unit`` argument.
    :rtype: :class:`decimal.Decimal`

    >>> parse_length("1cm", "mm")
    Decimal('1E+1')
    >>> parse_length("1cm", "cm")
    Decimal('1')
    >>> parse_length("10cm")
    Decimal('284.5275590551181102362204724')
    """
    match = __SIZE_COMPILED_RE.match(string)
    if match is None:
        raise CouldNotParse(string)
    return convert_length(Decimal(match.groups()[0]), match.groups()[1], unit)


def parse_couple(string, unit="pt"):
    """Return a tuple of dimensions.

    :param str string: The string to parse, as "LENGTHxLENGTH" (where LENGTH
        are length, parsable by :func:`parse_length`). Example: ``21cm x
        29.7cm``. The separator can be ``x``, ``×`` or empty, surrounded by an
        arbitrary number of spaces. For instance: ``2cmx3cm``, ``2cm x 3cm``,
        ``2cm×3cm``, ``2cm 3cm``.
    :rtype: :class:`tuple`
    :return: A tuple of :class:`decimal.Decimal`, representing the dimensions.

    >>> parse_couple("1cm 10cm", "mm")
    (Decimal('1E+1'), Decimal('1E+2'))
    >>> parse_couple("1mm 10mm", "cm")
    (Decimal('0.1'), Decimal('1'))
    """
    try:
        match = __PAPERSIZE_COMPILED_RE.match(string).groupdict()
        return (parse_length(match["width"], unit), parse_length(match["height"], unit))
    except AttributeError as error:
        raise CouldNotParse(string) from error


def parse_papersize(string, unit="pt"):
    """Return the papersize corresponding to string.

    :param str string: The string to parse. It can be either a named size (as
        keys of constant :data:`SIZES`), or a couple of lengths (that will be
        processed by :func:`parse_couple`). The named paper sizes are case
        insensitive.  The following strings return the same size: ``a4``,
        ``A4``, ``21cm 29.7cm``, ``210mmx297mm``, ``21cm  ×  297mm``…
    :param str unit: The unit of the return values.
    :return: The paper size, as a couple of :class:`decimal.Decimal`.
    :rtype: :class:`tuple`

    >>> parse_papersize("A4", "cm")
    (Decimal('21.00000000000000000000000000'), Decimal('29.70000000000000000000000000'))
    >>> parse_papersize("21cm x 29.7cm", "mm")
    (Decimal('210.0000000000000000000000000'), Decimal('297.0000000000000000000000000'))
    >>> parse_papersize("10 100")
    (Decimal('10'), Decimal('100'))
    """
    if string.lower() in SIZES:
        return parse_papersize(SIZES[string.lower()], unit)
    return parse_couple(string, unit)


def is_portrait(width, height, *, strict=False, fuzzy=False, ndigits=7):
    """Return whether paper orientation is portrait

    That is, height greater or equal to width.

    :param width: Width of paper, as any sortable object.
    :param height: Height of paper, as any sortable object.
    :param bool strict: If ``False``, square format (width equals height) is considered portrait;
        if ``True`` square format is not considered portrait.
    :param bool fuzzy: If ``True``, comparison is done up to ``ndigits`` digits.
    :param int ndigits: Number of digits when using fuzzy comparison.

    >>> is_portrait(11, 10)
    False
    >>> is_portrait(10, 10)
    True
    >>> is_portrait(10, 11)
    True
    """
    if strict and is_square(width, height, fuzzy=fuzzy, ndigits=ndigits):
        return False
    if fuzzy:
        return round(height - width, ndigits=ndigits) >= 0
    return width <= height


def is_landscape(width, height, *, strict=False, fuzzy=False, ndigits=7):
    """Return whether paper orientation is landscape

    That is, width greater or equal to height.

    :param width: Width of paper, as any sortable object.
    :param height: Height of paper, as any sortable object.
    :param strict: If ``False``, square format (width equals height) is considered landscape;
        if ``True`` square format is not considered landscape.
    :param bool fuzzy: If ``True``, comparison is done up to ``ndigits`` digits.
    :param int ndigits: Number of digits when using fuzzy comparison.

    >>> is_landscape(11, 10)
    True
    >>> is_landscape(10, 10)
    True
    >>> is_landscape(10, 11)
    False
    """
    if strict and is_square(width, height):
        return False
    if fuzzy:
        return round(width - height, ndigits=ndigits) >= 0
    return height <= width


def is_square(width, height, *, fuzzy=False, ndigits=7):
    """Return whether paper is a square (width equals height).

    :param width: Width of paper, as any sortable object.
    :param height: Height of paper, as any sortable object.
    :param bool fuzzy: If ``True``, comparison is done up to ``ndigits`` digits.
    :param int ndigits: Number of digits when using fuzzy comparison.

    >>> is_square(11, 10)
    False
    >>> is_square(10, 10)
    True
    >>> is_square(10, 10.00000001, fuzzy=False)
    False
    >>> is_square(10, 10.00000001, fuzzy=True)
    True
    >>> is_square(10, 10.00000001, fuzzy=True, ndigits=10)
    False
    """
    if fuzzy:
        return round(width - height, ndigits) == 0
    return width == height


def rotate(size, orientation):
    """Return the size, rotated if necessary to make it portrait or landscape.

    :param tuple size: Couple paper of dimension, as sortable objects
        (:class:`int`, :class:`float`, :class:`decimal.Decimal`…).
    :param orientation: Return format, one of ``PORTRAIT`` or ``LANDSCAPE``.
    :return: The size, as a couple of dimensions, of the same type of the
        ``size`` parameter.
    :rtype: :class:`tuple`

    >>> rotate((21, 29.7), PORTRAIT)
    (21, 29.7)
    >>> rotate((21, 29.7), LANDSCAPE)
    (29.7, 21)
    """
    if orientation == PORTRAIT:
        return (min(size), max(size))
    if orientation == LANDSCAPE:
        return (max(size), min(size))
    raise UnknownOrientation(orientation)

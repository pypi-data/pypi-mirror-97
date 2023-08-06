#!/usr/bin/env python
#
#  versions.py
"""
NamedTuple-like class to represent a version number.
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
import re
from typing import Dict, Generator, Iterable, Sequence, Tuple, Union

# 3rd party
from typing_extensions import final

__all__ = ["Version"]


@final
class Version(Tuple[int, int, int]):
	"""
	NamedTuple-like class to represent a version number.

	.. versionadded:: 0.4.4

	:param major:

	.. versionchanged:: 1.4.0 Implemented the same interface as a :func:`collections.namedtuple`.
	"""

	__slots__ = ()

	#: The major version number.
	major: int

	#: The minor version number.
	minor: int

	#: The patch version number.
	patch: int

	_fields: Tuple[str, str, str] = ("major", "minor", "patch")
	"""
	Tuple of strings listing the field names.

	Useful for introspection and for creating new named tuple types from existing named tuples.

	.. versionadded:: 1.4.0
	"""

	_field_defaults: Dict[str, int] = {"major": 0, "minor": 0, "patch": 0}
	"""
	Dictionary mapping field names to default values.

	.. versionadded:: 1.4.0
	"""

	@property  # type: ignore
	def major(self):  # noqa: D102
		return self[0]

	@property  # type: ignore
	def minor(self):  # noqa: D102
		return self[1]

	@property  # type: ignore
	def patch(self):  # noqa: D102
		return self[2]

	def __new__(cls, major=0, minor=0, patch=0) -> "Version":  # noqa: D102
		t: "Version" = super().__new__(cls, (int(major), int(minor), int(patch)))  # type: ignore

		return t

	def __repr__(self) -> str:
		"""
		Return the representation of the version.
		"""

		repr_fmt = '(' + ", ".join(f"{name}=%r" for name in self._fields) + ')'
		return self.__class__.__name__ + repr_fmt % self

	def __str__(self) -> str:
		"""
		Return version as a string.
		"""

		return 'v' + '.'.join(str(x) for x in self)  # pylint: disable=not-an-iterable

	def __float__(self) -> float:
		"""
		Return the major and minor version number as a float.
		"""

		return float('.'.join(str(x) for x in self[:2]))

	def __int__(self) -> int:
		"""
		Return the major version number as an integer.
		"""

		return self.major

	def __getnewargs__(self):
		"""
		Return Version as a plain tuple. Used by copy and pickle.
		"""

		return tuple(self)

	def __eq__(self, other) -> bool:
		"""
		Returns whether this version is equal to the other version.

		:type other: str, float, Version
		"""

		other = _prep_for_eq(other)

		if other is NotImplemented:
			return NotImplemented  # pragma: no cover
		else:
			shortest = min(len(self), (len(other)))
			return self[:shortest] == other[:shortest]

	def __gt__(self, other) -> bool:
		"""
		Returns whether this version is greater than the other version.

		:type other: str, float, Version
		"""

		other = _prep_for_eq(other)

		if other is NotImplemented:
			return NotImplemented  # pragma: no cover
		else:
			return tuple(self) > other

	def __lt__(self, other) -> bool:
		"""
		Returns whether this version is less than the other version.

		:type other: str, float, Version
		"""

		other = _prep_for_eq(other)

		if other is NotImplemented:
			return NotImplemented  # pragma: no cover
		else:
			return tuple(self) < other

	def __ge__(self, other) -> bool:
		"""
		Returns whether this version is greater than or equal to the other version.

		:type other: str, float, Version
		"""

		other = _prep_for_eq(other)

		if other is NotImplemented:
			return NotImplemented  # pragma: no cover
		else:
			return tuple(self)[:len(other)] >= other

	def __le__(self, other) -> bool:
		"""
		Returns whether this version is less than or equal to the other version.

		:type other: str, float, Version
		"""

		other = _prep_for_eq(other)

		if other is NotImplemented:
			return NotImplemented  # pragma: no cover
		else:
			return tuple(self)[:len(other)] <= other

	@classmethod
	def from_str(cls, version_string: str) -> "Version":
		"""
		Create a :class:`~.Version` from a :class:`str`.

		:param version_string: The version number.

		:return: The created :class:`~domdf_python_tools.versions.Version`.
		"""

		return cls(*_iter_string(version_string))

	@classmethod
	def from_tuple(cls, version_tuple: Tuple[Union[str, int], ...]) -> "Version":
		"""
		Create a :class:`~.Version` from a :class:`tuple`.

		:param version_tuple: The version number.

		:return: The created :class:`~domdf_python_tools.versions.Version`.

		.. versionchanged:: 0.9.0

			Tuples with more than three elements are truncated.
			Previously a :exc:`TypeError` was raised.
		"""

		return cls(*(int(x) for x in version_tuple[:3]))

	@classmethod
	def from_float(cls, version_float: float) -> "Version":
		"""
		Create a :class:`~.Version` from a :class:`float`.

		:param version_float: The version number.

		:return: The created :class:`~domdf_python_tools.versions.Version`.
		"""

		return cls.from_str(str(version_float))

	def _asdict(self) -> Dict[str, int]:
		"""
		Return a new dict which maps field names to their corresponding values.

		.. versionadded:: 1.4.0
		"""

		return {
				"major": self.major,
				"minor": self.minor,
				"patch": self.patch,
				}

	def _replace(self, **kwargs) -> "Version":
		"""
		Return a new instance of the named tuple replacing specified fields with new values.

		.. versionadded:: 1.4.0

		:param kwargs:
		"""

		return self.__class__(**{**self._asdict(), **kwargs})

	@classmethod
	def _make(cls, iterable: Iterable[Union[str, int]]) -> "Version":
		"""
		Class method that makes a new instance from an existing sequence or iterable.

		.. versionadded:: 1.4.0

		:param iterable:
		"""

		return cls(*(int(x) for x in tuple(iterable)[:3]))


def _iter_string(version_string: str) -> Generator[int, None, None]:
	"""
	Iterate over the version elements from a string.

	:param version_string: The version as a string.

	:return: Iterable elements of the version.
	"""

	return (int(x) for x in re.split("[.,]", version_string))


def _iter_float(version_float: float) -> Generator[int, None, None]:
	"""
	Iterate over the version elements from a float.

	:param version_float: The version as a float.

	:return: Iterable elements of the version.
	"""

	return _iter_string(str(version_float))


def _prep_for_eq(other: Union[str, float, Version], ) -> Tuple[int, ...]:
	"""
	Prepare 'other' for use in ``__eq__``, ``__le__``, ``__ge__``, ``__gt__``, and ``__lt__``.
	"""

	if isinstance(other, str):
		return tuple(_iter_string(other))
	elif isinstance(other, (Version, Sequence)):
		return tuple(int(x) for x in other)
	elif isinstance(other, (int, float)):
		return tuple(_iter_float(other))
	else:  # pragma: no cover
		return NotImplemented

__author__ = "David Scheliga"
__email__ = "david.scheliga@gmx.de"
__version__ = "0.3.2"
__all__ = [
    "STANDARD_CONVENTION_NAME",
    "NameGiver",
    "register_filename_validator",
    "get_filename_validator",
    "get_filename_convention",
    "disassemble_filename",
    "construct_filename",
    "construct_filepath",
    "ANameGiver",
    "NameGiver",
]

import copy
import re
from abc import ABC, abstractmethod
from collections.abc import Mapping

import jsonschema
from typing import (
    Union,
    AnyStr,
    Pattern,
    Iterator,
    Optional,
    Dict,
    Tuple,
    TypeVar,
    List,
    Any,
    Generator,
)
from functools import lru_cache
from pathlib import Path


_MATCHES_UUID4 = re.compile(
    "[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
)


STANDARD_CONVENTION_NAME = "Standard March 2021"
_FILE_NAMING_CONVENTION = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Naming Convention for Specimen Files",
    "description": "JSON Schema for filenames related to specimen.",
    "name": STANDARD_CONVENTION_NAME,
    "type": "object",
    "template": "{identifier}{sub_id}{source_id}{vargroup}{context}{extension}",
    "properties": {
        "identifier": {
            "description": "The specimen's identifier by its projects name or its UUID4",
            "type": "string",
            "minLength": 1,
            "maxLength": 36,
            "pattern": r"^[0-9a-zA-Z-_]+$",
            "search_pattern": "^[0-9a-zA-Z-_]+",
        },
        "extension": {"type": "string", "search_pattern": r"\.[0-9a-zA-Z]+$"},
        "sub_id": {
            "type": "string",
            "minLength": 1,
            "maxLength": 4,
            "pattern": r"^[0-9A-Z]+$",
            "search_pattern": "#[0-9A-Z]{1,4}",
            "prefix": "#",
        },
        "source_id": {
            "type": "string",
            "minLength": 5,
            "maxLength": 12,
            "pattern": r"^[0-9a-zA-Z-]+$",
            "search_pattern": r"#[0-9a-zA-Z-]{5,12}",
            "prefix": "#",
        },
        "context": {
            "type": "string",
            "minLength": 3,
            "maxLength": 16,
            "pattern": r"^[a-zA-Z]+[0-9a-zA-Z-]+$",
            "search_pattern": r"\.[a-zA-Z]{1}[0-9a-zA-Z-]{2,15}",
            "prefix": ".",
        },
        "vargroup": {
            "type": "array",
            "pattern": r"^#(_[a-zA-Z0-9+-,. ]+)+$",
            "search_pattern": r"#(_[0-9a-zA-Z+-,. ]+)+",
            "prefix": "#_",
            "delimiter": "_",
        },
    },
    "required": ["identifier"],
    "dependencies": {"context": ["extension"]},
}


JsonschemaValidator = TypeVar("JsonschemaValidator")
"""
A Validator implementing the jsonschema.IValidator interface.
"""

FILENAME_VALIDATOR = jsonschema.Draft7Validator(_FILE_NAMING_CONVENTION)
FilenameConvention = Dict
"""
A filename convention is a jsonschema, which requires the custom field **template**
containing a standard python string with formatting specifiers. The specifiers matches
the properties of the jsonschema. Additional custom fields of the *properties* are
*search_pattern* and *prefix*.

:template: A python string with formatting specifiers like "{part1}{part2}". Located in
           the jsonschemas root.
:search_pattern: The regular expression by which the specific part can be recognized.
:prefix: A prefix which is put in front of the name part.
"""

_ROOT_PATH_NAME = "root_path"

_registered_validators = {STANDARD_CONVENTION_NAME: FILENAME_VALIDATOR}


@lru_cache(maxsize=10)
def _compile_regex(pattern: str) -> Pattern[AnyStr]:
    return re.compile(pattern)


def register_filename_validator(filename_validator: JsonschemaValidator) -> bool:
    """
    Registers file naming convention. Does **not override existing** file naming
    conventions.

    Args:
        filename_validator:

    Raises:
        TypeError:
            If validator doesn't provide a schema attribute, meaning it doesn't
            implement JsonschemaValidator.

        AttributeError:
            If 'name' is missing within the file naming convention.

    .. warning::

        This function doesn't override already registered filename conventions. If
        the convention name is already occupied this function returns `False`. Check
        the functions return value and decide how to react on it.

    .. warning::

        This function doesn't check the full validity of the custom file naming
        convention. Whether your custom file naming convention runs or not should be
        tested using standard python testing environments. Use this function, if
        you know what you are doing.

    Returns:
        bool:
            `True` if the naming convention is registered using the name of this
            convention, or `False` if the name was already occupied.

    """
    try:
        naming_schema = filename_validator.schema
    except AttributeError:
        raise TypeError(
            "filename_validator doesn't provide a `schema` attribute. A validator must"
            " implement a jsonschema.IValidator or namefiles.JsonschemaValidator."
        )

    try:
        name_of_convention = naming_schema["name"]
    except KeyError:
        raise KeyError("The file naming convention provided doesn't have a name.")

    global _registered_validators
    already_registered_do_not_override = name_of_convention in _registered_validators
    if already_registered_do_not_override:
        return False

    _registered_validators[name_of_convention] = copy.deepcopy(filename_validator)
    return True


@lru_cache(maxsize=10)
def get_filename_validator(
    convention_name: Optional[str] = None,
) -> JsonschemaValidator:
    """
    Returns a filename validator for applying the file naming convention.

    Args:
        convention_name:
            The registered conventions name.

    Returns:
        JsonschemaValidator

    Raises:
        KeyError:
            On missing convention for requested name.

    Examples:
        >>> from namefiles import get_filename_validator, STANDARD_CONVENTION_NAME
        >>> type(get_filename_validator())
        <class 'jsonschema.validators.create.<locals>.Validator'>

        >>> get_filename_convention("not existing")
        Traceback (most recent call last):
        ...
        KeyError: "No file naming convention named by 'not existing' could be found."
    """
    if convention_name is None:
        convention_name = STANDARD_CONVENTION_NAME
    try:
        requested_validator = _registered_validators[convention_name]
    except KeyError:
        raise KeyError(
            "No file naming convention named by '{}' could be found."
            "".format(convention_name)
        )
    return copy.deepcopy(requested_validator)


@lru_cache(maxsize=10)
def get_filename_convention(convention_name: Optional[None] = None) -> dict:
    """
    Gets the currently defined file naming convention.

    Args:
        convention_name:
            The targeted file naming convention's name. Returns the standard
            file naming convention by default, if no name is defined.

    Returns:
        dict

    Examples:
        >>> from namefiles import get_filename_convention
        >>> import json
        >>> standard_convention = get_filename_convention()
        >>> standard_representation = json.dumps(standard_convention, indent="  ")
        >>> print(standard_representation)
        {
          "$schema": "http://json-schema.org/draft-07/schema#",
          "title": "Naming Convention for Specimen Files",
          "description": "JSON Schema for filenames related to specimen.",
          "name": "Standard March 2021",
          "type": "object",
          "template": "{identifier}{sub_id}{source_id}{vargroup}{context}{extension}",
          "properties": {
            "identifier": {
              "description": "The specimen's identifier by its projects name or its UUID4",
              "type": "string",
              "minLength": 1,
              "maxLength": 36,
              "pattern": "^[0-9a-zA-Z-_]+$",
              "search_pattern": "^[0-9a-zA-Z-_]+"
            },
            "extension": {
              "type": "string",
              "search_pattern": "\\\\.[0-9a-zA-Z]+$"
            },
            "sub_id": {
              "type": "string",
              "minLength": 1,
              "maxLength": 4,
              "pattern": "^[0-9A-Z]+$",
              "search_pattern": "#[0-9A-Z]{1,4}",
              "prefix": "#"
            },
            "source_id": {
              "type": "string",
              "minLength": 5,
              "maxLength": 12,
              "pattern": "^[0-9a-zA-Z-]+$",
              "search_pattern": "#[0-9a-zA-Z-]{5,12}",
              "prefix": "#"
            },
            "context": {
              "type": "string",
              "minLength": 3,
              "maxLength": 16,
              "pattern": "^[a-zA-Z]+[0-9a-zA-Z-]+$",
              "search_pattern": "\\\\.[a-zA-Z]{1}[0-9a-zA-Z-]{2,15}",
              "prefix": "."
            },
            "vargroup": {
              "type": "array",
              "pattern": "^#(_[a-zA-Z0-9+-,. ]+)+$",
              "search_pattern": "#(_[0-9a-zA-Z+-,. ]+)+",
              "prefix": "#_",
              "delimiter": "_"
            }
          },
          "required": [
            "identifier"
          ],
          "dependencies": {
            "context": [
              "extension"
            ]
          }
        }
    """
    validator_of_convention = get_filename_validator(convention_name=convention_name)
    return validator_of_convention.schema


def _extract_filename_parts(
    potential_filename_parts: dict, file_naming_convention: Optional[dict] = None
) -> dict:
    """
    Extracts filename parts from a dictionary based by a file naming convention.

    Args:
        potential_filename_parts:
            A dictionary which potentially contains filename parts to be applied
            by the defined file naming convention.

        file_naming_convention:
            The file naming convention jsonschema, which should be applied.

    Returns:
        dict
    """
    if file_naming_convention is None:
        file_naming_convention = get_filename_convention()

    result = {}
    if "root_path" in potential_filename_parts:
        result["root_path"] = potential_filename_parts["root_path"]
    for name_part_id in file_naming_convention["properties"]:
        if (
            name_part_id in potential_filename_parts
            and potential_filename_parts[name_part_id]
        ):
            result[name_part_id] = potential_filename_parts[name_part_id]
    return result


def disassemble_filename(
    target_path: Union[Path, str],
    filename_validator: Optional[JsonschemaValidator] = None,
) -> dict:
    """
    Disassembles a file's name into the parts defined by a file naming convention.

    Args:
        target_path:
            The file which name should be disassembled.

        filename_validator:
            The validator to validate the filename parts with its file naming
            convention.

    Returns:
        dict

    Examples:
        >>> from namefiles import disassemble_filename
        >>> from doctestprinter import doctest_print
        >>> disassemled_filename = disassemble_filename(
        ...     "zoo/cage/Zebra#A#Afrika#_ffffff_000000.animal.stock"
        ... )
        >>> doctest_print(disassemled_filename, max_line_width=70)
        {'identifier': 'zoo', 'extension': '.stock', 'sub_id': 'A', 'source_id':
        'Afrika', 'context': 'animal', 'vargroup': ['ffffff', '000000']}
    """

    if filename_validator is None:
        fnc = FILENAME_VALIDATOR.schema
    else:
        try:
            fnc = filename_validator.schema
        except AttributeError:
            raise TypeError(
                "The given validator doesn't implement "
                "the JsonSchemaValidator interface."
            )

    result = dict([(key, "") for key in fnc["properties"]])
    used_path = Path(target_path)
    if used_path.is_absolute():
        result["root_path"] = used_path.parent
        head = str(used_path.name)
    else:
        head = str(used_path)
    for partid, item in fnc["properties"].items():
        if "search_pattern" not in item:
            continue
        matcher = _compile_regex(item["search_pattern"])
        match = matcher.search(head)
        if match:
            start, end = match.span()
            addition = 0
            if "prefix" in item:
                prefix = item["prefix"]
                addition = len(prefix)
            result[partid] = head[start + addition : end]
            head = head[:start] + head[end:]
            if "delimiter" in item:
                result[partid] = result[partid].split(item["delimiter"])
    return result


def construct_filename(
    filename_template: Optional[str] = None,
    filename_validator: Optional[JsonschemaValidator] = None,
    **filename_parts
) -> str:
    """
    Constructs a filename using a filename convention.

    Args:
        filename_template:
            A template providing a ``format`` method to be called with the fileparts.

        filename_validator:
            The validator to validate the filename parts with its file naming
            convention.

        **filename_parts:
            File name parts as keywords to be used for the filename construction.

    Returns:
        str

    Examples:
        >>> import namefiles
        >>> namefiles.construct_filename(identifier="basename")
        'basename'
        >>> namefiles.construct_filename(identifier="basename", extension=".txt")
        'basename.txt'
        >>> namefiles.construct_filename(
        ...     identifier="basename", sub_id="SUB1", extension=".txt"
        ... )
        'basename#SUB1.txt'
        >>> namefiles.construct_filename(
        ...     identifier="basename",
        ...     sub_id="SUB1",
        ...     vargroup = ["Alibaba", 40, "thieves"],
        ...     source_id = "arabia",
        ...     context = "tale",
        ...     extension = ".txt"
        ... )
        'basename#SUB1#arabia#_Alibaba_40_thieves.tale.txt'

        >>> namefiles.construct_filename(identifier="basename", context="tale")
        Traceback (most recent call last):
        ...
        ValueError: Filename cannot be constructed, because , 'extension' is a dependency of 'context'
    """
    construction_parts = _extract_filename_parts(filename_parts)
    if filename_validator is None:
        filename_validator = FILENAME_VALIDATOR
    template = filename_validator.schema["template"]
    if filename_template is not None:
        template = filename_template

    parts_are_valid, error_message = _validate_name_parts_collect_errors(
        construction_parts, filename_validator=filename_validator
    )
    if not parts_are_valid:
        raise ValueError(error_message)

    part_properties = filename_validator.schema["properties"]
    parts = dict([(key, "") for key in part_properties])

    for partid, item in part_properties.items():
        if partid not in construction_parts:
            continue
        try:
            prefix = item["prefix"]
        except KeyError:
            prefix = ""
        if item["type"] == "array":
            values = [str(x) for x in construction_parts[partid]]
            value = item["delimiter"].join(values)
        else:
            value = construction_parts[partid]
        parts[partid] = "{}{}".format(prefix, value)
    filename = template.format(**parts)
    return filename


def _validate_name_parts_collect_errors(
    construct_parts, filename_validator
) -> Tuple[bool, str]:
    """

    Args:
        construct_parts:
        filename_validator:

    Returns:

    Examples:
        >>> from namefiles import (
        ...     _validate_name_parts_collect_errors,
        ...     FILENAME_VALIDATOR
        ... )
        >>> from doctestprinter import doctest_print
        >>> invalid_parts = {"identifier": "A?", "context": "invalid_cause_to_long"}
        >>> is_false, message = _validate_name_parts_collect_errors(
        ...     construct_parts=invalid_parts, filename_validator=FILENAME_VALIDATOR
        ... )
        >>> doctest_print(message, max_line_width=70)
        Filename cannot be constructed, because , identifier 'A?' does not match
        '^[0-9a-zA-Z-_]+$', context 'invalid_cause_to_long' is too long, context
        'invalid_cause_to_long' does not match '^[a-zA-Z]+[0-9a-zA-Z-]+$', 'extension'
        is a dependency of 'context'


    """
    errors = [error for error in filename_validator.iter_errors(construct_parts)]
    no_errors_occurred_everything_is_fine = not errors
    if no_errors_occurred_everything_is_fine:
        return True, ""

    error_message = "Filename cannot be constructed, because "
    for error in errors:
        if error.path:
            part_id = "/".join(error.path)
            name_part = construct_parts[part_id]
            part_is_optional = part_id not in filename_validator.schema["required"]
            part_is_optional_and_empty = not name_part and part_is_optional
            if part_is_optional_and_empty:
                continue
            error_message += ", {} {}".format(part_id, error.message)
        else:
            error_message += ", {}".format(error.message)
    return False, error_message


def construct_filepath(
    filename_template: Optional[str] = None,
    filename_validator: Optional[JsonschemaValidator] = None,
    root_path: str = None,
    **filename_parts
) -> Path:
    """
    Constructs a filepath using a file naming convention.

    Args:
        filename_template:
            A template providing a ``format`` method to be called with the fileparts.

        filename_validator:
            The validator to validate the filename parts with its file naming
            convention.

        root_path:
            The file's root path.

        **filename_parts:
            File name parts as keywords to be used for the filename construction.

    Returns:
        Path

    Examples:
        >>> from namefiles import construct_filepath, FILENAME_VALIDATOR
        >>> sample_pathlib_path = construct_filepath(
        ...     root_path="/a/path", identifier="file", sub_id="NAME"
        ... )
        >>> str(sample_pathlib_path)
        '/a/path/file#NAME'

    """
    assert root_path is not None, "A root_path needs to be defined."
    filename = construct_filename(
        filename_template, filename_validator=filename_validator, **filename_parts
    )
    filepath = Path(root_path, filename)
    return filepath


class ANameGiver(Mapping, ABC):
    def __init__(self, **filename_parts):
        """
        *A Name Giver* is the abstract base class, which can be used to define
        a custom file naming convention. This can achived subclassing ANameGiver
        and overriding its classmethod *get_filename_validator*, which needs
        to return a jsonschema.IValidator.

        Notes:
            jsonschema has no declaration of IValidator. The called methods
            within namefiles are declared within JsonschemaValidator as a
            substitution.

        Args:
            **filename_parts:
                Filename parts for the implemented file name convention.

        Examples:
            To enable a custom filename convention you subclass
            :class:`namefiles.ANameGiver` and override the
            :func:`namefiles.ANameGiver.get_filename_validator` providing your
            file naming convention. In this example the naming convention of
            :mod:`namefiles` is used, which uses the jsonschema draft 7 specification.

            >>> from doctestprinter import doctest_print
            >>> from jsonschema import Draft7Validator
            >>> from namefiles import ANameGiver, get_filename_convention
            >>> class MyNameGiver(ANameGiver):
            ...     CUSTOM_VALIDATOR = Draft7Validator(get_filename_convention())
            ...     @classmethod
            ...     def get_filename_validator(cls) -> FilenameConvention:
            ...         # Put your custom file naming convention (jsonschema) here
            ...         return cls.CUSTOM_VALIDATOR
            >>> sample_giver = MyNameGiver.disassemble("A#NAME.txt")
            >>> sample_giver
            MyNameGiver(root_path: ., identifier: A, extension: .txt, sub_id: NAME)
            >>> str(sample_giver)
            'A#NAME.txt'
            >>> sample_giver.set_parts(
            ...     identifier="Zebra", vargroup=["in", "the"], extension=".zoo"
            ... )
            >>> str(sample_giver)
            'Zebra#NAME#_in_the.zoo'
            >>> sample_giver.set_parts(
            ...     identifier="Z", sub_id="BRA", vargroup="", extension=""
            ... )
            >>> str(sample_giver)
            'Z#BRA'

            Implements collections.abc.Mapping

            >>> converted_into_dict = dict(sample_giver)
            >>> doctest_print(converted_into_dict, max_line_width=70)
            {'root_path': '.', 'identifier': 'Z', 'extension': '', 'sub_id': 'BRA',
            'source_id': '', 'context': '', 'vargroup': ''}
            >>> len(sample_giver)
            7
            >>> sample_giver["sub_id"]
            'BRA'

            Disassembling of path and filename

            >>> sample_giver = MyNameGiver.disassemble("/a/path/Z#BRA.txt")
            >>> sample_giver
            MyNameGiver(root_path: /a/path, identifier: Z, extension: .txt, sub_id: BRA)
            >>> str(sample_giver.to_path())
            '/a/path/Z#BRA.txt'
            >>> str(sample_giver.to_path(root_path="/another/path"))
            '/another/path/Z#BRA.txt'
        """
        self._filename_parts = {}
        self._initialize_filename_parts(filename_parts)

    def _initialize_filename_parts(self, potential_filename_parts):
        """
        This method is there to guard ANameGiver from large amounts of keys
        if a custom dictionary with containing filename parts is used.

        Args:
            potential_filename_parts:
                Filename parts

        Returns:

        """
        my_convention = self.get_filename_validator().schema

        if _ROOT_PATH_NAME in potential_filename_parts:
            root_path = potential_filename_parts[_ROOT_PATH_NAME]
            self._filename_parts[_ROOT_PATH_NAME] = root_path

        for part_key in my_convention["properties"]:
            if part_key not in potential_filename_parts:
                continue
            self._filename_parts[part_key] = potential_filename_parts[part_key]

    def __repr__(self):
        filename_parts = [
            "{}: {}".format(part_name, part_value)
            for part_name, part_value in self._filename_parts.items()
            if part_value
        ]
        all_parts_together = ", ".join(filename_parts)
        return "{}({})".format(self.__class__.__name__, all_parts_together)

    def __str__(self):
        return construct_filename(
            filename_validator=self.get_filename_validator(), **self._filename_parts
        )

    def __getitem__(self, part_name: str) -> Any:
        """
        Returns a filename part for the part's name.

        Args:
            part_name:
                Name of the requested part.

        Returns:
            Any
        """
        return self._filename_parts[part_name]

    def __len__(self) -> int:
        return len(self._filename_parts)

    def __iter__(self) -> Iterator[str]:
        return iter(self._filename_parts)

    def keys(self) -> Generator:
        """
        Filename parts of the filename convention.

        Returns:
            Generator
        """
        return self._filename_parts.keys()

    def items(self) -> Generator:
        """
        The filename's parts as key value pairs.

        Returns:
            Generator
        """
        yield from self._filename_parts.items()

    def with_parts(self, **filename_parts) -> "ANameGiver":
        """
        Returns a new instance with the old part overridden by the potential_filename_parts
        provided.

        Args:
            **filename_parts:
                New filename parts overriding the old ones.

        Returns:
            ANameGiver

        Examples:
            >>> from namefiles import NameGiver
            >>> new_filename = NameGiver.disassemble("A#file.txt").with_parts(
            ...     sub_id="NEW", source_id="filename"
            ... )
            >>> str(new_filename)
            'A#NEW#filename.txt'
        """
        requested_name_giver = copy.deepcopy(self)
        requested_name_giver.set_parts(**filename_parts)
        return requested_name_giver

    def set_parts(self, **filename_parts):
        """
        Sets filename parts with new values.

        Args:
            **filename_parts:
                Parts which should be set with new values.
        """
        for part_id, part_value in filename_parts.items():
            self._filename_parts[part_id] = part_value

    def to_path(self, root_path: Optional[Union[str, Path]] = None) -> Path:
        """
        Returns a :class:`pathlib.Path` of the declared filename parts.

        Args:
            root_path:
                Optional root path of the resulting filename. Default will be
                the working directory.

        Returns:
            pathlib.Path
        """
        if root_path is not None and isinstance(root_path, (str, Path)):
            used_parts = self._filename_parts.copy()
            used_parts["root_path"] = str(root_path)
        else:
            used_parts = self._filename_parts
        return construct_filepath(**used_parts)

    @classmethod
    @abstractmethod
    def get_filename_validator(cls) -> JsonschemaValidator:
        """
        Returns this name givers validator providing the file naming convention.

        Returns:
            JsonschemaValidator
        """
        pass

    def set_name_part(self, part_name: str, part_value: str):
        """
        Sets the value of a convention's filename part.

        Args:
            part_name:
                Name of the convention's filename part.

            part_value:
                New value of the filename part.
        """
        self._filename_parts[part_name] = part_value

    @classmethod
    def disassemble(cls, filename_or_path) -> "ANameGiver":
        """
        Disassembles the filename returning ANameGiver.

        Args:
            filename_or_path:
                Either a path or filename. A path's parent is used if a filepath is
                provided.

        Returns:
            ANameGiver
        """
        filepath = Path(filename_or_path)
        filename = filepath.name
        root_path = str(filepath.parent)
        filename_parts = disassemble_filename(
            filename, filename_validator=cls.get_filename_validator()
        )
        return cls(root_path=root_path, **filename_parts)


class NameGiver(ANameGiver):
    def __init__(self, **filename_parts):
        """
        The *Name Giver* implements the current standard file naming convention.
        The NameGiver is the convinient method to make a new filename based
        on the latest standard file naming convention.

        Examples:
            The major entry point is the disassemble method, which returns a
            NameGiver instance containing all filename parts based on the
            latest standard file naming convention.
            >>> from namefiles import NameGiver
            >>> sample_giver = NameGiver.disassemble("A#NAME.txt")
            >>> sample_giver
            NameGiver(root_path: ., identifier: A, extension: .txt, sub_id: NAME)

            The NameGiver mimics a Mapping and additionally providing
            the major filename parts as properties.
            >>> sample_giver["identifier"]
            'A'
            >>> sample_giver["sub_id"]
            'NAME'
            >>> sample_giver.identifier
            'A'
            >>> sample_giver.identifier = "Zebra"
            >>> sample_giver.identifier
            'Zebra'

            Either convert the instance to a string to get a filename (filepath)
            >>> str(sample_giver)
            'Zebra#NAME.txt'

            or use the :func:`NameGiver.to_path` method to receive a
            :class:`pathlib.PurePath`.

        """
        super().__init__(**filename_parts)

    @classmethod
    def get_filename_validator(cls) -> FilenameConvention:
        return FILENAME_VALIDATOR

    @property
    def identifier(self) -> str:
        """
        The mandatory entity's name which relates to multiple files. The *identifier*
        is the leading filename part.

        Notes:
            The identifier has a maximum length of 36 characters and can consist of
            words [`a-zA-Z0-9_`] with the addition of the hyphen-minus '-' (U+002D),
            which should be the default on keyboards.

            Its regular expression ``^[0-9a-zA-Z-_]+$``

        Examples:
            Minimal to maximal identifier examples.

            ::

                a                                       # At leas 1 character is needed.
                1044e098-7bfb-11eb-9439-0242ac130002    # 36 chars allows a UUID

        Returns:
            str
        """
        return self["identifier"]

    @identifier.setter
    def identifier(self, value):
        self.set_name_part("identifier", value)

    @property
    def sub_id(self) -> str:
        """
        The *sub id* is the first branch of the identifier.

        Notes:
            The sub identifier allows uppercase words without the underscore
            [A-Z0-9] with a maximum length of 4.

            Its regular expression is ``^[0-9a-zA-Z-]+$``

            The sub identifier's task is to distinguish different states of the same
            context. A context in this term could be different video captures of the
            same object with multiple cameras or just different file versions.

            The sub identifier should be seen as a branch of the identifier. Not
            a version within a sequence.

        Examples:
            Multiple different video captures of the same object.

            ::

                ant#CAM0.avi
                ant#CAM1.avi
                ant#CAM2.avi

            Different children (versions).

            ::

                a#1
                a#1ST
                a#2ND
                a#RAW

        Returns:
            str
        """
        return self["sub_id"]

    @sub_id.setter
    def sub_id(self, value):
        self.set_name_part("sub_id", value)

    @property
    def source_id(self) -> str:
        """
        The *source id* states, where this file came from.

        Notes:
            The source identifier allows words without underscores [`a-zA-Z0-9`] with
            the addition of the hyphen-minus `'-'` (U+002D),
            which should be the default on keyboards.

            Its regular expression is ``^[0-9a-zA-Z-]+$``

            The source identifier states different sources, whenever the context would
            lead to equal filenames. it might be the name of the program or device which
            made this file.

        Examples:

            A comparison of sources onto 2 different sub versions of *Zeb-a*.

            ::

                Zeb-a#1#canon.jpg
                Zeb-a#2#canon.jpg
                Zeb-a#1#nikon.jpg
                Zeb-a#2#nikon.jpg

        Returns:
            str
        """
        return self["source_id"]

    @source_id.setter
    def source_id(self, value):
        self.set_name_part("source_id", value)

    @property
    def vargroup(self) -> List[str]:
        """
        The *group of variables* (vargroup) contains meta attributes.

        Notes:
            Each variable of the group is a string. It allows words [`a-zA-Z0-9_`] with
            the addition of:

                - '-' `hyphen-minus` (U+002D)
                - '+' plus
                - ',' comma
                - '.' dot

            Its regular expression is ``^#(_[a-zA-Z0-9+-,. ]+)+$``

             Examples in which meta attributes are stored in the filename:

             - number of a subsequent sequence e.g. image sequences
             - a date neither being the creation nor the change date

        Examples:

            >>> from namefiles import NameGiver
            >>> NameGiver.disassemble("Zeb-a#_000000_ffffff_1.9m_no color").vargroup
            ['000000', 'ffffff', '1.9m', 'no color']

        Returns:
            List[str]
        """
        group_of_variables = self["vargroup"]
        assert isinstance(
            group_of_variables, list
        ), "A list is expected. Got {} instead.".format(type(group_of_variables))
        return group_of_variables

    @vargroup.setter
    def vargroup(self, value):
        self.set_name_part("vargroup", value)

    @property
    def context(self) -> str:
        """
        *Context* of the file's content.

        Notes:
            The context allows words without underscores [a-zA-Z0-9]
            starting with alphabetic character.

            Its regular expression is ``^[a-zA-Z]+[0-9a-zA-Z-]+$``

            While the file extension just states the formatting of the file
            like '.txt' being a text file or '.csv' being a specifically
            formatted text file, they do not state any information about their
            context.

        Returns:
            str
        """
        return self["context"]

    @context.setter
    def context(self, value):
        self.set_name_part("context", value)

    @property
    def extension(self):
        """
        The common file extension with a leading dot.

        Notes:
            The extension states how the content is encoded and which structure it has.

        Examples:
            A file ending with '.txt' is a plain text file, which is encoded with
            'utf-8' in best case.

            A file ending with '.csv' is a plain text file, which contains a table
            having *'comma seperated values'*. Other examples are common formats like
            *.json* or *.yml*.

            Instead of creating non-common file endings for custom text based file
            formats. The text files should end with '.txt'. To state the custom
            content the *context* file part can be used.

        Returns:
            str
        """
        return self["extension"]

    @extension.setter
    def extension(self, value):
        self.set_name_part("extension", value)
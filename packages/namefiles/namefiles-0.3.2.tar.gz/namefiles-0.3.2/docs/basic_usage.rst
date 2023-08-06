********************
Basic Usage
********************

At the current implementation :mod:`namefiles` revolves around getting filenames
within python scripts, which comply to a file naming convention.

A first use case is using a source filename for a new filename. You might have
a source file which is used for a process resulting into a new file, for which
a related name is required.

By quickly setting the fresh filename parts a new path can be obtained.

.. doctest::

    >>> from namefiles import NameGiver
    >>> source_filename = NameGiver.disassemble("/root/path/A#file.txt")
    >>> target_filename = source_filename.with_parts(
    ...     sub_id="NEW", source_id="filename"
    ... )
    >>> target_filename.to_path()
    PosixPath('/root/path/A.txt')


Another use case is using metadata already carrying the filename parts.

.. doctest::

    >>> sample_metadata = {
    ...     "identifier": "A",
    ...     "sub_id": "FILE",
    ...     "context": "name",
    ...     "non-filename-field": "Is not for the filename."
    ... }
    >>> from namefiles import NameGiver
    >>> new_filepath_giver = NameGiver(
    ...     root_path="/root/path", extension=".txt", **sample_metadata
    ... )
    >>> str(new_filepath)
    '/root/path/A#FILE.name.txt'
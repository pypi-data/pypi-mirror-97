from pathlib import Path

from namefiles import NameGiver


def test_name_giver():
    sample_giver = NameGiver(identifier="Book1")

    sample_giver.identifier = "Book2"
    assert sample_giver.identifier == "Book2"

    sample_giver.sub_id = "ED01"
    assert sample_giver.sub_id == "ED01"

    sample_giver.vargroup = ["Abibaba", 40, "Thieves"]
    assert sample_giver.vargroup == ["Abibaba", 40, "Thieves"]

    sample_giver.source_id = "1001nights"
    assert sample_giver.source_id == "1001nights"

    sample_giver.context = "tales"
    assert sample_giver.context == "tales"

    sample_giver.extension = ".txt"
    assert sample_giver.extension == ".txt"


def test_metadata_case():
    sample_metadata = {
        "identifier": "A",
        "sub_id": "FILE",
        "context": "name",
        "non-filename-field": "Is not for the filename."
    }
    sample_name = NameGiver(extension=".txt", **sample_metadata)
    assert str(sample_name) == "A#FILE.name.txt"
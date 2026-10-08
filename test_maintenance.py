from maintenance import get_request, validate_request, get_team


def test_get_request():
    request = get_request("M001")

    assert request is not None
    assert request["request_id"] == "M001"


def test_request_not_found():
    request = get_request("M999")

    assert request is None


def test_valid_request():
    request = {
        "request_id": "M100",
        "resident_name": "Test Resident",
        "phone": "0400000000",
        "address": "Testikatu 1",
        "apartment": "1A",
        "description": "The kitchen sink is leaking."
    }

    missing = validate_request(request)

    assert missing == []


def test_missing_description():
    request = {
        "request_id": "M100",
        "resident_name": "Test Resident",
        "phone": "0400000000",
        "address": "Testikatu 1",
        "apartment": "1A",
        "description": ""
    }

    missing = validate_request(request)

    assert "description" in missing


def test_multiple_missing_fields():
    request = {
        "request_id": "M100",
        "resident_name": "",
        "phone": "",
        "address": "Testikatu 1",
        "apartment": "1A",
        "description": "The kitchen sink is leaking."
    }

    missing = validate_request(request)

    assert "resident_name" in missing
    assert "phone" in missing


def test_team_mapping():
    assert get_team("Plumbing") == "Plumbing Team"
    assert get_team("Electrical") == "Electrical Team"
    assert get_team("Heating") == "Heating Team"
    assert get_team("Building") == "Building Maintenance"
    assert get_team("Other") == "Manual Review"


def test_unknown_category_goes_to_manual_review():
    assert get_team("Unknown") == "Manual Review"
from maintenance import get_request,validate_request,get_team


def test_get_request():
    request = get_request("M001")

    assert request is not None
    assert request["request_id"] == "M001"


def test_request_not_found():
    request = get_request("M999")

    assert request is None

def test_missing_description():
    request = {
        "request_id": "M100",
        "description": ""
    }

    missing = validate_request(request)

    assert "description" in missing


def test_team_mapping():
    assert get_team("Plumbing") == "Plumbing Team"
    assert get_team("Electrical") == "Electrical Team"
    assert get_team("Heating") == "Heating Team"
    assert get_team("Building") == "Building Maintenance"
    assert get_team("Other") == "Manual Review"
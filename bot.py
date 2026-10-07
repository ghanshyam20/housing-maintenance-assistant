from maintenance import get_request, validate_request
from classifier import classify_request


def process_request(request_id):
    request = get_request(request_id)

    if request is None:
        print("Request not found")
        return

    missing = validate_request(request)

    if missing:
        print("Missing fields:", missing)
        return

    category = classify_request(request["description"])

    print("Request:", request["request_id"])
    print("Problem:", request["description"])
    print("Category:", category)


if __name__ == "__main__":
    process_request("M001")

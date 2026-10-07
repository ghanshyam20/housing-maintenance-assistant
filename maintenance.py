import csv

REQUESTS_FILE = "data/requests.csv"


def get_request(request_id):
    with open(REQUESTS_FILE, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["request_id"] == request_id:
                return row

    return None


def validate_request(request):
    required_fields = [
        "request_id",
        "resident_name",
        "phone",
        "address",
        "apartment",
        "description",
    ]

    missing = []

    for field in required_fields:
        if not request.get(field, "").strip():
            missing.append(field)

    return missing



if __name__ == "__main__":
    request = get_request("M001")

    if request:
        print("Request:", request["request_id"])
        print("Resident:", request["resident_name"])
        print("Address:", request["address"])
        print("Apartment:", request["apartment"])
        print("Problem:", request["description"])
        print("Status:", request["status"])
    else:
        print("Request not found")

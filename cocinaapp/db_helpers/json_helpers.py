def get_indexed_json(json_data):
    """Returns the indexed json."""

    indexed_data = {}
    keys = [i["id"] for i in json_data]
    for i, j in enumerate(keys):
        indexed_data[j] = json_data[i]
    return indexed_data

def require_fields(
    data,
    fields
):

    if not data:

        return False

    return all(
        field in data
        for field in fields
    )

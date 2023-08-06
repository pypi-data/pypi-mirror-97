def find_term_match(values: list, term_id: str, default_val={}):
    """
    Return the element in a list which matches the `Term` with the given `@id`.

    Parameters
    ----------
    values
        The list in which to search for. Example: `cycle['inputs']`.
    term_id
        The `@id` of the `Term`. Example: `sandContent`
    default_val
        The returned value if no match was found.

    Returns
    -------
    dict
        The matching object.
    """
    return next((v for v in values if v.get('term', {}).get('@id') == term_id), default_val)


def find_primary_product(cycle: dict) -> dict:
    """
    Return the `Product` of a `Cycle` which is set to `primary`, `None` if none present.

    Parameters
    ----------
    cycle
        The JSON-LD of the `Cycle`.

    Returns
    -------
    dict
        The primary `Product`.
    """
    products = cycle.get('products', [])
    return next((p for p in products if p.get('primary', False)), products[0]) if len(products) > 0 else None

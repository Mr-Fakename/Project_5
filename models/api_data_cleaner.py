def make_readable(cleaned_data):
    """ Performs string formatting: proper capitalization, removal of unnecessary spaces,
        makes lists from keys with several values.
    """

    for product in cleaned_data:
        product["product_name_fr"] = product['product_name_fr'].title()
        product["nutriscore_grade"] = product["nutriscore_grade"].upper()

        product["brands"] = str(list(map(str.strip, product["brands"].title().split(','))))
        product["categories"] = ", ".join(map(str.strip, product["categories"].split(',')))
        product["stores"] = str(list(map(str.strip, product["stores"].title().split(','))))

    return cleaned_data

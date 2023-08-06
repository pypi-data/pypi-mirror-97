def normalize_vendor(vendor):
    """ Return a canonical name for a type of database. """
    if not vendor:
        return "db"  # should this ever happen?
    elif "sqlite" in vendor:
        return "sqlite"
    elif "postgres" in vendor or vendor == "psycopg2":
        return "postgres"
    else:
        return vendor

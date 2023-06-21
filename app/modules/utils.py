def compare_versions(version1: str, version2: str):
    """
    Compare two software version's removing "v char as prefix
    :param version1:
    :param version2:
    :return: -1 if version 1 is smaller than version 2, 1 if version 1 is greater than version 2, 0 if equal
    """

    # convert chars to lower case and remove "v" char
    clean_version1 = version1.lower().lstrip("v")
    clean_version2 = version2.lower().lstrip("v")

    if clean_version1 < clean_version2:
        return -1
    elif clean_version1 > clean_version2:
        return 1
    else:
        return 0

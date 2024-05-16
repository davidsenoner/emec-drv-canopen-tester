from collections import deque


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

    return (clean_version1 > clean_version2) - (clean_version1 < clean_version2)


class CurrentStatistics:
    """ Class to store current values and calculate statistics """

    def __init__(self, max_length: int):
        from statistics import mean, stdev, median

        assert max_length > 1, "max_length must be greater than 1"

        self.current_values = deque([0] * max_length, maxlen=max_length)
        self.max_length = max_length
        self.mean = mean
        self.stdev = stdev
        self.median = median

    def min(self):
        return min(self.current_values)

    def max(self):
        return max(self.current_values)

    def mean(self):
        return self.mean(self.current_values)

    def std_dev(self):
        return self.stdev(self.current_values)

    def median(self):
        return self.median(self.current_values)

    def add(self, value):
        self.current_values.append(value)

    def get_values(self):
        return self.current_values

    def reset(self):
        self.current_values = deque([0] * self.max_length, maxlen=self.max_length)

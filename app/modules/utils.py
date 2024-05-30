from collections import deque
import statistics


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

    def __init__(self, max_length: int, threshold: float = 0):

        assert max_length > 1, "max_length must be greater than 1"

        self.current_values = deque([0] * max_length, maxlen=max_length)
        self.max_length = max_length
        self.threshold = threshold

    def __repr__(self):
        return repr(self.current_values)

    def __iter__(self):
        return iter(self.current_values)

    def set_threshold(self, threshold):
        self.threshold = threshold

    def get_threshold(self):
        return self.threshold

    def is_below_threshold(self):
        return self.last() < self.threshold

    def is_above_threshold(self):
        return self.last() > self.threshold

    def values_above_threshold(self):
        count = 0
        for v in reversed(self.current_values):
            if v > self.threshold:
                count += 1
            else:
                break
        return count

    def min(self):
        return min(self.current_values)

    def max(self):
        return max(self.current_values)

    def mean(self):
        return statistics.mean(self.current_values)

    def std_dev(self):
        return statistics.stdev(self.current_values)

    def median(self):
        return statistics.median(self.current_values)

    def last(self):
        return self.current_values[-1]

    def first(self):
        return self.current_values[0]

    def add(self, value):
        self.current_values.append(value)

    def get_values(self):
        return self.current_values

    def reset(self):
        self.current_values = deque([0] * self.max_length, maxlen=self.max_length)

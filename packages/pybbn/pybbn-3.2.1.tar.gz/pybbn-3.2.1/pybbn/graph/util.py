from functools import lru_cache


class IdUtil(object):
    """
    ID util.
    """

    @staticmethod
    @lru_cache(maxsize=32768)
    def hash_string(s):
        """
        Hashes the string.

        :param s: String.
        :return: Hash value.
        """
        hash_value = 0

        if len(s) == 0:
            return hash_value

        for c in s:
            hash_value = ((hash_value << 5) - hash_value) + ord(c)
            hash_value |= 0

        return hash_value

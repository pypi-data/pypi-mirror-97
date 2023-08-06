def naiveExactMatch(pattern, string):
    """Perform a naive exact pattern search of `pattern` in `string`.

    :param str pattern: The pattern to be found in `string`.
    :param str string: The main string in which we look for the `pattern`.
    :return: The index of the first occurrence of `pattern` in `string`.
        If the `pattern` is not found, return -1.
    :rtype: int

    **Example Code**

    .. code:: python

        >> naiveExactMatch("abc", "ufkabcodp")
        3
    """

    for j in range(len(string) - len(pattern)+1):
        for i, p in enumerate(pattern):
            if p != string[j + i]:
                break
            if i >= len(pattern)-1:
                return j
    return -1

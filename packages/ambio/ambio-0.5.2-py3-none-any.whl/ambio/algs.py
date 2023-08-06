"""Features the most famous and useful algorithms used for
matching and analizing DNA sequences represented as strings.
"""


def hammingDistance(
    string1,
    string2
):
    """Calculates the Hamming distance between two strings.

    The Hamming distance between two strings of equal length is the number of positions
    at which the corresponding symbols are different. In other words, it measures 
    the minimum number of substitutions required to change one string into the other,
    or the minimum number of errors that could have transformed one string into the other.

    Learn more: `Hamming Distance [wikipedia] <https://en.wikipedia.org/wiki/Hamming_distance>`_

    :param str string1: The first string.
    :param str string2: The second string.

    :raises ValueError: The two strings are not the same length.

    :return: The Hamming distance between `string1` and `string2`.
    :rtype: int

    **Example code**

    .. code:: python

        >> hammingDistance("sunday", "sunray")
        1

        >> hammingDistance("hello", "world!")
        ValueError: "The two given strings are not the same length."
    """

    if len(string1) != len(string2):
        raise ValueError("The two given strings are not the same length.")

    dist = 0
    for i in range(len(string1)):
        if string1[i] != string2[i]:
            dist += 1

    return dist


def alignmentScoreTable(
        string1,
        string2,
        paths=False,
        insertionDeletionWeight=-2,
        substitutionWeight=-1,
        matchWeight=1
):
    """Generates the table of scores needed for finding the alignment score with the Needleman-Wunsch algorithm.

    Learn more: `Needleman-Wunsch Algorithm [wikipedia] <https://en.wikipedia.org/wiki/Needleman-Wunsch_algorithm>`_

    :param str string1: The first string to align.
    :param str string2: The second string to align.
    :param bool paths: When True the table used for backtracking is also returned.
    :param int insertionDeletionWeight: The cost of an insertion or deletion, default is -2.
    :param int substitutionWeight: The cost of a substitution, default is -1.
    :param int matchWeight: The profit of a matching character, default is 1.

    :return: A matrix containing the alignment scores, and 
        optionally another matrix with the origin cells.
    :rtype: list

    **Example code**

    .. code:: python

        >> scores, paths = alignmentScoreTable("home", "house", paths=True)
        >> scores
        [[ 0,  -2, -4, -6, -8],
         [-2,   1, -1, -3, -5],
         [-4,  -1,  2,  0, -2],
         [-6,  -3,  0,  1, -1],
         [-8,  -5, -2, -1,  0],
         [-10, -7, -4, -3,  0]]
        >> paths
        [[(-1,-1), (0, 0), (0, 1), (0, 2), (0, 3)],
         [ (0, 0), (0, 0), (1, 1), (1, 2), (1, 3)],
         [ (1, 0), (1, 1), (1, 1), (2, 2), (2, 3)],
         [ (2, 0), (2, 1), (2, 2), (2, 2), (3, 3)],
         [ (3, 0), (3, 1), (3, 2), (3, 3), (3, 3)],
         [ (4, 0), (4, 1), (4, 2), (4, 3), (4, 3)]]
    """

    tab = [[0 for i in range(len(string1) + 1)]
           for j in range(len(string2) + 1)]

    prevsTab = [[(-1, -1) for i in range(len(string1) + 1)]
                for j in range(len(string2) + 1)]

    string1 = "-" + string1
    string2 = "-" + string2

    for j in range(len(string2)):

        for i in range(len(string1)):

            choose = []
            prevs = []

            if j > 0:
                choose.append(tab[j-1][i] + insertionDeletionWeight)
                prevs.append((j-1, i))

            if i > 0:
                choose.append(tab[j][i-1] + insertionDeletionWeight)
                prevs.append((j, i-1))

            if j > 0 and i > 0:
                if string1[i] == string2[j]:
                    choose.append(tab[j-1][i-1] + matchWeight)
                else:
                    choose.append(tab[j-1][i-1] + substitutionWeight)
                prevs.append((j-1, i-1))

            if len(choose) > 0:
                tab[j][i] = max(choose)
                prevsTab[j][i] = prevs[choose.index(max(choose))]

    if paths:
        return tab, prevsTab
    else:
        return tab


def alignmentScore(
        string1,
        string2,
        insertionDeletionWeight=-2,
        substitutionWeight=-1,
        matchWeight=1
):
    """Calculate the alignment score of two given strings using the Needleman–Wunsch algorithm.

    The algorithm essentially divides a large problem (e.g. the full sequence) into a series of smaller problems, 
    and it uses the solutions to the smaller problems to find an optimal solution to the larger problem.

    Learn more: `Needleman-Wunsch Algorithm [wikipedia] <https://en.wikipedia.org/wiki/Needleman-Wunsch_algorithm>`_

    :param str string1: The first string to align.
    :param str string2: The second string to align.
    :param bool paths: When True the table used for backtracking is also returned.
    :param int insertionDeletionWeight: The cost of an insertion or deletion, default is -2.
    :param int substitutionWeight: The cost of a substitution, default is -1.
    :param int matchWeight: The profit of a matching character, default is 1.

    :return: A matrix containing the alignment scores, and 
        optionally another matrix with the origin cells.
    :rtype: list

    **Example code**

    .. code:: python

        >> alignmentScore("sunday", "sunray")
        4
    """

    table = alignmentScoreTable(
        string1, string2, False, insertionDeletionWeight, substitutionWeight, matchWeight)

    return table[-1][-1]


def showAlignment(
        string1,
        string2,
        insertionDeletionWeight=-2,
        substitutionWeight=-1,
        matchWeight=1
):
    """Returns a visual representation of the alignment of two given strings using the Needleman–Wunsch algorithm.

    Learn more: `Needleman-Wunsch Algorithm [wikipedia] <https://en.wikipedia.org/wiki/Needleman-Wunsch_algorithm>`_

    :param str string1: The first string to align.
    :param str string2: The second string to align.
    :param int insertionDeletionWeight: The cost of an insertion or deletion, default is -2.
    :param int substitutionWeight: The cost of a substitution, default is -1.
    :param int matchWeight: The profit of a matching character, default is 1.

    :return: A list containing the two strings modified to show 
        which edits have been made for them to be aligned.
    :rtype: list

    **Example code**

    .. code:: python

        >> al = showAlignment("sunday", "sunray")
        >> print(al[0] + "\\n" + al[1])
        s--unday
        saturday
    """

    _, track = alignmentScoreTable(
        string1, string2, True, insertionDeletionWeight, substitutionWeight, matchWeight)

    edited1 = edited2 = ""
    j = len(string2)
    i = len(string1)

    while i != 0 and j != 0:

        prev_j, prev_i = track[j][i]

        # diagonal move
        if prev_j == j-1 and prev_i == i-1:
            edited1 = string1[i-1] + edited1
            edited2 = string2[j-1] + edited2
        # vertical move
        elif prev_j == j-1:
            edited1 = "-" + edited1
            edited2 = string2[j-1] + edited2
        # horizontal move
        else:
            edited1 = string1[i-1] + edited1
            edited2 = "-" + edited2

        j = prev_j
        i = prev_i

    return [edited1, edited2]

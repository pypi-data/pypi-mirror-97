def hammingDistance(string1, string2):
    if len(string1) != len(string2):
        raise ValueError("The two given strings are not the same length.")

    dist = 0
    for i in range(len(string1)):
        if string1[i] != string2[i]:
            dist += 1

    return dist


def generateEditDistanceTable(string1, string2, paths=False):
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
                choose.append(tab[j-1][i] + 1)
                prevs.append((j-1, i))

            if i > 0:
                choose.append(tab[j][i-1] + 1)
                prevs.append((j, i-1))

            if j > 0 and i > 0:
                if string1[i] == string2[j]:
                    choose.append(tab[j-1][i-1])
                else:
                    choose.append(tab[j-1][i-1] + 1)
                prevs.append((j-1, i-1))

            if len(choose) > 0:
                tab[j][i] = min(choose)
                prevsTab[j][i] = prevs[choose.index(min(choose))]

    if paths:
        return tab, prevsTab
    else:
        return tab


def editDistance(string1, string2):

    tab = generateEditDistanceTable(string1, string2)

    return tab[-1][-1]


def displayEdits(string1, string2, compact=True):

    _, previousCell = generateEditDistanceTable(string1, string2, paths=True)

    if compact:
        edited1 = edited2 = ""
        j = len(string2)
        i = len(string1)

        while i != 0 and j != 0:

            prev_j, prev_i = previousCell[j][i]

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
    else:
        steps = [string2]
        j = len(string2)
        i = len(string1)

        while i != 0 and j != 0:

            prev_j, prev_i = previousCell[j][i]

            # diagonal move
            if prev_j == j-1 and prev_i == i-1:
                # character substitution
                if string1[i-1] != string2[j-1]:
                    temp = steps[-1]
                    t = list(temp)
                    t[j-1] = string1[i-1]
                    temp = "".join(t)
                    steps.append(temp)

            # vertical move
            elif prev_j == j-1:
                # character deletion
                temp = steps[-1][:j-1] + steps[-1][j:]
                steps.append(temp)

            # horizontal move
            else:
                # character insertion
                temp = steps[-1][:j] + string1[i-1] + steps[-1][j:]
                steps.append(temp)

            j = prev_j
            i = prev_i

        steps.reverse()
        return steps

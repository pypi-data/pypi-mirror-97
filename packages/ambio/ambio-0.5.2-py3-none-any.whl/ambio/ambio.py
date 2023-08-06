def generateEditDistanceTable(string1, string2):
    tab = [[0 for i in range(len(string1) + 1)]
           for j in range(len(string2) + 1)]

    string1 = "-" + string1
    string2 = "-" + string2

    for j in range(len(string2)):

        for i in range(len(string1)):

            choose = []

            if j > 0:
                choose.append(tab[j-1][i] + 1)

            if i > 0:
                choose.append(tab[j][i-1] + 1)

            if j > 0 and i > 0:
                if string1[i] == string2[j]:
                    choose.append(tab[j-1][i-1])
                else:
                    choose.append(tab[j-1][i-1] + 1)

            if len(choose) > 0:
                tab[j][i] = min(choose)

    return tab


def editDistance(string1, string2):

    tab = generateEditDistanceTable(string1, string2)

    return tab[-1][-1]

class EditDistance:
    """
    A class used to group all the functions regarding the Edit Distance between two strings

    Methods
    -------
    getStrings()
        Returns the two string attributes in a list

    getDistance()
        Returns the Edit Distance between the two string attributes

    getTable()
        Returns the table with the Edit distances between all the possible substrings of the two attributes 
    """

    def __init__(self, S, T):
        self.__string1 = S
        self.__string2 = T
        self.__tab = []

    def __genTable(self):
        self.__tab = [[0 for i in range(len(self.__string1) + 1)]
                      for j in range(len(self.__string2) + 1)]

        self.__string1 = "-" + self.__string1
        self.__string2 = "-" + self.__string2

        for j in range(len(self.__string2)):

            for i in range(len(self.__string1)):

                choose = []

                if j > 0:
                    choose.append(self.__tab[j-1][i] + 1)

                if i > 0:
                    choose.append(self.__tab[j][i-1] + 1)

                if j > 0 and i > 0:
                    if self.__string1[i] == self.__string2[j]:
                        choose.append(self.__tab[j-1][i-1])
                    else:
                        choose.append(self.__tab[j-1][i-1] + 1)

                if len(choose) > 0:
                    self.__tab[j][i] = min(choose)

    def getStrings(self):
        """Returns the two string attributes in a list

        :returns: a list with the two string attributes
        :rtype: list
        """

        return [self.__string1, self.__string2]

    def getDistance(self):
        """Returns the Edit Distance between the two string attributes

        :returns: the edit distance between the two strings attributes
        :rtype: int
        """

        if len(self.__tab) == 0:
            self.__genTable()

        return self.__tab[-1][-1]

    def getTable(self):
        """Returns the table with the Edit distances between all the possible substrings of the two string attributes

        :returns: the table with the Edit distances between all the possible substrings
        :rtype: list
        """

        if len(self.__tab) == 0:
            self.__genTable()

        return self.__tab

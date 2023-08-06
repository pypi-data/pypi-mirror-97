from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


class ContentBased:

    def __init__(self, lang="english"):

        self.lang = lang
        self.similarity_score = []
        self.data = []

    def predict(self, x=[], title=0, count=1):
        """
        fit value and calculating value
        """
        # remove punctuation
        data = x
        data.append(data[title])

        # create sparse matrics
        free_sw = self.__vectorizer(data)

        # calculate similarity
        similarity = []

        for i in range(0, len(data)):
            similarity.append(self._cosine_similarity(
                free_sw[len(free_sw) - 1], free_sw[i]))

        # get recommendation data
        recommend = self.__recommended(similarity, data, count)

        return recommend

    def __vectorizer(self, data=[]):
        """
        removing stopwords
        """

        # change text to Tf - Idf format
        vectorizer = TfidfVectorizer()
        vector = vectorizer.fit_transform(data)

        return vector.toarray()

    def __recommended(self, matrix=[], data=[], count=0):
        """
        find recommendation based on similarity matrix
        """
        init_matrix = matrix

        copy_matrix = []

        for mat in init_matrix:
            copy_matrix.append(mat)

        # sorting array from the biggest to lower
        copy_matrix.sort(reverse=True)
        copy_matrix = copy_matrix[1:count + 1]

        # set similarity score to global properties
        self.similarity_score = copy_matrix

        # get recommendation
        result = []
        for i in copy_matrix:
            result.append(init_matrix.index(i))

        return result[1:len(result)]

    # math section

    def _cosine_similarity(self, x=[], y=[]):
        """
        calculate similarity
        """
        a = np.array(x)
        b = np.array(y)

        # cosine similarity
        calc = np.sum(a * b) / (np.sqrt(np.sum(a**2)) * np.sqrt(np.sum(b**2)))

        # euclidean norm
        smoothing = np.sqrt(calc**2)

        return smoothing

    def score(self):
        """
        return similarity score
        """
        return self.similarity_score

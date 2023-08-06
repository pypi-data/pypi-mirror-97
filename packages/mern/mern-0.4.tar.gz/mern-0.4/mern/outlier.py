from nltk.corpus import stopwords
import string
import numpy as np

class NumericOutlier:

    def _zscore(self, data = []):
        """
        remove outlier with z - score fomula
        (x - mean) / standard deviation
        """

        mean = np.mean(data)
        std = np.std(data)
        result = []
        
        # calculate z - score
        for i in range(0, len(data)):
            calculation = (data[i] - mean) / std
            if calculation > 2 or calculation < -2:
                result.append(data[i])
            
        return result

    def _iqr(self, data = []):
        """
        remove outlier with Interquartile Range Score
        iqr = Q3 - Q1
        min = Q1 - (1.5 * iqr)
        max = Q3 + (1.5 * iqr)
        """
        # sorting data

        x = data
        x.sort()

        # find Q1, Q2 and Q3

        q2 = np.median(x)
        q1 = np.median([x[i] for i in range(0, round(len(x) / 2) - 1)])
        q3 = np.median([x[i] for i in range(round(len(x) / 2), len(x))])

        # iqr
        iqr = q3 - q1

        # find outlier
        min_data = q1 - (1.5 * iqr)
        max_data = q1 + (1.5 * iqr)
        result = []

        for n in x:
            if n < min_data or n > max_data:
                result.append(n)
        
        return result

    def find(self, x = [], method=None):
        """
        remove outlier
        it take list parameter and method (zscore, iqr score)
        """
        if method != None:
            if method.lower() == "zscore":
                return self._zscore(x)
            else:
                return self._iqr(x)
        else:
            return ["Please tell me what kind of method do you want ? (zsocre, iqr)"]


class TextOutlier:

    def remove_punctuation(self, data=[]):
        """
        remove punctuation
        """
        clean_text = []

        for text in data:
            try:
                sentences = text.lower()
                for c in string.punctuation:
                    sentences = sentences.replace(c, "")
                clean_text.append(sentences)
            except:
                pass
        return clean_text

    def remove_stopwords(self, data=[], lang="english"):
        """
        removing stop words ex: The, is, a
        """
        clean_text = []
        # remove stop words

        for text in data:
            sentences = text.lower().split()
            free_sw = []
            result = ''
            for sw in sentences:
                if sw not in stopwords.words(lang):
                    free_sw.append(sw)

            # merge words
            for words in free_sw:
                result += words + " "
            result = result[0:len(result) - 1]

            clean_text.append(result)

        return clean_text

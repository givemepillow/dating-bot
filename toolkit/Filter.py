from toolkit.replacement import repl


class Filter():
    with open('bad_words.txt', 'r', encoding='utf-8') as file:
        bad_words = list(map(str.rstrip, file.readlines()))

    def __init__(self, bio):
        self.bio = bio

    @classmethod
    def _replace(self, bio):
        bio = bio.lower().replace(" ", "")
        for key, value in repl.items():
            for letter in value:
                for phr in bio:
                    if letter == phr:
                        bio = bio.replace(phr, key)

    @classmethod
    def _distance(self, a, b):
        "Calculates the Levenshtein distance between a and b."
        n, m = len(a), len(b)
        if n > m:
            a, b = b, a
            n, m = m, n

        current_row = range(n + 1)
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
                if a[j - 1] != b[i - 1]:
                    change += 1
                current_row[j] = min(add, delete, change)

        return current_row[n]

    @classmethod
    def check(self, text):
        self._replace(text)
        for part in range(len(text)):
            for word in self.bad_words:
                fragment = text[part: part + len(word)]
                if self._distance(fragment, word) <= len(word) * 0.25:
                    return word

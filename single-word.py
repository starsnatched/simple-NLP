"""Fast Levenshtein distance NLP algorithm for a single word autocorrection.
Returns 3 most probable words(suggestions) for the input from the NLTK word corpus.
Un-document line 9(nltk.download()) if you haven't downloaded NLTK word corpus already.

`pip install nltk` is required."""

import nltk

# nltk.download('words')
from nltk.corpus import words

class AutoCorrector:
    def __init__(self, word_list):
        self.word_list = word_list

    def levenshtein_distance(self, s1, s2):
        if len(s1) < len(s2):
            return self.levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)

        for i, c1 in enumerate(s1):
            current_row = [i + 1]

            for j, c2 in enumerate(s2):
                insert_cost = previous_row[j + 1] + 1
                delete_cost = current_row[j] + 1
                replace_cost = previous_row[j] + (c1 != c2)

                current_row.append(min(insert_cost, delete_cost, replace_cost))

            previous_row = current_row

        return previous_row[-1]

    def suggest_correction(self, input_word, num_suggestions=3):
        suggestions = []

        for word in self.word_list:
            distance = self.levenshtein_distance(input_word, word)
            similarity = 1 - distance / max(len(input_word), len(word))

            if similarity > 0.7:    # adjust this threshold. lower(e.g. 0.2) means it will return even if the suggestion is not similar enough.
                suggestions.append((word, similarity))

        if suggestions:
            suggestions.sort(key=lambda x: x[1], reverse=True)
            return [suggestion[0] for suggestion in suggestions[:num_suggestions]]
        else:
            return ["No suggestion"]

word_list = words.words()
auto_corrector = AutoCorrector(word_list)

input_word = "whtevr"   # change this to your desired input.
results = auto_corrector.suggest_correction(input_word, num_suggestions=3)

for result in results:
    print(result)
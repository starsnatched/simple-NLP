"""Extremely fast suggestive text feature.
Edit 'corpus.txt' with a book corpus to make the NLP model more robust.

'corpus.txt' is directly copied from the book "To kill a Mockingbird"."""

from collections import defaultdict

class SuggestiveTextModel:
    def __init__(self, n):
        self.n = n
        self.ngrams = defaultdict(list)

    def train(self, text):
        words = text.split()
        for i in range(len(words) - self.n):
            prefix = tuple(words[i:i + self.n])
            self.ngrams[prefix].append(words[i + self.n])

    def generate_text(self, seed, length=10):
        current_prefix = tuple(seed.split()[-self.n:])
        generated_text = list(current_prefix)

        for _ in range(length):
            next_word_options = self.ngrams[current_prefix]
            # print(next_word_options)
            
            if not next_word_options:
                break

            next_word = ", ".join(next_word_options[:3])
            generated_text.append(next_word)
            current_prefix = tuple(generated_text[-self.n:])

        return ' '.join(generated_text)

while True:
    seed_text = input(">> ").replace("\n", " ").lower()

    seed_split = seed_text.split(" ")
    if len(seed_split) > 5:
        model = SuggestiveTextModel(n=5)
    else:
        model = SuggestiveTextModel(n=len(seed_split))

    with open('corpus.txt', 'r', encoding='utf-8') as corpus:
        training_data = corpus.read().replace("\n", " ").lower()

    model.train(training_data)

    generated_text = model.generate_text(seed_text, length=1).replace(seed_text, "").strip()
    print(generated_text)

    # with open('corpus.txt', 'a', encoding='utf-8') as corpus:
    #     corpus.write(seed_text.strip() + "\n")
'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 18, 2015.

This version is a direct solution to the nifty assignment, and does exactly what the nifty assignment says on the tin.

'''

import math


# see: http://nifty.stanford.edu/2017/guerzhoy-SAT-synonyms/
# http://nifty.stanford.edu/2017/guerzhoy-SAT-synonyms/2015/p3_synonyms.pdf


def norm(vec) -> float:
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    Norm is defined as
    '''

    sum_of_squares = 0.0  # floating point to handle large numbers
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2) -> float:
    """Get the similarity between two vectors"""
    numerator = dot(vec1, vec2)
    denominator = norm(vec1) * norm(vec2)

    return numerator / denominator


def dot(vec1, vec2) -> int:
    output = 0
    # We only really need to search through a single time
    # Anything that doesn't match first time thru doesn't matter second time thru
    for key in vec1:
        try:
            output += vec1[key] * vec2[key]
        except KeyError:
            pass

    return output


def magnitude(vec: dict) -> int:
    return sum([i ** 2 for i in vec.values()])


def build_semantic_descriptors(sentences: list) -> dict:
    """
    Build semantic descriptors for every word that exists in the texts.
    Iterates over every word in the text and makes note of every other word that also appears in sentences shared
    with the initial word.
    """
    semantic_desc = {}

    for sentence in sentences:
        for active_word in sentence:
            # Try to find if we have a record for the current
            active_desc = semantic_desc.get(active_word, {})
            for word in sentence:
                if word == active_word:
                    continue
                try:
                    active_desc[word] += 1
                except KeyError:
                    active_desc[word] = 1

            semantic_desc[active_word] = active_desc

    return semantic_desc


def clean_and_split(text, separators) -> list:
    """Replace all separators with the first and then split on the first"""

    cleaned_text = text
    cleaned_text = cleaned_text.replace("-\n", "")
    cleaned_text = cleaned_text.replace("\n", " ")
    for sep in separators:
        cleaned_text = cleaned_text.replace(sep, separators[0])
    return cleaned_text.split(separators[0])


def build_semantic_descriptors_from_files(filenames: list) -> dict:
    """Generate vectors that hold all of the contextual words"""

    all_sentences = []

    for filename in filenames:
        with open(filename, "r", encoding="utf-8") as g:
            # Load the file and create a list of sentences from it
            file_text = g.read()

            # Just replace sentence swap punctuation with a single mark so we only have to split once.
            sentences = clean_and_split(file_text, "?.!")

            cleaned_sentences = []
            for sentence in sentences:
                cleaned = clean_and_split(sentence, [" ", ',', '--', '-', ':', ';', '"', "'"])
                cleaned_words = [w.lower() for w in cleaned if w != ""]  # Make all words lowercase and remove empty
                cleaned_sentences.append(cleaned_words)  # Append the list itself

            # print(cleaned_sentences)

            all_sentences += cleaned_sentences

    print("descriptors built")

    return build_semantic_descriptors(all_sentences)


def most_similar_word(word: str, choices: str, semantic_descriptors: dict, similarity_fn) -> tuple:
    """Return the word from choices that is most likely a synonym of `word`."""
    unmatched_choices = []
    similarity_values = {}
    choice_descriptors = {}
    if word not in semantic_descriptors:
        # It's kind of an issue if we have never seen what this word is
        # We'll just make a random guess and take note
        print("Can't find context for this word {}. No guesses possible.".format(word))
        print(word, choices)
        print("*" * 30)

        return choices[0], 0
    else:
        target_word_desc = semantic_descriptors[word]
    # Build tuple with choice, descriptor

    for choice in choices:
        try:
            choice_descriptors[choice] = semantic_descriptors[choice]
        except KeyError:
            # If we don't have context data for this one, let's just skip it
            unmatched_choices.append(choice)

    for choice, desc in choice_descriptors.items():
        if choice in unmatched_choices:
            # The value is basically ignored as we do a later comparison
            similarity_values[choice] = -1
        else:
            similarity_values[choice] = similarity_fn(target_word_desc, desc)

    best_match = ("", 0)
    for choice, similarity in similarity_values.items():
        # Determine the best match
        if similarity > best_match[1]:
            best_match = (choice, similarity)
        elif similarity == best_match[1] and choices.index(choice) < choices.index(best_match[0]):
            # If it matches similarity, we want the one with the smaller index
            best_match = (choice, similarity)

    return best_match


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    words_run = 0
    words_correct = 0

    with open(filename) as f:
        for line in f.readlines():
            # python 3 woo
            first_word, correct_answer, *options = line.split()
            closest_match = most_similar_word(first_word, options, semantic_descriptors, similarity_fn)
            if closest_match[0] == correct_answer:
                words_correct += 1
            words_run += 1
            print("Target: {}\nChoices: {}\nBest Match: {}".format(first_word, options, closest_match))
            print(closest_match[0] == correct_answer)
            print("*" * 30)
    return words_correct / words_run


if __name__ == '__main__':
    descriptors = build_semantic_descriptors_from_files(["swans_way.txt", "test_book_2.txt"])

    print("Accuracy:", run_similarity_test("test.txt", descriptors, cosine_similarity))

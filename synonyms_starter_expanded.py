'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 18, 2015.

---

Implemented by Matthew Thompson Dec. 6 2017

This is based off of the nifty assignment.

This version runs through and prints the words that most closely match the word, based on its proximity.
'''

import synonym_starter_base as syn


def get_synonyms(word, semantic_descriptors, similarity_fn, max_words_matched=50, sim_threshold=0.75) -> (dict, None):
    similar_words = {}
    try:
        target_word_desc = semantic_descriptors[word]
    except KeyError:
        print("No descriptor exists for this word.")
        return

    for w, desc in semantic_descriptors.items():
        try:
            similarity = similarity_fn(target_word_desc, desc)
        except ZeroDivisionError:  # if the norm of one value is zero; can't be calculated
            similarity = -1
        if similarity > sim_threshold and word != w:
            similar_words[w] = similarity
            if 0 < max_words_matched < len(similar_words):
                break

    return sorted(similar_words.items(), key=lambda t: t[1], reverse=True)  # sort the output words


if __name__ == '__main__':

    example_sentences = [['i', 'am', 'a', 'sick', 'man'],
                         ['i', 'am', 'a', 'spiteful', 'man'],
                         ['i', 'am', 'an', 'unattractive', 'man'],
                         ['i', 'believe', 'my', 'liver', 'is', 'diseased'],
                         ['however', 'i', 'know', 'nothing', 'at', 'all', 'about', 'my',
                          'disease', 'and', 'do', 'not', 'know', 'for', 'certain', 'what', 'ails', 'me']]
    print(syn.build_semantic_descriptors(example_sentences))

    descriptors = syn.build_semantic_descriptors_from_files(["swans_way.txt", "test_book_2.txt"])

    # print("Accuracy:", run_similarity_test("test.txt", descriptors, cosine_similarity))
    while True:
        word = input("Most common context for which word? ").lower()
        print(get_synonyms(word, descriptors, syn.cosine_similarity, max_words_matched=-1))
        print()
    # closest_match = most_similar_word(word, list(descriptors.keys()), descriptors, cosine_similarity)

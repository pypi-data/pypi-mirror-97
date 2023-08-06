import itertools
import re
import sys


def build_index(pdf_document):

    print("\nBUILDING INDEX\n...")

    inv_index = []

    # Preprocesses and indexes collection per document.

    for paragraph in pdf_document.paragraphs.paragraphs:
        docnumber = paragraph.number

        text = paragraph.Text

        text.replace('\n', '')
        tokenizedline = re.split('[\W]', text)

        processed_text = [w.lower() for w in tokenizedline]

        # Builds an index for each document then appends each to a large index for full collection

        indexes_per_document = []

        for word in processed_text:
            word_occurrences = {}
            term_obj = {}
            positions = [i+1 for i, x in enumerate(processed_text) if x == word] # All positions of a word per document
            word_occurrences[docnumber] = positions     # Dictionary for {document:[list of positions in doc]}
            term_obj[word] = word_occurrences           # Dictionary for {term: {document: [list of positions in doc]}}
            if term_obj not in indexes_per_document:
                indexes_per_document.append(term_obj)
        inv_index.append(indexes_per_document)

    # Sort and group inverted index by word

    inv_index = list(itertools.chain.from_iterable(inv_index))
    inv_index.sort(key=lambda d: sorted(d.keys()))
    inv_index = itertools.groupby(inv_index, key=lambda x: sorted(x.keys()))


    inv_index_json={}

    for word, positions in inv_index:
        string_word = "{}".format(''.join(word))
        if string_word not in inv_index_json:
            inv_index_json[string_word]={}
        list_positions = []
        for x in list(positions):
            for key, v in x.items():
                list_positions.append(v)
        for item in list_positions:
            for doc, pos in item.items():
                inv_index_json[string_word][doc]=pos


    print("INDEXING COMPLETE\n")
    return inv_index_json

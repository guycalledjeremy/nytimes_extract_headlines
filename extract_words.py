""" Docstring for this file.
"""

import argparse
import json
import _pickle as pickle
import os


def setup_words(data, filepath):
    """
    """
    print("Getting all words list...")
    allWords = []
    for year in range(len(data)):
        print("setup_words - processing year "+str(1900+year)+"...")
        for article in data[year]:
            word_list = article["headline"].split()
            for tagged_word in word_list:
                if "/NN" in tagged_word:
                    word = tagged_word[:tagged_word.find("/")]
                    if word not in allWords:
                        allWords.append(word)

    print("Maintained the all words list.")
    with open(filepath, 'wb') as handle:
        pickle.dump(allWords, handle)
    print("All words list saved.")

    return allWords


def main(args):
    """
    """
    allOutput = {}
    # Load the extracted data from the input file
    data = json.load(open(args.input))
    print("Data extracted...")

    # Get all nouns ever existed in headlines
    word_list_filename = args.output_w[:args.output_w.find(".")] + '.pickle'
    if os.path.isfile(word_list_filename) and os.path.getsize(word_list_filename) > 0:
        with open(word_list_filename, 'rb') as f:
            allWords = pickle.load(f)
            print("Words list extracted from pickle file...")
    else:
        allWords = setup_words(data, word_list_filename)
    for word in allWords:
        allOutput[word] = []

    year_word_count = []
    for year in range(len(data)):
        year_word_count.append(0)
        print("frequency count - processing year "+str(1900+year)+"...")
        for word in allWords:
            allOutput[word].append(0)
        print("Initialised...")
        for article in data[year]:
            word_list = article["headline"].split()
            for tagged_word in word_list:
                if "/NN" in tagged_word:
                    year_word_count[-1] += 1
                    word = tagged_word[:tagged_word.find("/")]
                    if word in allWords:
                        allOutput[word][year] += 1

    # Normalise all word counts
    for year in range(len(data)):
        for word in allOutput.keys():
            year_count = allOutput[word][year]
            allOutput[word][year] = year_count / year_word_count[year]

    f_out = open(args.output_o, 'w')
    f_out.write(json.dumps(allOutput))
    f_out.close()
    print("Word frequency count JSON file created...")
    w_out = open(args.output_w, 'w')
    w_out.write(json.dumps(allWords))
    w_out.close()
    print("Word list JSON file created...")
    print("Number of nouns collected in total: "+str(len(allWords))+".")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process each .')
    parser.add_argument("-i", "--input", help="the input json file containing \
    headlines", required=True)
    parser.add_argument("-o", "--output_o", help="Directs the outputed  to a \
    filename of your choice", required=True)
    parser.add_argument("-w", "--output_w", help="Directs the outputed topics to a \
    filename of your choice", required=True)
    args = parser.parse_args()

    print("Word Extraction Started...")
    main(args)
    print("Word Extraction Finished.")

"""
    This file takes in the normalised frequency as well as words in the technology subject
obtained from Oxford English Dictionary, and return a histogram reporting cpd for each
decade.

Output:
    - args.output_o(JSON file): this JSON file contains a list of list, with each list containing
info(dict, {word: (year, mse)}) about words whose change point is within the decade.
    - args.output_csv(CSV file): this CSV file contains a table representing the number of tech
words whose change point was detected within that decade.
"""

import argparse
import json
import csv
from changepoint_detection import cpd


def main(args):
    """
    """
    # Load the extracted data from the input file
    data = json.load(open(args.input))
    all_words = list(data.keys())
    print("Data extracted...")

    # Load the tech words from OED
    oed_words_filepath = "oed_keywords.json"
    oed_words_dict = json.load(open(oed_words_filepath))
    oed_words_list = list(oed_words_dict.keys())

    # Filter words OED that are not in any headline
    selected_words_list = []
    selected_data = {}
    for original_word in oed_words_list:
        # Many of the words from OED, unlike the words from headlines, are not processed
        word = original_word.lower()
        if word in all_words:
            selected_words_list.append(word)
            selected_data[word] = data[word]
    print("Total number of words extracted from OED: "+str(len(oed_words_list)))
    print("Total number of words selected: "+str(len(selected_words_list)))

    # Perform cpd on all the selected words
    allOutput_json = []
    for i in range(10):
        allOutput_json.append([])
    for word in selected_words_list:
        year, ems = cpd(data[word])
        decade = int(str(year)[2])
        allOutput_json[decade].append({word: (year, ems)})

    f_out = open(args.output_o, 'w')
    f_out.write(json.dumps(allOutput_json))
    f_out.close()
    print("Word cpd data JSON file created...")

    # Get the CSV file
    allOutput_csv = [["year", "Data"]]
    for i in range(10):
        allOutput_csv.append([1900+i*10])
    for year in range(len(allOutput_json)):
        allOutput_csv[year+1].append(len(allOutput_json[year]))

    # Create the output word frequency count csv file
    with open(args.output_csv, 'w') as file:
        writer = csv.writer(file)
        writer.writerows(allOutput_csv)
    print("Histogram CSV file created...")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process each .')
    parser.add_argument("-i", "--input", help="the input json file containing \
    headlines", required=True)
    parser.add_argument("-o", "--output_o", help="Directs the outputed  to a \
    filename of your choice", required=True)
    parser.add_argument("-c", "--output_csv", help="Directs the outputed  to a \
    filename of your choice", required=True)
    args = parser.parse_args()

    print("Words Generation Started...")
    main(args)
    print("Words Generation Finished.")

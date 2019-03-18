""" Docstring for this file.
"""

import argparse
import json
import csv
import re
import numpy as np

experiment_list = ['click', 'google', 'tape', 'catfish', 'follow', 'cloud',
                   'footprint', 'profile', 'tweet', 'bug', 'cookie',  'server',
                   'spam', 'apple/NNP', 'uber/NNP', 'amazon/NNP']

topics_dict = {}
for term in experiment_list:
    topics_dict[term] = []


def freq_count(headline, array):
    """ Describe this function
    """
    for i in range(len(experiment_list)):
        array[i] += len(re.findall(experiment_list[i], headline))

    return array


def topic_update(headline, keywards):
    """ Describe this function
    """
    # Get the topics for headline word each year
    for term in experiment_list:
        if len(re.findall(term, headline)) > 0:
            for item in keywards:
                if item["name"] == "subject" and item["value"] not in topics_dict[term][-1]:
                    topics_dict[term][-1].append(item["value"])


def main(args):
    """ Describe this function
    """
    allOutput = []
    finished = False
    print("Processing " + args.input + "...")
    allData = json.load(open(args.input))

    for year in range(len(allData)):
        for term in experiment_list:
            topics_dict[term].append([])
        # Initialise frequency array for each year
        freq_array = np.linspace(0, 0, num=len(experiment_list))
        for data in allData[year]:
            # Get word count for each headline
            freq_array = freq_count(data["headline"], freq_array)
            # Update topics for each headline
            topic_update(data["headline"], data["keywords"])
        allOutput.append(freq_array)
        print("Year " + str(1900 + year) + " Finished.")
    finished = True

    if finished:
        # Create the output word frequency count csv file
        with open(args.output_o, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(allOutput)
        print("Word frequency csv file created...")
        # Create the ouput dictionary of topic words json file
        fout = open(args.output_t, 'w')
        fout.write(json.dumps(topics_dict))
        fout.close()
        print("Topics JSON file created.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process each .')
    parser.add_argument("-i", "--input", help="the input json file containing \
    headlines", required=True)
    parser.add_argument("-o", "--output_o", help="Directs the output to a \
    filename of your choice (for frequency count)", required=True)
    parser.add_argument("-t", "--output_t", help="Directs the output to a \
    filename of your choice (for topics)", required=True)
    args = parser.parse_args()

    print("Frequency Count Started...")
    main(args)
    print("Frequency Count Finished.")

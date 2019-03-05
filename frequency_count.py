""" Docstring for this file.
"""

import argparse
import json
import csv
import re
import numpy as np

experiment_list = ['click', 'google', 'tape', 'catfish', 'follow', 'cloud',
                   'footprint', 'profile', 'tweet', 'bug', 'cookie',  'server',
                   'spam', 'apple/NNP', 'uber', 'amazon/NNP']


def freq_count(headline, array):
    """ Describe this function
    """
    for i in range(len(experiment_list)):
        array[i] += len(re.findall(experiment_list[i], headline))

    return array


def main(args):
    """ Describe this function
    """
    allOutput = []
    finished = False
    print("Processing " + args.input + "...")
    allData = json.load(open(args.input))

    for year in range(len(allData)):
        # Initialise frequency array for each year
        freq_array = np.linspace(0, 0, num=len(experiment_list))
        for data in allData[year]:
            freq_array = freq_count(data["headline"], freq_array)
        allOutput.append(freq_array)
        print("Year " + str(1900 + year) + " Finished.")
    finished = True

    if finished:
        # Create the output word frequency count csv file
        with open(args.output, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(allOutput)
        print("Word frequency csv file created...")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process each .')
    parser.add_argument("-i", "--input", help="the input json file containing \
    headlines", required=True)
    parser.add_argument("-o", "--output", help="Directs the output to a \
    filename of your choice", required=True)
    args = parser.parse_args()

    print("Frequency Count Started...")
    main(args)
    print("Frequency Count Finished.")

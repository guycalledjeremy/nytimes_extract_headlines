""" Docstring for this file.
"""

import argparse
import json
import csv
import numpy as np
from sklearn.metrics import mean_squared_error


def get_freq_diff(words_freq):
    """
    """
    output_dict = {}
    for word in words_freq.keys():
        output_dict[word] = []
        for i in range(len(words_freq[word])-1):
            output_dict[word].append((words_freq[word][i+1]-words_freq[word][i]) * 100)

    return output_dict


def get_sig_words(data_dict, freq_diff):
    """
    """
    all_data_dict = {}
    for word in data_dict.keys():
        sum_pre_80 = 0
        sum_post_80 = 0
        for i in range(len(data_dict[word])):
            if i < 79:
                sum_pre_80 += data_dict[word][i]
            else:
                sum_post_80 += data_dict[word][i]
        # Check if ...
        avg = sum_pre_80 / 80
        if sum_pre_80 < 0:
            break

        # sorted_freq = freq_diff[word]
        # sorted_freq.sort()
        # See how many time points for this word meet our criteria
        count = 0
        for n in data_dict[word]:
            if n > avg * 5 and data_dict[word].index(n) >= 69 and sum_pre_80 > 0:
                count += 1
        # Group all words based on how well they fit our criteria
        if count not in all_data_dict.keys():
            all_data_dict[count] = []
        all_data_dict[count].append(word)

    # Only take the top 20 for eyeballing
    filtered_output = {}
    desired_num = 10
    count_list = list(all_data_dict.keys())
    count_list.sort(reverse=True)
    # TODO
    print(all_data_dict[count_list[-1]])
    print(len(all_data_dict[count_list[-1]]))
    print(count_list)
    #for count_num in count_list:
    #    if desired_num > 0:
    #        for word in all_data_dict[count_num]:
    #            if desired_num > 0:
    #                filtered_output[word] = data_dict[word]
    #                desired_num -= 1
    #            else:
    #                break
    #    else:
    #        break

    # TODO
    for i in range(len(count_list)):
        if desired_num > 0:
            for word in all_data_dict[count_list[(i+1)*-1]]:
                if desired_num > 0:
                    filtered_output[word] = data_dict[word]
                    desired_num -= 1
                else:
                    break
        else:
            break

    return filtered_output

def cpd(freq_count):
    """
    :param freq_count: the frequency of a word from 1900-2000
    :type freq_count: list of int
    :return: cp_year, the changepoint year
    :rtype: int
    """
    years = np.arange(0, 101, 1)
    mse = []
    for i in years:
        fit = np.polyfit(years[i:], profile[i:], 2)
        linefit = np.poly1d(fit)
        y_fit = np.zeros(i)
        y_fit = np.concatenate((y_fit, linefit(years[i:])), axis=0)
        mse.append(mean_squared_error(profile, y_fit))
    min_mse = mse.index(min(mse))
    if min_mse == 100:
        cp_year = 2000
    else:
        cp_year = 1900 + min_mse
    return cp_year


def main(args):
    """
    """
    # Load the extracted data from the input file
    data = json.load(open(args.input))
    all_words = list(data.keys())
    print("Data extracted...")

    oed_words_filepath = "oed_keywords.json"
    oed_words_dict = json.load(open(oed_words_filepath))
    oed_words_list = list(oed_words_dict.keys())
    selected_words_list = []
    selected_data = {}
    for original_word in oed_words_list:
        word = original_word.lower()
        if word in all_words:
            selected_words_list.append(word)
            selected_data[word] = data[word]
    print("Total number of words extracted from OED: "+str(len(oed_words_list)))
    print("Total number of words selected: "+str(len(selected_words_list)))

    freq_diff_dict = get_freq_diff(selected_data)
    print("Normalised frequency difference obtained...")

    allOutput = get_sig_words(selected_data, freq_diff_dict)
    print("Selected "+str(len(allOutput.keys()))+" words.")

    f_out = open(args.output_o, 'w')
    f_out.write(json.dumps(allOutput))
    f_out.close()
    print("Word frequency count JSON file created...")

    # Create a csv file as well
    csvOutput = [[("year", "word")]]
    allWords = list(allOutput.keys())
    # Write the first row
    for word in allWords:
        csvOutput[0].append(word)
    # Initialise all the other rows
    for i in range(100):
        csvOutput.append([1901+i])
        # Update the csv file
        for word in allWords:
            csvOutput[-1].append(data[word][i])

    # Create the output word frequency count csv file
    with open(args.output_csv, 'w') as file:
        writer = csv.writer(file)
        writer.writerows(csvOutput)
    print("Filtered words frequency csv file created...")


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

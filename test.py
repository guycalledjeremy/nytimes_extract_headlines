
import json
import csv

experiment_list = ['tape', 'profile', 'cookie', 'apple', 'virus', 'stream', 'avatar', 'windows', 'computer', 'cyber', 'mouse']


if __name__ == "__main__":
    allOutput = {}
    data = json.load(open("word_freq_trend.json"))
    for word in experiment_list:
        if word in data.keys():
            allOutput[word] = []
            for i in data[word]:
                allOutput[word].append(i*100)

    csvOutput = [[("year", "word")]]
    # Write the first row
    for word in experiment_list:
        csvOutput[0].append(word)
    # Initialise all the other rows
    for i in range(100):
        csvOutput.append([1900+i])
        # Update the csv file
        for word in experiment_list:
            csvOutput[-1].append(allOutput[word][i])

    # Create the output word frequency count csv file
    with open('test.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(csvOutput)
    print("Filtered words frequency csv file created...")

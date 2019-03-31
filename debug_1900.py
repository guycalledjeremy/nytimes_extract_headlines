import argparse
import json
import csv


def main(args):
    """
    """
    allOutput = []
    for i in range(10):
        allOutput.append([])
    data = json.load(open("cpd_data.json"))
    year_1900 = data[0]
    for word_data in year_1900:
        word = list(word_data.keys())[0]
        year = word_data[word][0]
        if 1900 <= year <= 1909:
            allOutput[0].append(word)
        elif 1910 <= year <= 1919:
            allOutput[1].append(word)
        elif 1920 <= year <= 1929:
            allOutput[2].append(word)
        elif 1930 <= year <= 1939:
            allOutput[3].append(word)
        elif 1940 <= year <= 1949:
            allOutput[4].append(word)
        elif 1950 <= year <= 1959:
            allOutput[5].append(word)
        elif 1960 <= year <= 1969:
            allOutput[6].append(word)
        elif 1970 <= year <= 1979:
            allOutput[7].append(word)
        elif 1980 <= year <= 1989:
            allOutput[8].append(word)
        elif 1990 <= year <= 1999:
            allOutput[9].append(word)
        else:
            print("Error: invalid year; word "+word+", year"+str(year))

    for year in allOutput:
        print(str(year)+": "+str(len(year)))

    # Get the CSV file
    allOutput_csv = [["year", "Data"]]
    for i in range(10):
        allOutput_csv.append([1900+i*10])
    for year in range(len(allOutput)):
        allOutput_csv[year+1].append(len(allOutput[year]))

    # Create the output word frequency count csv file
    with open(args.output_csv, 'w') as file:
        writer = csv.writer(file)
        writer.writerows(allOutput_csv)
    print("Debugging CSV file created...")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process each .')
    parser.add_argument("-c", "--output_csv", help="Directs the outputed  to a \
    filename of your choice", required=True)
    args = parser.parse_args()

    print("Debugging Started...")
    main(args)
    print("Debugging Finished.")

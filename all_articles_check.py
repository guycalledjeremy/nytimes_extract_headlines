""" Docstring for this file.
"""

import argparse
import json
import requests
import time


def main(args):
    """
    """
    allOutput = []
    # Get API_key
    api_key = open("api_key.txt", "r").read().strip()
    print("API key extracted...")
    # Get json data from NYTimes dataset
    headers = {'Accept': 'application/json'}
    # Initiate list of months for random generation
    # months = [month for month in range(1, 13)]
    # Get data from the randomly generate month of each year (1900-2000)
    print("Begin file extraction from URL...")
    task_count = 0
    # Initiate for timeout
    # task_count = 0
    for year in range(1900, 2000):
        article_count = 0
        for i in range(1, 13):
            if task_count == 10:
                task_count = 0
                print("Time out to avoid request limit...")
                time.sleep(60)
            with requests.get('https://api.nytimes.com/svc/archive/v1/'+str(year)+'/'+str(i)+'.json?api-key='+api_key, headers=headers) as file:
                data = file.json()
                task_count += 1
                # task_count += 1
                try:
                    # Only take the documents parts of the data
                    articles = data["response"]["docs"]
                    # Subsampling the dataset for inspection
                    # articles_sub = articles[:2]
                    article_count += len(articles)
                    print(str(year)+'/'+str(i)+" extracted")
                except KeyError:
                    print('Error: File extraction error, /'+str(year)+'/'+str(i)+'.')
        allOutput.append(article_count)
    print("File extracted from URL...")

    f_out = open(args.output, 'w')
    f_out.write(json.dumps(allOutput))
    f_out.close()
    print("Data JSON file created...")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process each .')
    parser.add_argument("-o", "--output", help="Directs the outputed topics to a \
    filename of your choice", required=True)
    args = parser.parse_args()

    print("Articles count Started...")
    main(args)
    print("Articles count Finished.")

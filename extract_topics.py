""" Docstring for this file.
"""

import argparse
import json
import requests
import time


def main(args):
    """ Describe this function.

    Parameters:
        args.output : string, filename of the output file
    """
    finished = False
    allOutput = []
    # Get API_key
    api_key = open("api_key.txt", "r").read().strip()
    print("API key extracted...")
    # Get json data from NYTimes dataset
    headers = {'Accept': 'application/json'}
    # Get data from the randomly generate month of each year (1900-2000)
    print("Begin file extraction from URL...")
    task_count = 0
    article_count = 0
    tech_article_count = 0
    # Break the data collection into two blocks
    for year in range(1990, 2019):
        for i in range(1, 13):
            if task_count == 10:
                task_count = 0
                print("Time out to avoid request limit...")
                time.sleep(60)
            with requests.get('https://api.nytimes.com/svc/archive/v1/'+str(year)+'/'+str(i)+'.json?api-key='+api_key, headers=headers) as file:
                data = file.json()
                task_count += 1
                try:
                    # Only take the documents parts of the data
                    articles = data["response"]["docs"]
                    # Subsampling the dataset for inspection
                    # articles_sub = articles[:2]
                    for article in articles:
                        article_count += 1
                        if article["section_name"] == "Technology":
                            tech_article_count += 1
                            for item in article["keywords"]:
                                if item["name"] == "subject" and item["value"] not in allOutput:
                                    allOutput.append(item["value"])

                    finished = True
                    print(str(year)+'/'+str(i)+" extracted")
                except KeyError:
                    print('Error: File extraction error, /'+str(year)+'/'+str(i)+'.')
    print("File extracted from URL...")

    if finished:
        print('Number of topics: '+str(len(allOutput)))
        print('Number of articles in total: '+str(article_count))
        print('Number of technology section articles in total: '+str(tech_article_count))
        # Create the new output topic json file
        t_out = open(args.output, 'w')
        t_out.write(json.dumps(allOutput))
        t_out.close()
        print("Topic JSON file created...")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process each .')
    parser.add_argument("-o", "--output", help="Directs the output to a \
    filename of your choice", required=True)
    args = parser.parse_args()

    print("Headline Topics Extraction Started...")
    main(args)
    print("Headline Topics Extraction Finished.")

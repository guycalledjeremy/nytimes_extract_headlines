""" Docstring for this file.
"""

import argparse
import json
import requests
import random


def preproc(headline):
    """ This function pre-process a single news headline

    Args:
        headline : string, the body of a headline

    Returns:
        modHeadline: string, the modified headline
    """
    print("TODO, proproc")


def main(args):
    """ This function gets data from NYTimes archive dataset and process each
    article to extract headlines. It returns nothing but outputs a json file
    from extraction and pro-processing.

    Parameters:
        args.output : string, filename of the output file
    """
    finished = False
    allOutput = []
    # TODO: Record all topics you get from the json file
    topicOutput = []
    # Get API_key
    api_key = open("api_key.txt", "r").read().strip()
    print("API key extracted...")
    # Get json data from NYTimes dataset
    headers = {'Accept': 'application/json'}
    # Initiate list of months for random generation
    months = [month for month in range(1, 13)]
    # Get data from the randomly generate month of each year (1900-2000)
    print("Begin file extraction from URL...")
    # Use a smaller time slot for testing:
    # for year in range(1900, 2001):
    # TODO: try get around the api's request limit (which is around 20/min)
    for year in range(1995, 2000):
        random.shuffle(months)
        for i in range(2):
            with requests.get('https://api.nytimes.com/svc/archive/v1/'+str(year)+'/'+str(months[i])+'.json?api-key='+api_key, headers=headers) as file:
                data = file.json()
                try:
                    # Only take the documents parts of the data
                    articles = data["response"]["docs"]
                    # Subsampling the dataset for inspection
                    articles_sub = articles[:2]
                    for article in articles_sub:
                        article_out = {}
                        article_out["headline"] = {}
                        article_out["headline"]["main"] = article["headline"]["main"]
                        # TODO: Notice not all years have the same json file structure.
                        # Pending: What's our solution to these two sections?
                        # try:
                        #     article_out["headline"]["print_headline"] = article["headline"]["print_headline"]
                        #     article_out["headline"]["sub"] = article["headline"]["sub"]
                        # except KeyError:
                        #     print('Older news having different format, /'+str(year)+'/'+str(months[i]))
                        article_out["keywords"] = article["keywords"]
                        # Add the topics to a list to be recorded in another json file
                        for item in article["keywords"]:
                            if item["name"] == "subject" and item["value"] not in topicOutput:
                                topicOutput.append(item["value"])
                        article_out["pub_date"] = article["pub_date"]
                        article_out["news_desk"] = article["news_desk"]
                        article_out["section_name"] = article["section_name"]
                        allOutput.append(article_out)

                    finished = True
                    print(str(year)+'/'+str(months[i])+" extracted")
                except KeyError:
                    print('Error: File extraction error, /'+str(year)+'/'+str(months[i])+'; \n' + str(data['fault']))
    print("File extracted from URL...")

    if finished:
        # Create the new output topic json file
        t_out = open(args.output_t, 'w')
        t_out.write(json.dumps(topicOutput))
        t_out.close()
        print("Topic JSON file created...")
        # Create the new output data json file
        f_out = open(args.output_d, 'w')
        f_out.write(json.dumps(allOutput))
        f_out.close()
        print("Data JSON file created...")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process each .')
    parser.add_argument("-o", "--output_d", help="Directs the output to a \
    filename of your choice", required=True)
    parser.add_argument("-t", "--output_t", help="Directs the outputed topics to a \
    filename of your choice", required=True)
    args = parser.parse_args()

    print("Headline Extraction Started...")
    main(args)
    print("Headline Extraction Finished.")

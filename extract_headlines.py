""" Docstring for this file.
"""

import argparse
import json
import requests


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
    # Get API_key
    api_key = open("api_key.txt", "r").read().strip()
    print("API key extracted.")
    # Get json data from NYTimes dataset
    headers = {'Accept': 'application/json'}
    with requests.get('https://api.nytimes.com/svc/archive/v1/2019/1.json?api-key='+api_key, headers=headers) as file:
        print("File extracted from URL.")
        data = file.json()
        try:
            # Only take the documents parts of the data
            articles = data["response"]["docs"]
            # Subsampling the dataset for inspection
            articles_sub = articles[:2]
            #
            for article in articles_sub:
                allOutput.append(article)

            finished = True
        except KeyError:
            print("Error: File extraction error; \n" + str(data['fault']))

    if finished:
        # Create the new
        f_out = open(args.output, 'w')
        f_out.write(json.dumps(allOutput))
        f_out.close()
        print("JSON file created.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process each .')
    parser.add_argument("-o", "--output", help="Directs the output to a \
    filename of your choice", required=True)
    args = parser.parse_args()

    print("Headline Extraction Started.")
    main(args)

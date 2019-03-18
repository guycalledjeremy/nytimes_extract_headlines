""" Docstring for this file.
"""

import argparse
import json
import requests
import time
import re
import spacy

nlp = spacy.load('en', disable=['parser', 'ner'])


def preproc(headline):
    """ This function pre-process a single news headline

    Args:
        headline : string, the body of a headline

    Returns:
        finHeadline: string, the modified headline
    """
    modHeadline = headline

    # Add a space around all punctuations, but avoid spliting abbreviation
    modHeadline = re.sub(r'(\S)(![\w\.])', r'\1 \2', modHeadline)
    modHeadline = re.sub(r'(![\w\.])(\S)', r'\1 \2', modHeadline)

    # Clean up all double spaces
    modHeadline = re.sub(r'\s+', r' ', modHeadline)

    # Get POS-Tags
    utt = nlp(modHeadline)
    finHeadline = ''
    for token in utt:
        # If this word is not a stop word
        if not nlp.vocab[token.text].is_stop:
            finHeadline = finHeadline + token.lemma_ + '/' + token.tag_ + ' '

    return finHeadline


def main(args):
    """ This function gets data from NYTimes archive dataset and process each
    article to extract headlines. It returns nothing but outputs a json file
    from extraction and pro-processing.

    Parameters:
        args.output : string, filename of the output file
    """
    finished = False
    allOutput = []
    years_count_Output = []
    # TODO
    # Record all topics you get from the json file
    # topicOutput = []
    # TODO
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
    article_count = 0
    tech_article_count = 0
    # Load the topics from the input file
    tech_topics = json.load(open(args.input))
    # Initiate for timeout
    # task_count = 0
    for year in range(1900, 2000):
        yearOutput = []
        year_article_count = 0
        # random.shuffle(months)
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
                    for article in articles:
                        article_count += 1
                        # Check if
                        tech_check = False
                        if article["keywords"] != []:
                            for item in article["keywords"]:
                                if item["name"] == "subject":
                                    if item["value"] not in tech_topics:
                                        tech_check = False
                                    else:
                                        tech_check = True
                            # if item["name"] == "subject" and item["value"] not in topicOutput:
                                # topicOutput.append(item["value"])
                        # If this article only has topics as recorded
                        if tech_check:
                            tech_article_count += 1
                            year_article_count += 1
                            article_out = {}
                            article_out["headline"] = preproc(article["headline"]["main"])
                            article_out["keywords"] = article["keywords"]
                            article_out["pub_date"] = article["pub_date"]
                            yearOutput.append(article_out)

                    finished = True
                    print(str(year)+'/'+str(i)+" extracted")
                except KeyError:
                    print('Error: File extraction error, /'+str(year)+'/'+str(i)+'.')

            # Check for task count to do timeout to avoid request limit
            # if task_count == 10:
                # print("Avoid exceeding request limit, sleep for 50s ...")
                # time.sleep(50)
                # task_count = 0
        years_count_Output.append(year_article_count)
        allOutput.append(yearOutput)
    print("File extracted from URL...")

    if finished:
        # Record the article counts by year
        y_out = open(args.output_y, 'w')
        y_out.write(json.dumps(years_count_Output))
        y_out.close()
        print("Year article counts recorded in JSON file...")
        # Create the new output data json file
        print('Number of years requested: '+str(len(allOutput)))
        print('Number of articles in total: '+str(article_count))
        print('Number of technology section articles in total: '+str(tech_article_count))
        f_out = open(args.output_o, 'w')
        f_out.write(json.dumps(allOutput))
        f_out.close()
        print("Data JSON file created...")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process each .')
    parser.add_argument("-i", "--input", help="the input json file containing \
    headlines", required=True)
    # parser.add_argument("-o", "--output_d", help="Directs the output to a \
    # filename of your choice", required=True)
    parser.add_argument("-y", "--output_y", help="Directs the outputed topics to a \
    filename of your choice", required=True)
    parser.add_argument("-o", "--output_o", help="Directs the outputed topics to a \
    filename of your choice", required=True)
    args = parser.parse_args()

    print("Headline Extraction Started...")
    main(args)
    print("Headline Extraction Finished.")

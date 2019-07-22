from elsapy.elsclient import ElsClient
from elsapy.elsdoc import FullDoc
import csv
import json
import pandas as pd


def ElsevierScraper(config_file, DOI_file, output_file):
    """
    Uses the Elsevier API and a list of DOIs to download plain text articles, including the title, abstract, pub date, 
    and the references as an unstructured string. Automatically resumes at the most recent DOI using the last line of 
    the output file.
    
    :param config_file: configuration json file, so far just contains the API key
    :param DOI_file: input .txt file containing one DOI per row
    :param output_file: csv file containing output
    :return:
    """

    ## Initialize client
    with open(config_file, 'r') as j:
        config = json.load(j)

    client = ElsClient(config['apikey'])
    DOIs = []

    with open(DOI_file, 'r') as f:
        for line in f.readlines():
            # This is only here becust j. DOIs have a higher success rate than others while the Springer scraper is being made
            if "j." in line:
                DOIs.append(line.strip("\n").strip("\r"))
    total = len(DOIs)

    # Tries to start from the most recent DOI present in the output file. If the file is empty, starts from the begining
    try:
        start = pd.read_csv(output_file)
        start = start.tail(1)['DOI'].iloc[0]
        start = DOIs.index(start.strip("\n").strip("\r")) + 1
        DOIs = DOIs[start:]
        output = []
    except:
        output = [["DOI", "Title", "Abstract", "Publication Date", "Text", "References"]]

    progress = total - len(DOIs)
    count = 0

    for DOI in DOIs:
        print(DOI)
        doi_doc = FullDoc(doi=DOI)
        if doi_doc.read(client):
            data = doi_doc.data
            coreData = data['coredata']
            abstract = coreData['dc:description']
            text = str(data['originalText']).split(abstract)[-1]
            try:
                references = text.split("References")[1]
            except IndexError:
                references = "NA"
            text = text.split("References")[0]
            date = coreData['prism:coverDisplayDate']
            output.append([DOI, doi_doc.title, abstract, date, text, references])
            count += 1
            if count % 10 == 0:
                with open(output_file, "a", encoding='utf8', newline="") as f:
                    writer = csv.writer(f)
                    writer.writerows(output)
                output = []

            if count % 100 == 0:
                print("Total Progress: {}%".format(round(float(count + progress) / total * 100, 4)))

        else:
            print("Read document failed.")

    with open(output_file, "a", encoding='utf8', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(output)


if __name__ == "__main__":
    ElsevierScraper('config.json', "DOIs.txt", "MatSciFullText.csv")

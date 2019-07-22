from elsapy.elsclient import ElsClient
from elsapy.elsdoc import FullDoc
import csv
import json
import pandas as pd
from multiprocessing import Pool
from functools import partial

"WARNING: This code is capable of completely blitzing the Elsevier servers with (especially with threads > 4)." \
"Not recommended as it may get your account suspended, though it does afford a 10x increase in speed. "


def mp_handler(DOI_file, output_file, mapped_function, num_processes=4):
    """
    Manages multiprocessing for scraping functions. Takes a list of DOIs and an output file, finds the most recent DOI
    in the output file and iterates through the DOIs from there.

    :param DOI_file: filename of the DOI text file
    :param output_file: filename of output csv
    :param mapped_function: function to be mapped
    :param num_processes: number of processes to be run in parallel
    :return: void: writes to CSV
    """

    DOIs = []
    with open(DOI_file, 'r') as f:
        for line in f.readlines():
            # This is only here becust j. DOIs have a higher success rate than others while the Springer scraper is being made
            if "j." in line:
                DOIs.append(line.strip("\n").strip("\r"))
    total = len(DOIs)

    # Tries to start from the most recent DOI present in the output file. If the file is empty, writes headers to file
    # TODO Test that header writing works properly
    try:
        start = pd.read_csv(output_file)
        start = start.tail(1)['DOI'].iloc[0]
        start = DOIs.index(start.strip("\n").strip("\r")) + 1
        DOIs = DOIs[start:]

    except:
        with open(output_file, mode='a', encoding='utf8', newline="") as outputFile:
            output_writer = csv.writer(outputFile, delimiter=',')
            output_writer.writerow(["DOI", "Title", "Abstract", "Publication Date", "Text", "References"])
    progress = total - len(DOIs)

    pool = Pool(processes=num_processes)
    count = 0
    with open(output_file, mode='a', encoding='utf8', newline="") as outputFile:
        output_writer = csv.writer(outputFile, delimiter=',')
        for result in pool.imap(mapped_function, DOIs):
            output_writer.writerow(result)
            count += 1
            if count % 100 == 0:
                print("Total Progress: {}%".format(round(float(count + progress) / total * 100, 4)))


def ElsevierScraper(client, target_DOI):
    """
    Uses the Elsevier API and a list of DOIs to download plain text articles, including the title, abstract, pub date,
    and the references as an unstructured string. Automatically resumes at the most recent DOI using the last line of
    the output file.

    :param client: Elsevier client containing the API key
    :param target_DOI: DOI of the article being scraped
    :return: list containing the DOI, title, abstract, publication date, full text and unstructured string of references
    """

    print(target_DOI)
    doi_doc = FullDoc(doi=target_DOI)
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
        return [target_DOI, doi_doc.title, abstract, date, text, references]
    else:
        print("Read document failed.")


if __name__ == "__main__":
    # Initialize client
    with open('config.json', 'r') as j:
        config = json.load(j)
    client = ElsClient(config['apikey'])

    scraper = partial(ElsevierScraper, client)
    mp_handler('DOIs.txt', "MatSciFullText.csv", scraper, num_processes=4)

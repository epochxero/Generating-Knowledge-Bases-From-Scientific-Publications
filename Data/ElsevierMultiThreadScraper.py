from elsapy.elsclient import ElsClient
from elsapy.elsdoc import FullDoc
import csv
import json
from multiprocessing import Pool
from functools import partial
import os

"""
WARNING: This code is capable of completely blitzing the Elsevier servers (especially with threads > 4).
Not recommended as it may get your API account suspended, though num_threads=4 does afford a 10x increase in speed 
compared to num_threads=1. Set to 2 by default to err on the side of caution. When running, time how long it takes
to grab 100 articles (the progress counter appears every 100 articles). 18 - 20 seconds is the fastest tested range (no
issues) but 20 - 25 seconds is likely less likely safer. 
"""


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
            # Only necessary if using original DOI list
            if "j." in line:
                DOIs.append(line.strip("\n").strip("\r"))
    total = len(DOIs)

    # Tries to start from the most recent DOI present in the output file. If the file is empty, writes headers to file
    try:
        with open(output_file, 'rb') as f:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
            last_line = f.readline().decode()

        start = last_line.split(",")[0]
        print("Most Recent DOI: {}".format(start))
        start = DOIs.index(start.strip("\n").strip("\r")) + 1
        print("Resume Position: {}".format(start))
        DOIs = DOIs[start:]

    except Exception as e:
        print(e)
        if os.path.isfile(output_file):
            print("Invalid DOI, please check the last line of the file to ensure it's written properly")
            return
        else:
            print("No file exists, initializing file")
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

    print("Done!")

def ElsevierScraper(client, target_DOI):
    """
    Uses the Elsevier API with a valid key and a DOI to download the plain text article, including the title, abstract,
    pub date, and the references as an unstructured string.

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
        # Could save this to a separate file but it's easier to search for NA and make a new sublist after the fact
        print("Error: couldn't read {}.".format(target_DOI))
        return [target_DOI, "NA", "NA","NA","NA","NA"]


if __name__ == "__main__":
    # Initialize client
    with open('config.json', 'r') as j:
        config = json.load(j)
    client = ElsClient(config['apikey'])
    scraper = partial(ElsevierScraper, client)
    mp_handler('DOI_j.txt', "MatSciFullText.csv", scraper, num_processes=2)

import argparse
import csv
import httplib
import json


def load_data(user_id):

    print("Connecting to remote web site...")
    con = httplib.HTTPConnection("10fastfingers.com")
    print("Connected to remote web site.")
    headers = {
        "X-Requested-With": "XMLHttpRequest"
    }

    print("Retrieving data...")
    con.request("POST", "/users/get_graph_data/1/{}/0".format(user_id), "", headers)
    response = con.getresponse()
    response_content = response.read()
    print("Data retrieved.")

    print("Parsing data...")
    data = json.loads(response_content)
    print("Data parsed.")

    return data


def prepare_data(stats):
    result = []

    for data_item in stats:
        new_data_item = {}
        for k, v in data_item.items():
            new_data_item[k] = v

        test_type = ""
        if "g1" in data_item:
            test_type = "simple"
        elif "g2" in data_item:
            test_type = "advanced"
        new_data_item["test_type"] = test_type
        result.append(new_data_item)

    return result


def parse_arguments():

    parser = argparse.ArgumentParser(description='Import statistics from http://10fastfingers.com to a CSV file.')
    parser.add_argument('-u', '--user', required=True,
                        help='The user identifier')
    parser.add_argument('-o', '--target-file', required=True,
                        help='The target directory')

    return parser.parse_args()


def write_stats(target_file):

    with open(target_file, 'wb') as f:
        writer = csv.DictWriter(f,
                                {'test_type', 'date', 'keystrokes', 'backspace_pressed',
                                 'correct_words', 'wrong_words'},
                                extrasaction='ignore', quoting=csv.QUOTE_ALL)
        for data_item in stats:
            writer.writerow(data_item)

# Retrieve arguments
args = parse_arguments()
user_id = args.user
target_file = args.target_file

# Load and process stats
graph_data = load_data(user_id)
stats = graph_data["graph_data"]
stats = prepare_data(stats)

# Write the stats
write_stats(target_file)
import os
import json
import pandas as pd
from bart_work_personality_classifier import identify_work_personality


def aggregate_podcasts(directory):
    combined_text = []
    combined_labels = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                print(file)
                file_path = os.path.join(root, file)
                
                # Read the JSON file
                with open(file_path, 'r') as json_file:
                    try:
                        data = json.load(json_file)
                        print(json_file)
                        print('\n')
                        for block in data['results']:
                            if not block['alternatives'][0]:
                                continue
                            text = block['alternatives'][0]['transcript']
                            label = identify_work_personality(text)

                            if label:
                                combined_text.append(text)
                                combined_labels.append(label)

                    except json.JSONDecodeError:
                        print(f"Error decoding JSON file: {file_path}")
                    except KeyError:
                        print(f"Transcript not found in JSON file: {file_path}")

    return {'text': combined_text, 'label': combined_labels}

# directory = os.path.join(os.getcwd(), 'data-sets/spotify-podcasts-2020/podcasts-transcripts')
# df = pd.DataFrame(aggregate_podcasts(directory))
# df.to_csv('spotify_podcast_labeled_text.csv')
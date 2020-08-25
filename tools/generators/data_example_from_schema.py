import os
import json


def create_data_example_from_schema(base_dir, target_dir, export_onto_url):
    """Generate data example based on schema.

        Args:
            base_dir (str): Schema directory.
            target_dir (str): DataExample directory.
            export_onto_url (str): Link to base ontologies.

        Returns:
    """
    for path, subdirs, files in os.walk(base_dir):
        for name in files:
            if "DataProductParameters" not in path and "DataProductOutput" not in path :
                with open(os.path.join(path, name), 'r') as json_file:
                    data = json.load(json_file)
                # Build data example json based on schema
                data_example = dict()
                data_example['@context'] = f'{export_onto_url}Context/{name[:-5]}/'
                data_example['@type'] = f'{name[:-5]}'
                data_example['@id'] = ''
                data_example['data'] = ''
                data_example['metadata'] = ''

                for i in data['properties']:
                    if i != '@type' and i != '@context':
                        if data['properties'][i].get('properties'):
                            data_example[i] = {k: data['properties'][i]['properties'][k]['examples'][0]
                                            if 'examples' in data['properties'][i]['properties'][k] else '' for k in data['properties'][i]['properties']}
                        else:
                            data_example[i] = ''

                # Build DataExample files
                data_example_path = path.replace(base_dir, target_dir)
                if not os.path.exists(data_example_path):
                    os.makedirs(data_example_path)
                with open(os.path.join(data_example_path, name), 'w') as data_example_file:
                    json.dump(data_example, data_example_file,
                            indent=4, ensure_ascii=False)

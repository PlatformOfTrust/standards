import os
import json
from shutil import copyfile, copy       


def move_manual(base_dir, target_dir):
    for f in os.listdir(base_dir):
        with open(os.path.join(base_dir, f), 'r') as json_file:
            data = json.load(json_file)

            if isinstance(data, list):
                data = data[0]
            if data.get('$id'):
                entity_path = [x for x in data['$id'].split('/') if x]
            elif data.get('@context'):
                entity_path = [x for x in data['@context'].split('/') if x]
            else:
                raise KeyError

            entity_path.insert(4, target_dir)
            target_path = '/'.join(entity_path[4:-1])
            target_file = entity_path[-1]
            os.makedirs(target_path, exist_ok=True)
            
            copy(os.path.join(base_dir, f), os.path.join(target_path, f'{target_file}.json'))

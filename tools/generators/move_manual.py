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
                target_path = target_dir + '/' + \
                    '/'.join([x for x in data['$id'].split('/') if x][4:-1])
            elif data.get('@context'):
                target_path = target_dir + '/' + \
                    '/'.join([x for x in data['@context'].split('/') if x][4:-1])
            else:
                raise KeyError
            
            if not os.path.exists(target_path):
                os.mkdir(target_path)

            copy(os.path.join(base_dir, f), os.path.join(target_path, f))

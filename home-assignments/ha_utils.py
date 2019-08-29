import os
import json
import urllib

def parse_cell_ids(nb_json_data):
    cell_ids = []
    for cell in nb_json_data['cells']:
        if 'metadata' in cell and 'nbgrader' in cell['metadata'] and 'grade_id' in cell['metadata']['nbgrader']:
            cell_ids.append(cell['metadata']['nbgrader']['grade_id'])
    return cell_ids

def check_notebook_uptodate_and_not_corrupted(nb_dirname, nb_fname):
    assignment_name = os.path.basename(nb_dirname)
    commit = 'master' # Should be master (latest version)
    # commit = '3d1588a79b1bd6361f6b12da9e6be022adf0f683' # For debug
    url = 'https://raw.githubusercontent.com/JulianoLagana/deep-machine-learning/{commit}/Home%20Assignments/{assignment_name}/{assignment_name}.ipynb'.format(assignment_name=assignment_name, commit=commit)
    try:
        ref_nb_file = urllib.request.urlopen(url)
    except:
        print('[WARNING] Could not fetch reference notebook from GitHub repo. Are you offline?')
        print('[WARNING] Could not verify that current notebook is up-to-date and not corrupted')
        return
    ref_nb_data = json.load(ref_nb_file)
    with open(os.path.join(nb_dirname, nb_fname), 'r') as f:
        curr_nb_data = json.load(f)
    ref_cell_ids = parse_cell_ids(ref_nb_data)
    curr_cell_ids = parse_cell_ids(curr_nb_data)
    assert len(curr_cell_ids) == len(set(curr_cell_ids)), \
        '[ERROR] Notebook appears to be corrupt - detected multiple cells with same cell ID. Did you copy/paste any cells?'
    ref_cell_ids = set(ref_cell_ids)
    curr_cell_ids = set(curr_cell_ids)
    assert len(curr_cell_ids) > 0, \
        '[ERROR] Notebook appears to be corrupt - no cell IDs found. Did you perhaps run it on Google Colab?'
    if len(ref_cell_ids - curr_cell_ids) > 0:
        print('Missing cells: {}'.format(sorted(ref_cell_ids - curr_cell_ids)))
    if len(curr_cell_ids - ref_cell_ids) > 0:
        print('Found unexpected cells: {}'.format(sorted(curr_cell_ids - ref_cell_ids)))
    assert ref_cell_ids == curr_cell_ids, \
        '[ERROR] Notebook does not seem to be up-to-date.'

    print('[SUCCESS] Notebook is up-to-date!')

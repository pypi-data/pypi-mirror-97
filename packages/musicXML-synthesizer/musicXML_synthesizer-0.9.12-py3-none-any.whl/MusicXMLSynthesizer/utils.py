from pathlib import Path

def parse_notes_meta_to_list(file_path):

    result_list = []
    # detect non-exist file path
    fp = Path(file_path)
    if not fp.is_file():
        print("Path:{}, Contnet: {}".format("Invalid", ""))
        return 

    with open(file_path, 'r') as f:
        result_list = f.readlines()
    return result_list


def write_file(output_path, xml=""):
    fp = Path(output_path)
    print()

    parent_dir_path = fp.parents[0]
    if not parent_dir_path.exists() and not parent_dir_path.is_dir():
        print('not exist')
        Path.mkdir(parent_dir_path)

    file = open(output_path, "w+")
    file.write(xml)

    print('done')

def create_synthesizer(input_data_directory):
    # input data
    xsd_path = "musicxml-3.1-dtd-xsd/schema/musicxml.xsd"
    techs_and_notes_list = parse_notes_meta_to_list(
        "{}FinalNotes.txt".format(input_data_directory))
    beats_list = parse_notes_meta_to_list(
        "{}beats.txt".format(input_data_directory))
    downbeats_list = parse_notes_meta_to_list(
        "{}downbeats.txt".format(input_data_directory))
    
    # setup
    synthesizer = Synthesizer(xsd_path)
    synthesizer.save(techs_and_notes_list, downbeats_list, beats_list)
    
    return synthesizer
import os
import json


def read_sensor_grid_result(result_folder, extension, grid_key):
    """Read results from files that align with sensor grids.

    Args:
        result_folder: Path to the folder containing the results.
        extension: Text for the file extension to be read (eg. res).
        grid_key: Text for the key in the grids_info.json that identifies the
            file name of each sensor grid.

    Returns:
        A matrix with each sub-list containing the values for each of the sensor grids.
    """
    # check that the required files are present
    if not os.path.isdir(result_folder):
        raise ValueError('Invalid result folder: %s' % result_folder)
    grid_json = os.path.join(result_folder, 'grids_info.json')
    if not os.path.isfile(grid_json):
        raise ValueError('Result folder contains no grids_info.json.')

    # load the list of grids and gather all of the results
    with open(grid_json) as json_file:
        grid_list = json.load(json_file)
    results = []
    for grid in grid_list:
        result_file = os.path.join(
            result_folder, '{}.{}'.format(grid[grid_key], extension))
        if os.path.isfile(result_file):
            with open(result_file) as inf:
                results.append([min(float(line), 100) for line in inf])
    return results

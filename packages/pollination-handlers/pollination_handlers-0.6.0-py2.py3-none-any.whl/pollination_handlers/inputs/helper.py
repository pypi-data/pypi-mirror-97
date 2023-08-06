import os
import tempfile
import uuid


def get_tempfile(extension, file_name=None):
    """Get full path to a temporary file with extension."""
    file_name = str(uuid.uuid4())[:6] if file_name is None \
        or file_name == '-' else file_name
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, '%s.%s' % (file_name, extension))
    return file_path


def write_values_to_csv(file_path, values):
    """Write a list of fractional values to a discrete 0/1 CSV."""
    discrete_vals = []
    for v in values:
        dv = '1' if v >= 0.1 else '0'
        discrete_vals.append(dv)
    with open(file_path, 'w') as fp:
        fp.write('\n'.join(discrete_vals))
    return file_path

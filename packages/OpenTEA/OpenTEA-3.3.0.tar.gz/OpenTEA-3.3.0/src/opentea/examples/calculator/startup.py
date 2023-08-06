"""Startup script to call calculator gui."""
import os
import inspect
import yaml
from opentea.gui_forms.otinker import main_otinker


def main(schema_file=None):
    """Call the otinker gui."""
    if schema_file == None:
        schema_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "schema_calculator.yaml")
    with open(schema_file, 'r') as fin:
        schema = yaml.load(fin, Loader=yaml.FullLoader)
    base_dir = inspect.getfile(inspect.currentframe())
    base_dir = os.path.dirname(os.path.abspath(base_dir))
    main_otinker(schema, calling_dir=base_dir, tab_3d=True)


if __name__ == "__main__":
    main()

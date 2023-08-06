"""Generate a Tk from upon a Gui schema.

A GUI schema is a JSON-Schema dictionnary,
with tags require and existifs added to declare explicit cyclic depenencies
"""
import os
import time
from PIL import ImageTk, Image
from tkinter import Tk, ttk, TclError
import opentea
from opentea.gui_forms.root_widget import OTRoot
from opentea.gui_forms.constants import (
    BASE_DIR,
    set_constants,
    quit_dialog,
)
from opentea.noob.validation import validate_opentea_schema


def create_voidfile(path):
    """Create a dummy file for otinker"""
    void_ct = """
# Opentea Project
meta:
  validate: {}
"""
    with open(path, "w") as fout:
        fout.write(void_ct)

def ask_new_file(root):
    """Dialog to ask a new file"""
    path = os.path.join(BASE_DIR, "images", "logo_project_large.gif")
    logo_im = Image.open(path)
    logo_tk = ImageTk.PhotoImage(logo_im)

    holder = ttk.Frame(root)

    label = ttk.Label(holder, image=logo_tk)
    label.image = logo_tk  # keep a reference!
    label.pack(side="top")
    holder.pack()
    # Dialog
    def full_name(name):
        tmp = name + ".yml"
        tmp.replace(" ", "_")
        return os.path.join(os.getcwd(), tmp)

    def callback():
        """what happen if command is pressed"""
        pname_str = entry.get()
        if len(pname_str) <= 3:
            feedback["text"] = "Please use more characters..."
            feedback.configure(foreground="red")
            root.update()
            return

        if os.path.isfile(full_name(pname_str)):
            feedback["text"] = "This file already exist..."
            feedback.configure(foreground="red")
            root.update()
            return

        feedback["text"] = f"Success, starting up with {pname_str}.yml ..."
        feedback.configure(foreground="green4")
        root.update()
        time.sleep(0.3)
        root.quit()

    task = ttk.Label(holder, text="What will be the name of this project?")
    entry = ttk.Entry(holder)
    button = ttk.Button(holder, text="Start", command=callback)
    feedback = ttk.Label(holder, text="")

    task.pack(side="top")
    entry.pack(side="top")
    button.pack(side="top")
    feedback.pack(side="bottom")
    root.mainloop()

    try:
        out = full_name(entry.get())
        holder.destroy()
        create_voidfile(out)
    except TclError:
        out = "-Interrupted-"
    return out


# pylint: disable=too-many-arguments
def main_otinker(
    schema,
    calling_dir=None,
    start_mainloop=True,
    tab_3d=False,
    theme="clam",
    data_file=None,
):
    """Startup the gui generation.

    Inputs :
    --------
    schema : dictionary compatible with json-schema
    calling_dir : directory from which otinker was called
    test_only : only for testing

    Outputs :
    ---------
    a tkinter GUI
    """
    # global CALLING_DIR
    # CALLING_DIR = calling_dir
    print(f"Staring up OpenTEA GUI engine v.{opentea.__version__}...")
    validate_opentea_schema(schema)
    tksession = Tk()
    tksession.protocol("WM_DELETE_WINDOW", quit_dialog)

    sty = ttk.Style()
    sty.theme_use(theme)

    set_constants(tksession, calling_dir, theme)

    if start_mainloop is False:
        create_voidfile("dummy.yml")
        data_file = "dummy.yml"

    if data_file is None:
        data_file = ask_new_file(tksession)
    else:
        data_file = os.path.abspath(data_file)

    if data_file == "-Interrupted-":
        return

    print(f"Opening {data_file}...")
    OTRoot(
        schema,
        tksession,
        start_mainloop=start_mainloop,
        tab_3d=tab_3d,
        data_file=data_file,
    )

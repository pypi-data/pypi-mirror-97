"""Constants definitions."""
import os
from glob import glob
import inspect
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msgbox

# from tkinter import Text as Tk_Text
from tkinter.scrolledtext import ScrolledText
from tkinter import Variable as Tk_Variable
from tkinter import Canvas as Tk_Canvas
from PIL import ImageTk, Image

# BG_COLOR = '#%02x%02x%02x' % (220, 218, 213)
WIDTH_UNIT = 400
LINE_HEIGHT = 22
BASE_DIR = inspect.getfile(inspect.currentframe())
BASE_DIR = os.path.dirname(os.path.abspath(BASE_DIR))


IMAGE_DICT = dict()
PARAMS = dict()
VALIDATE = dict()


class SetException(Exception):
    """Define an exception on the widget setters."""


class GetException(Exception):
    """Define an exception on the widget getters."""


def quit_dialog():
    """Quitting dialog"""
    if msgbox.askokcancel("Quit", "Do you really wish to quit?"):
        PARAMS["top"].destroy()
        print("Get outta here and go back to your boring programs.")


# pylint: disable=global-statement
def set_constants(tksession, calling_dir, theme):
    """Set top Tk objet"""
    global PARAMS
    PARAMS["top"] = tksession
    PARAMS["calling_dir"] = calling_dir

    if theme not in ["alt", "aqua", "clam", "classic", "default"]:
        print(theme + " theme not supported. Fallback to clam...")
        theme = "clam"

    PARAMS["theme"] = theme
    if theme == "alt":
        bgc = (224, 224, 224)
        PARAMS["bg"] = "#%02x%02x%02x" % bgc
        PARAMS["bg_lbl"] = "#%02x%02x%02x" % (
            bgc[0] - 7,
            bgc[1] - 7,
            bgc[2] - 7,
        )
    if theme == "aqua":
        bgc = (240, 240, 240)
        PARAMS["bg"] = "#%02x%02x%02x" % bgc
        PARAMS["bg_lbl"] = "#%02x%02x%02x" % (
            bgc[0] - 7,
            bgc[1] - 7,
            bgc[2] - 7,
        )
    if theme == "clam":
        bgc = (220, 218, 213)
        PARAMS["bg"] = "#%02x%02x%02x" % bgc
        PARAMS["bg_lbl"] = PARAMS["bg"]
    if theme == "classic":
        bgc = (224, 224, 224)
        PARAMS["bg"] = "#%02x%02x%02x" % bgc
        PARAMS["bg_lbl"] = "#%02x%02x%02x" % (
            bgc[0] - 6,
            bgc[1] - 6,
            bgc[2] - 6,
        )
    if theme == "default":
        bgc = (220, 218, 213)
        PARAMS["bg"] = "#%02x%02x%02x" % bgc
        PARAMS["bg_lbl"] = "#%02x%02x%02x" % (
            bgc[0] - 3,
            bgc[1] - 1,
            bgc[2] + 4,
        )

    bgc_dark = tuple([int(0.3 * i) for i in bgc])
    PARAMS["bg_dark"] = "#%02x%02x%02x" % bgc_dark


# pylint: disable=global-statement
def set_root(root):
    """Set root objet"""
    global PARAMS
    PARAMS["root"] = root


# pylint: disable=global-statement
def set_tabs(tabs):
    """Set validate shared meory"""
    global VALIDATE
    for tabname in tabs:
        VALIDATE[tabname] = 0


# pylint: disable=global-statement
def tab_validated(tabname, value):
    """Set validate shared meory"""
    global VALIDATE
    VALIDATE[tabname] = value


# pylint: disable=global-statement
def load_icons():
    """Load icons.

    Load all ./otinker_images/*_icon.gif as icons

    Returns :
    ---------
    load_icons : dictionnary of ImageTk objects
    """
    global IMAGE_DICT
    icons_dir = os.path.join(BASE_DIR, "images")
    icons_pattern = "_icon.gif"
    icons_files = glob("%s/*%s" % (icons_dir, icons_pattern))
    icons = dict()
    for k in icons_files:
        key = os.path.basename(k).replace(icons_pattern, "")
        icons[key] = ImageTk.PhotoImage(Image.open(k))
        IMAGE_DICT[key] = icons[key]
    return icons


# pylint: disable=too-many-ancestors
class SwitchForm(ttk.Frame):
    """Overriden Frame class to mimick notebooks without tabs."""

    def add(self, name, title=None):
        """Add a tab-like Frame."""
        # if name[0] != name[0].lower():
        #    raise RuntimeError(
        #        "Switchforms cannot start with  upper case letters")
        tab_id = ttk.LabelFrame(
            self, name="_" + name, text=title, relief="sunken"
        )
        tab_id.shortname = name
        self.sf_raise(tab_id)
        return tab_id

    def sf_del(self, tab_name):
        """Destroy tab_id tab."""
        for child_widget in self.winfo_children():
            if child_widget.shortname == tab_name:
                child_widget.destroy()

    def sf_raise(self, tab_name):
        """Forget current view and repack tab_name tab."""
        for child_widget in self.winfo_children():
            if child_widget.shortname == tab_name:
                child_widget.pack(fill="both")
            else:
                child_widget.pack_forget()


def create_scrollable_canvas(holder_frame):
    """Create a scollable canvas."""
    frm = ttk.Frame(holder_frame)
    frm.pack(side="top", fill="both", expand=True)
    frm.columnconfigure(0, weight=1)
    frm.columnconfigure(1, weight=0)
    frm.rowconfigure(0, weight=1)
    frm.rowconfigure(1, weight=0)

    frm.can = Tk_Canvas(
        frm,
        background=PARAMS["bg_lbl"],
        highlightbackground=PARAMS["bg_lbl"],
        highlightcolor=PARAMS["bg_lbl"],
    )

    frm.can.configure(width=1000, height=300)

    frm.sby = ttk.Scrollbar(frm, orient="vertical", command=frm.can.yview)
    frm.sbx = ttk.Scrollbar(frm, orient="horizontal", command=frm.can.xview)

    frm.can.configure(yscrollcommand=frm.sby.set)
    frm.can.configure(xscrollcommand=frm.sbx.set)

    frm.can.grid(row=0, column=0, sticky="news")
    frm.sby.grid(row=0, column=1, sticky="ns")
    frm.sbx.grid(row=1, column=0, sticky="we")
    return frm.can


# pylint: disable=too-many-arguments
class TextConsole:
    """ Text widget with search and auto -refresh capabilities."""

    def __init__(
        self,
        holder,
        content,
        height=None,
        width=None,
        search=False,
        disabled=True,
    ):
        """Startup class.

        holder : Tkwidget where to pack the text
        content: Tkstring to display in the widget"""
        self.content = content
        self.disabled = disabled
        self.container = ttk.Frame(holder, relief="sunken")
        self.container.pack(fill="both",)
        self.controls = ttk.Frame(self.container)
        self.body = ttk.Frame(self.container,)
        if search:
            self.controls.pack(fill="x", side="top")
        self.body.pack(fill="x", side="bottom", padx=2, pady=2)
        if disabled:
            bg_color = PARAMS["bg"]
        else:
            bg_color = "white"
        self.txt = ScrolledText(
            self.body,
            background=bg_color,
            highlightbackground=PARAMS["bg_lbl"],
        )
        if height is not None:
            self.txt.configure(height=height)
        if width is not None:
            self.txt.configure(width=width)
        self.txt.pack(fill="both")
        self.search_var = Tk_Variable()
        self.search_lbl = ttk.Label(self.controls, text="Search")
        self.search_ent = ttk.Entry(
            self.controls, textvariable=self.search_var
        )
        self.search_lbl.pack(side="right")
        self.search_ent.pack(side="right")

        self.update()
        self.search_var.trace("w", self.highlight_pattern)
        self.content.trace("w", self.update)

    def update(self, *args):
        """Update the content"""
        self.txt.configure(state="normal")
        self.txt.delete(0.0, "end")
        self.txt.insert(0.0, self.content.get())
        if self.disabled:
            self.txt.configure(state="disabled")
        self.highlight_pattern()

    def highlight_pattern(self, *args):
        """Highlight the pattern."""
        self.txt.tag_delete("highlight")
        self.txt.mark_set("insert", 1.0)
        self.txt.mark_set("matchStart", 1.0)
        self.txt.mark_set("matchEnd", 1.0)
        self.txt.mark_set("searchLimit", "end")
        count = tk.StringVar()
        pattern = self.search_var.get()
        if pattern:
            while True:
                index = self.txt.search(
                    self.search_var.get(),
                    "matchEnd",
                    "searchLimit",
                    count=count,
                    regexp=True,
                )
                if index == "":
                    break
                if count.get() == 0:
                    break
                self.txt.mark_set("matchStart", index)
                self.txt.mark_set("insert", index)
                self.txt.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                self.txt.tag_add("highlight", "matchStart", "matchEnd")
        self.txt.tag_config("highlight", background="yellow")
        self.txt.see("insert")

    def get(self):
        """Get the content"""
        return self.txt.get("1.0", "end")

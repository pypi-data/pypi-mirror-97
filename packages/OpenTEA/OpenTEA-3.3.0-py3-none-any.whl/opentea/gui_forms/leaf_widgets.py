"""
Leaf widgets :
==============

Leaves are the lower part to the graph,
at the tip of the branches.
Most of these widget are entries.

Entries:
--------

The generic node EntryNode is the basis for all
single line inputs:

 - numbers
 - integers
 - strings

Additionnal content can be shown to give info
in the case of validation rules.

Booleans:
---------

This is tranlated to a single Checkbox

Choices:
--------

The choice widget corresponds to the Schema enum property.
This is tranlated to radiobuttons in the form.

FleBrowser:
-----------

This special entry check that the content is a file,
and add a browsing dialog to select the file.

Documentation and Description (DEPRECATED):
-------------------------------------------

Kept fo backward compatibility,
docuementation and descriptions are wats to display strings
in the forms.

Prefer now the documentation and description attributes
in the blocks.

Comments:
---------

Comments are multiline textfields
They can also be usefull for feedbach in disabled mode.

Lists:
------

List corresponds to arrays of parameters,
shown aslist of entries.
These list cannot take dependency links for the moments.

Without a fixed dimension,
specified with "MaxItemns" and "MinItems" attributes in the SCHEMA,
a +/- dialog is shown to extend or crop the list.

"""

import os
import operator

from tkinter import (ttk,
                     Variable,
                     StringVar,
                     BooleanVar,
                     Label,
                     Toplevel,
                     Text,
                     Entry,
                     Listbox,
                     filedialog)

from nob import Nob

from opentea.gui_forms.constants import (
    PARAMS,
    WIDTH_UNIT,
    LINE_HEIGHT,
    IMAGE_DICT,
    GetException,
    SetException,
    TextConsole)

#pylint: disable=too-few-public-methods
class LeafWidget():
    """Factory for OpenTea Widgets."""

    def __init__(self, schema, root_frame, name):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        holder_nlines : integer
            custom number of lines for holder
        """
        self.tree = dict()
        self.status = 1
        self.schema = schema

        self._title = "#" + name
        if "title" in schema:
            self._title = schema["title"]

        self.state = "normal"
        if "state" in schema:
            self.state = schema["state"]

        self._holder = ttk.Frame(root_frame,
                                 name=name,
                                 width=WIDTH_UNIT,
                                 height=LINE_HEIGHT)
        if self.state != "hidden":
            self._holder.pack(side="top", fill="x")

        self._label = Label(self._holder,
                            text=self._title,
                            background=PARAMS["bg_lbl"],
                            justify="right",
                            wraplength=int(0.5*WIDTH_UNIT))
        self._label.place(relx=0.5, rely=0.5, anchor="se")

        if "description" in schema:
            self._desc = Label(
                root_frame,
                text=schema["description"],
                background=PARAMS["bg_lbl"],
                justify="left",
                wraplength=int(1*WIDTH_UNIT))
            self._desc.pack(side="top", fill="x")

    def get_status(self):
        """Return current attribute self.status."""
        return self.status


#pylint: disable=no-member
class _OTEntry(LeafWidget):
    """Factory for OpenTea Entries."""

    def __init__(self, schema, root_frame, name):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, root_frame, name)

        self._inits_entry(schema)

    def _inits_entry(self, schema):
        """Initialise entry."""
        self.tkvar = Variable()
        self._status = Label(self._holder,
                             text="no status yet",
                             background=PARAMS["bg_lbl"],
                             foreground="red",
                             justify="left",
                             compound="left",
                             wraplength=WIDTH_UNIT,
                             width=WIDTH_UNIT)
        self._entry = Entry(self._holder,
                            textvariable=self.tkvar,
                            borderwidth=0)

        if self.state == "disabled":
            self._entry.configure(
                highlightbackground=PARAMS["bg"],
                disabledbackground=PARAMS["bg"],
                disabledforeground=PARAMS["bg_dark"],
                state="disabled")

        self._entry.bind('<Key>', self.memory_change)

        self._entry.place(relwidth=0.5, relx=0.5, rely=0.5, anchor="sw")
        self._status.place(relx=0.5, rely=0.5, anchor="n")

        self._holder.config(height=2 * LINE_HEIGHT)

        self.tkvar.trace('w', self._update_status_callback)
        self._bounds = [None]*2
        self._exclusive_bounds = [False]*2

        if "maximum" in schema:
            self._bounds[1] = schema['maximum']
            if "exclusiveMaximum" in schema:
                self._exclusive_bounds[1] = schema["exclusiveMaximum"]
        if "minimum" in schema:
            self._bounds[0] = schema['minimum']
            if "exclusiveMinimum" in schema:
                self._exclusive_bounds[0] = schema["exclusiveMinimum"]

    def memory_change(self, *args):
        """Trigger virtual event on mermory change."""
        if self.state == "normal":
            self._entry.event_generate('<<mem_change>>')

    def _update_status_callback(self, *args):
        """Redirect upon status callback."""
        self.status = 1
        status = ''
        try:
            value = self.get()
            self._status.config(text='', image='')
            if isinstance(value, (float, int)):
                status = self._boundedvalue()
                if status:
                    raise GetException
            #self._entry.event_generate('<<mem_change>>')

        except GetException:
            if not status:
                status = 'Invalid input "%s"' % (self._entry.get())
            self._status.config(
                text=status, fg='red', image=IMAGE_DICT['invalid'])
            self.status = -1

    def _boundedvalue(self):
        """Validate rules on entries."""
        value = self.get()
        error_msg = str()

        str_operators = ['>', '<']
        operators = [operator.ge, operator.le]
        for i in range(2):
            if self._bounds[i] is not None:
                if operators[i](value, self._bounds[i]):
                    if self._exclusive_bounds[i]:
                        if value == self._bounds[i]:
                            error_msg = (
                                'Invalid :%s %s' % (str_operators[i],
                                                    str(self._bounds[i])))
                else:
                    error_msg = (
                        'Invalid:%s= %s' % (str_operators[i],
                                            str(self._bounds[i])))
                    if self._exclusive_bounds[i]:
                        error_msg = (
                            'Invalid %s %s' % (str_operators[i],
                                               str(self._bounds[i])))
        return error_msg


class OTInteger(_OTEntry):
    """OTinteger variable."""

    def get(self):
        """Return python integer."""
        try:
            out = int(self.tkvar.get())
        except ValueError:
            raise GetException()
        return out

    def set(self, value):
        """Set integer to widget."""
        try:
            int_val = int(value)
            self.tkvar.set(int_val)
            # self._entry.event_generate('<<mem_change>>')
        except ValueError:
            raise SetException()


class OTString(_OTEntry):
    """OTinteger variable."""

    def get(self):
        """Return python integer."""
        try:
            out = str(self.tkvar.get())
        except ValueError:
            raise GetException()
        return out

    def set(self, value):
        """Set integer to widget."""
        try:
            str_val = str(value)
            self.tkvar.set(str_val)
            # self._entry.event_generate('<<mem_change>>')
        except ValueError:
            raise SetException()


class OTNumber(_OTEntry):
    """OTNumber floats."""

    def get(self):
        """Return python integer."""
        try:
            out = float(self.tkvar.get())
        except ValueError:
            raise GetException()
        return out

    def set(self, value):
        """Set integer to widget."""
        try:
            float_val = float(value)
            self.tkvar.set(float_val)
            # self._entry.event_generate('<<mem_change>>')
        except ValueError:
            raise SetException()


class OTBoolean(LeafWidget):
    """OT booleans."""

    def __init__(self, schema, root_frame, name):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, root_frame, name)
        self.tkvar = BooleanVar()
        self._label.place(relx=0.5, rely=0.5, anchor="e")
        self._cbutt = ttk.Checkbutton(self._holder,
                                      variable=self.tkvar,
                                      command=self._callback_bool)
        self._cbutt.place(relx=0.5, rely=0.5, anchor="w")

    def get(self):
        """Return python boolean."""
        try:
            value = int(self.tkvar.get())
            out = bool(value)
        except ValueError:
            raise GetException()
        return out

    def set(self, value):
        """Set boolean to widget."""
        try:
            self.tkvar.set(value)
        except ValueError:
            raise SetException()

    def _callback_bool(self):
        """Event emission on radio change."""
        self._cbutt.event_generate('<<mem_change>>')


class OTChoice(LeafWidget):
    """OT choices widget."""

    def __init__(self, schema, root_frame, name, dynamic=False):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, root_frame, name)
        self.tkvar = StringVar()
        self._label.place(relx=0.5, rely=1, anchor="se")
        self.dynamic = dynamic
        if not self.dynamic:
            if len(schema["enum"]) > 3:
                self._pack_with_combobox(schema["enum"])
            else:
                self._pack_with_radiobuttons()
        else:
            pass

    def _pack_with_radiobuttons(self):
        """Radiobutton version of the widget"""
        n_lines = max(len(self.schema["enum"]), 1)
        self._holder.config(height=n_lines * LINE_HEIGHT)
        rel_step = 1./n_lines
        current_rely = 1*rel_step

        self._label.place(
            relx=0.5,
            rely=current_rely,
            anchor="se")

        titles = self.schema["enum"]
        if "enum_titles" in self.schema:
            titles = self.schema["enum_titles"]
        for value, title in zip(self.schema["enum"], titles):
            self.rad_btn = ttk.Radiobutton(
                self._holder,
                text=title,
                value=value,
                variable=self.tkvar,
                command=self._callback_choice)
            self.rad_btn.place(
                relx=0.5,
                rely=current_rely,
                anchor="sw")
            current_rely += rel_step

    def _pack_with_combobox(self, option):
        """Combobox version of the widget"""
        self.combo = ttk.Combobox(
            self._holder,
            values=option,
            textvariable=self.tkvar,
            postcommand=self._callback_choice)
        self.combo.place(relx=0.5, rely=1, anchor="sw")

    def _callback_choice(self):
        """Reaction to option change."""
        self._holder.event_generate('<<mem_change>>')

    def get(self):
        """Return python string."""
        out = self.tkvar.get()
        return out

    def set(self, value):
        """Set choice to widget."""
        if self.dynamic:
            tree = Nob(PARAMS["root"].get())
            key = self.schema["ot_dyn_choice"]
            options = tree[key][:]
            self._pack_with_combobox(options)

        self.tkvar.set(value)


class OTFileBrowser(LeafWidget):
    """OT file/folder browser widget."""

    def __init__(self, schema, root_frame, name):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, root_frame, name)
        self.tkvar = StringVar()
        self._filter = []
        self._isdirectory = False
        if 'ot_filter' in schema:
            filters = schema['ot_filter']
            if 'directory' in filters:
                self._isdirectory = True
            else:
                for ext in filters:
                    filetype = ("%s files" % ext, "*.%s" % (ext))
                    self._filter.append(filetype)

        self._label.place(relx=0.5, rely=0.5, anchor="e")

        self._path = ttk.Entry(self._holder,
                               textvariable=self.tkvar,
                               state='disabled',
                               foreground='black')
        self._path.place(relx=0.5, rely=0.5, relwidth=0.4, anchor="w")

        self._btn = ttk.Button(self._holder,
                               image=IMAGE_DICT['load'],
                               width=0.1*WIDTH_UNIT,
                               compound='left',
                               style='clam.TLabel',
                               command=self._browse)

        self._btn.place(relx=0.9, rely=0.5, anchor="w")

    def _browse(self, event=None):
        """Browse directory or files."""
        if self._isdirectory:
            path = filedialog.askdirectory(title=self._title)
        else:
            path = filedialog.askopenfilename(title=self._title,
                                              filetypes=self._filter)
        path = os.path.relpath(path)
        self.tkvar.set(path)

    def get(self):
        """Return data."""
        return self.tkvar.get()

    def set(self, value):
        """Set content."""
        self.tkvar.set(value)


class OTDocu(LeafWidget):
    """OTinteger variable."""

    def __init__(self, schema, root_frame, name):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, root_frame, name)
        self.tkvar = StringVar()
        self._btn = ttk.Button(self._holder,
                               width=0.01*WIDTH_UNIT,
                               compound='center',
                               image=IMAGE_DICT['docu'],
                               style='clam.TLabel',
                               command=self._popup_dialog)
        self._btn.place(relx=0.9, rely=0.5, anchor="center")
        self._holder.pack_configure(side="bottom", fill="x")

        self.parent = root_frame

        while self.parent.master is not None:
            self.parent = self.parent.master

        self._dialog = None

    def _popup_dialog(self):
        """Display content of documentation string."""
        self._dialog = Toplevel(self.parent)
        self._dialog.transient(self.parent)
        self._dialog.title('Documentation')
        self._dialog.grab_set()

        self._dialog.bind("<Control-w>", self._destroy_dialog)
        self._dialog.bind("<Escape>", self._destroy_dialog)
        self._dialog.protocol("WM_DELETE_WINDOW", self._destroy_dialog)

        dlg_frame = ttk.Frame(self._dialog,
                              width=3*WIDTH_UNIT,
                              height=3*WIDTH_UNIT)
        dlg_frame.pack(side="top", fill="both", expand=True)
        dlg_frame.grid_propagate(False)
        dlg_frame.grid_rowconfigure(0, weight=1)
        dlg_frame.grid_columnconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(dlg_frame)
        scrollbar.pack(side='right', fill='y')

        text_wd = Text(
            dlg_frame,
            wrap='word',
            yscrollcommand=scrollbar.set,
            borderwidth=0.02*WIDTH_UNIT,
            relief="sunken")

        # Example of formatting
        text_wd.tag_configure('bold', font=('Times', 14, 'normal'))
        text_wd.insert("end", self.tkvar, 'bold')
        text_wd.config(state='disabled')
        text_wd.pack()
        scrollbar.config(command=text_wd.yview)

    def _destroy_dialog(self, event=None):
        """Destroying dialog."""
        self.parent.focus_set()
        self._dialog.destroy()
        self._dialog = None

    def get(self):
        """Void return."""
        return None

    def set(self, value):
        """Set value to documentation content."""
        self.tkvar.set(value)


class OTDescription(LeafWidget):
    """OT descriptin field."""

    def __init__(self, schema, root_frame, name):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, root_frame, name)
        self.tkvar = StringVar()
        self._holder.pack_configure(side="bottom", fill="x")

        self._label = Label(
            self._holder,
            text=self._title,
            background=PARAMS["bg_lbl"],
            justify="right",
            wraplength=int(0.5*WIDTH_UNIT))

        self._label.config(justify="left",
                           textvariable=self.tkvar,
                           wraplength=WIDTH_UNIT*0.8)
        self._label.pack(side="bottom", fill="x")

    def get(self):
        """Return data."""
        return None

    def set(self, value):
        """Set content."""
        self.tkvar.set(value)


class OTComment(LeafWidget):
    """OT Comment field."""

    def __init__(self, schema, root_frame, name):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, root_frame, name)
        self.tkvar = StringVar()
        self._holder.pack_configure(side="top", fill="x")
        disabled = False
        height = 6
        if "state" in schema:
            if  schema["state"] == "disabled":
                disabled = True

        if "height" in schema:
            height = schema["height"]

        self.txt = TextConsole(self._holder,
                               self.tkvar,
                               height=height,
                               width=10,
                               disabled=disabled)

    def get(self):
        """Return data."""
        #self.tkvar.set(self.txt.get())
        return self.tkvar.get()

    def set(self, value):
        """Set content."""
        #nlines = value.split("\n")
        #print("Tile"+ self._title + "^^^^^")
        #print("updating line nb:"+ str(len(nlines)))
        self.tkvar.set(value)
        self.txt.update()


class OTEmpty(LeafWidget):
    """OT widget for unimplemented types."""

    def __init__(self, schema, root_frame, name):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, root_frame, name)

        self._label = Label(
            self._holder,
            text=self._title,
            background=PARAMS["bg_lbl"],
            justify="right",
            wraplength=int(0.5*WIDTH_UNIT))

        info = []
        for item in ["name", "title", "type", "ot_type"]:
            if item in schema:
                info.append(item + " = " + str(schema[item]))

        self._label.configure(text="\n".join(info))
        self._label.pack(side="top", padx=2, pady=2)
        # hide void strings for empty objects
        if "ot_type" in schema:
            if schema["ot_type"] == "void":
              #  self._label.forget()
              #  self._title.forget()
                self._holder.forget()

    def get(self):
        """Return data."""
        return None

    def set(self, value):
        """Set content."""


class OTList(LeafWidget):
    """Factory for OpenTea Lists."""

    def __init__(self, schema, root_frame, name):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        """
        super().__init__(schema, root_frame, name)
        self.variable = list()
        self.item_type = schema["items"]["type"]
        self.item_default = schema["items"]["default"]
        self.entrywidgets = list()
        self.resizable = True

        self._inits_list()

    def _inits_list(self):
        """Initialise entry."""

        self._status = Label(
            self._holder,
            text="",
            background=PARAMS["bg_lbl"],
            foreground="red",
            justify="left",
            compound="left",
            wraplength=WIDTH_UNIT,
            width=WIDTH_UNIT)
        self.entrylistholder = ttk.Frame(self._holder)
        self.entrylistholder.place(relwidth=0.5,
                                   relx=0.5,
                                   rely=0.0, anchor="nw")
        self._status.place(relwidth=0.9,
                           relx=0.9,
                           rely=1.0,
                           anchor="se")
        # force
        if "minItems" in self.schema:
            self.resizable = False
        if "maxItems" in self.schema:
            self.resizable = False
        if self.state == "disabled":
            self.resizable = False
        if self.resizable:
            self.additem_bt = ttk.Button(self._holder,
                                         text="+",
                                         command=self.additem)
            self.delitem_bt = ttk.Button(self._holder,
                                         text="-",
                                         command=self.delitem)

            self.additem_bt.place(relwidth=0.05,
                                  relx=0.95,
                                  rely=1.0, anchor="se")
            self.delitem_bt.place(relwidth=0.05,
                                  relx=1,
                                  rely=1.0, anchor="se")
        self._update_entrylist()

    def _update_entrylist(self):
        """Update entry list upon Tk variable."""
        for entries in self.entrywidgets:
            entries.destroy()
        self.entrywidgets = list()

        if self.state == "disabled":
            nlines = 6
            lbx = Listbox(
                self.entrylistholder,
                height=nlines)
            self.entrywidgets.append(lbx)
            for item in self.variable:
                lbx.insert("end", item)
            lbx.pack(side="top", fill="both")
            lbx.configure(
                state="disabled",
                highlightbackground=PARAMS["bg"],
                background=PARAMS["bg"],
                disabledforeground=PARAMS["bg_dark"])
        else:
            nlines = max(2, 1+len(self.variable))

            if not self.variable:
                self.entrywidgets.append(ttk.Label(self.entrylistholder,
                                                   text="void"))
                self.entrywidgets[-1].pack(side="top")
            else:
                for _ in self.variable:
                    self.entrywidgets.append(ttk.Entry(
                        self.entrylistholder))

                for i, entry in enumerate(self.entrywidgets):
                    entry.pack(side="top")
                    entry.insert(0, self.variable[i])
                    entry.bind("<Key>", self.memory_changed)
                    entry.bind("<Return>", self._single_entry_callback)
                    entry.bind("<Leave>", self._single_entry_callback)

        self._holder.config(height=nlines*LINE_HEIGHT)

    def memory_changed(self, event):
        """Trigger virtual event on memory change."""
        self.entrylistholder.event_generate('<<mem_change>>')

    def additem(self):
        """Add an item at the end of the array."""
        self.variable.append(self.item_default)

        self._update_entrylist()

    def delitem(self):
        """Delete item at the end of the array"""
        if self.variable:
            self._status.config(text='', image='')
            del self.variable[-1]
            self._update_entrylist()

    def _single_entry_callback(self, event):
        """Send the content of the list bact to the variable."""
        new_var = list()
        self.status = 1
        self._status.config(text='', image='')
        for entry in self.entrywidgets:
            value = entry.get()
            try:
                if self.item_type == "number":
                    value = float(value)
                elif self.item_type == "integer":
                    value = int(value)
            except ValueError:
                self.status = -1
                self._status.config(
                    text='Invalid input "%s"' % (value),
                    fg='red',
                    image=IMAGE_DICT['invalid'])
            new_var.append(value)

        if new_var != self.variable:
            self.variable = list(new_var)

    def get(self):
        """Return data."""
        return self.variable

    def set(self, value):
        """Set content."""
        self.variable = list(value)
        self._update_entrylist()

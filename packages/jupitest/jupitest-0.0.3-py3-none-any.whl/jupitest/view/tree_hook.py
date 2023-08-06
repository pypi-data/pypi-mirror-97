import tkinter as tk
from pyrustic.widget.tree import Hook


class TreeHook(Hook):
    def __init__(self, callback):
        self._callback = callback
        self._expander_stringvar = tk.StringVar()
        self._title_one_stringvar = tk.StringVar()
        self._title_two_stringvar = tk.StringVar()

    def on_build_node(self, tree, node, frame):
        self._tree = tree
        self._node = node
        title = node["title"]
        node_id = node["node_id"]
        node_type = node["data"]["type"]
        container = node["container"]
        # Titlebar
        titlebar = tk.Frame(frame)
        titlebar.grid(row=0, column=0, sticky="we")
        # Toolbar
        toolbar = tk.Frame(frame)
        toolbar.columnconfigure(0, weight=1)
        toolbar.grid(row=1, column=0, sticky="we")
        # expander
        if container:
            self._expander_stringvar.set("+")
            command = (lambda self=self,
                              node_id=node_id:
                       self._tree.collexp(node_id))
            expander = tk.Button(titlebar,
                                 name="treeExpanderButton",
                                 textvariable=self._expander_stringvar,
                                 command=command)
            expander.grid(row=0, column=0, sticky="w", padx=(0, 5))
        # titlelabel_one
        self._title_one_stringvar.set(node_type)
        titlelabel_one = tk.Label(titlebar,
                                  name="treeTitleLabelOne",
                                  textvariable=self._title_one_stringvar)
        titlelabel_one.grid(row=0, column=1, sticky="w", padx=(0, 5))
        # titlelabel_two
        self._title_two_stringvar.set(title)
        titlelabel_two = tk.Label(titlebar,
                                  name="treeTitleLabelTwo",
                                  textvariable=self._title_two_stringvar)
        titlelabel_two.grid(row=0, column=2, sticky="w")
        # binding command to titlebar, so callback will trigger toolbar
        command = (lambda event,
                          self=self,
                          toolbar=toolbar,
                          node=node: self._callback.on_title_clicked(node, toolbar))
        titlelabel_one.bind("<Button-1>", command)
        titlelabel_two.bind("<Button-1>", command)

    def on_display_node(self, tree, node):
        pass

    def on_destroy_node(self, tree, node):
        pass

    def on_collapse_node(self, tree, node):
        self._expander_stringvar.set("+")
        self._callback.on_node_collapsed(node)

    def on_expand_node(self, tree, node):
        self._expander_stringvar.set("-")
        self._callback.on_node_expanded(node)

    def on_feed_node(self, tree, node, *args, **kwargs):
        pass

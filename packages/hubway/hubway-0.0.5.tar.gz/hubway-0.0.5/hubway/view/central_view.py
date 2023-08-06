import tkinter as tk
from pyrustic.view import View
from pyrustic.widget.scrollbox import Scrollbox
from pyrustic.widget.tree import Tree
from hubway.view.tree_hook import TreeHook


class CentralView(View):
    def __init__(self, master, main_view, main_host):
        super().__init__()
        self._master = master
        self._main_view = main_view
        self._main_host = main_host
        self._body = None
        self._tree = None

    @property
    def tree_view(self):
        return self._tree

    @property
    def scrollbox(self):
        return self._scrollbox

    # ===============================
    #            PROPERTY
    # ===============================

    # ===============================
    #            PUBLIC
    # ===============================

    def add_node(self, owner, repo):
        self._main_host.update_activity("add", owner, repo)
        self._collapse_nodes()
        self._tree.feed(0, datatype="add_owner_repo",
                        data=(owner, repo))

    # ===============================
    #            LIFECYCLE
    # ===============================
    def _on_build(self):
        self._body = tk.Frame(self._master)
        # scrollbox
        self._scrollbox = Scrollbox(self._body, orient="v")
        self._scrollbox.pack(expand=1, fill=tk.BOTH)
        # tree
        self._tree = Tree(self._scrollbox.box,
                          spacing=15)
        self._tree.pack(expand=1, fill=tk.BOTH)
        hook = lambda self=self: TreeHook(self._main_view, self._main_host)
        self._tree.hook = hook


    def _on_display(self):
        # insert first node
        # insert ghost root node
        self._insert_ghost_root()
        # request last activity
        host = self._main_host.last_activity
        consumer = (lambda data, tree=self._tree:
                    tree.feed(0, datatype="last_activity", data=data))
        self._main_view.threadom.run(host, consumer=consumer)

    def _on_destroy(self):
        pass

    # ===============================
    #            PRIVATE
    # ===============================
    def _insert_ghost_root(self):
        # insert first node
        node_id = self._tree.insert()
        self._tree.ghost(node_id)

    def _collapse_nodes(self):
        for owner in self._tree.nodes:
            owner_node_id = owner["node_id"]
            if owner_node_id == 0:
                continue
            else:
                self._tree.collapse(owner_node_id)

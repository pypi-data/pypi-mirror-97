import tkinter as tk
from pyrustic.widget.tree import Hook
from hubway.view.node_view import NodeView


class TreeHook(Hook):
    def __init__(self, main_view, main_host):
        self._main_view = main_view
        self._main_host = main_host
        self._cache = {}

    # =============================
    #           PUBLIC
    # =============================


    # =============================
    #      IMPLEMENTATION OF HOOK
    # =============================
    def on_build_node(self, tree, node, frame):
        node_id = node["node_id"]
        if node_id == 0:
            return
        node_view = NodeView(frame, tree, self._main_view, self._main_host, node_id)
        node_view.build_pack(expand=1, fill=tk.X, side=tk.LEFT)
        tree.tag(node_id, data={"node_view": node_view})
        node_type = node["data"]["type"]
        if node_type in ("description", "latest_release", "total_downloads"):
            node_view.populate()

    def on_display_node(self, tree, node):
        pass

    def on_feed_node(self, tree, node, *args, **kwargs):
        datatype = kwargs.get("datatype")
        data = kwargs.get("data")
        if datatype == "last_activity":
            self._load_last_activity(node, data)
        elif datatype == "add_owner_repo":
            self._add_owner_repo(tree, *data)

    def on_expand_node(self, tree, node):
        node_id = node["node_id"]
        node_type = node["data"]["type"]
        node_view = node["data"].get("node_view", None)
        if node_view:
            node_view.edit_state(expanded=True)
        if node_type == "repo" and not tree.descendants(node_id):
            self._insert_repo_sub_nodes(tree, node_id)

    def on_collapse_node(self, tree, node):
        node_view = node["data"].get("node_view", None)
        if node_view:
            node_view.edit_state(expanded=False)

    # =============================
    #           PRIVATE
    # =============================
    def _load_last_activity(self, tree, data):
        for owner, repos in data.items():
            # add owner to tree
            data = {"type": "owner", "name": owner}
            node_id = tree.insert(parent=0, data=data, expand=True)
            for repo in repos:
                # add repo to owner
                data = {"type": "repo", "name": repo}
                tree.insert(parent=node_id, data=data)

    # ===================
    def _request_data(self, node, node_type, node_view):
        repo_node = node(node["parent"])
        owner_node = node(repo_node["parent"])
        repo = repo_node["data"]["name"]
        owner = owner_node["data"]["name"]
        threadom = self._main_view.threadom
        host_choice = {"description": self._main_host.repo_description,
                       "latest_release": self._main_host.latest_release,
                       "total_downloads": self._main_host.latest_releases_downloads}
        host = host_choice[node_type]
        host_args = (owner, repo)
        consumer = (lambda data, datatype=node_type,
                           node_view=node_view:
                    node_view.feed(datatype, data=data))
        threadom.run(host, target_args=host_args, consumer=consumer)

    def _add_owner_repo(self, tree, owner, repo):
        owner_node_id = self._add_owner(tree, owner)
        repo_node_id = self._add_repo(tree, owner_node_id, repo)
        # move owner node to top
        tree.move(owner_node_id)
        # expand owner node
        tree.expand(owner_node_id)
        # pull scrollbar to top
        self._main_view.central_view.scrollbox.yview_moveto(0)
        # expand repo
        tree.expand(repo_node_id)

    def _add_owner(self, tree, owner):
        node_id = None
        for node in tree.descendants(0):
            cache = node["data"]["name"]
            if cache.lower() == owner.lower():
                node_id = node["node_id"]
                return node_id
        # add owner to tree
        data = {"type": "owner", "name": owner}
        node_id = tree.insert(parent=0, data=data, expand=True, index=0)
        return node_id

    def _add_repo(self, tree, parent_node_id, repo):
        for node in tree.descendants(parent_node_id):
            cache = node["data"]["name"]
            if cache.lower() == repo.lower():
                node_id = node["node_id"]
                tree.delete(node_id)
        # add repo
        data = {"type": "repo", "name": repo}
        node_id = tree.insert(parent=parent_node_id, data=data, index=0)
        return node_id

    def _insert_repo_sub_nodes(self, tree, node_id):
        # insert Description Node
        data = {"type": "description", "name": "Repository description"}
        tree.insert(node_id, container=False, data=data)
        # insert Latest Release Node
        data = {"type": "latest_release", "name": "Latest release"}
        tree.insert(node_id, container=False, data=data)
        # insert Total Downloads Node
        data = {"type": "total_downloads", "name": "Latest ten (pre)releases"}
        tree.insert(node_id, container=False, data=data)

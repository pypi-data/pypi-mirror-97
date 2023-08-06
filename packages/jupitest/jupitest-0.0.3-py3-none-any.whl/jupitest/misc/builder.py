import os
import os.path
from pyrustic.threadom import Threadom
from jupitest.host.main_host import MainHost
from jupitest.host.result import Result
from jupitest.host.reloader import Reloader
from jupitest.view.log_window import LogWindow
from jupitest.view.toolbar import Toolbar
from pyrustic.widget.tree import Tree
from jupitest.view.main_view import MainView
from pyrustic.manager.misc import funcs


class MainHostBuilder:
    def build(self, root_path):
        return MainHost(root_path, Reloader(), ResultBuilder())


class ResultBuilder:
    def build(self, test_id, queue):
        return Result(test_id, queue)


class LogWindowBuilder:
    def build(self, master, message):
        return LogWindow(master, message).build_wait()


class ToolbarBuilder:
    def build(self, node_id, parent, callback):
        toolbar = Toolbar(node_id, parent, callback, LogWindowBuilder())
        toolbar.build()
        return toolbar


class TreeBuilder:
    def build(self, master, callback):
        return Tree(master, callback)


class MainViewBuilder:
    def build(self, app):
        #jasonix = funcs.get_manager_jasonix()
        #target = jasonix.data["target"]
        target = os.getcwd()
        tests_path = os.path.join(target, "tests")
        return MainView(app,
                        Threadom(app.root),
                        MainHostBuilder().build(target),
                        ToolbarBuilder(),
                        tests_path)

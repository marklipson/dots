import json
import os
import copy
import threading
import time


class Data(object):
    """
    A {}-like object that saves everything to disk.
    """
    def __init__(self, filename: str):
        self.filename = filename
        self.time_changed = None
        self.data = {}
        self.write_thread = threading.Thread(target=self.bg_write)
        self.running = True
        self.changed = False
        self.write_thread.start()

    def stop(self):
        self.running = False

    def bg_write(self):
        while self.running:
            time.sleep(0.1)
            if self.changed:
                self.save()

    def load(self):
        """
        Load data from disk if we haven't loaded it yet, or if it has changed there.
        """
        if os.path.exists(self.filename):
            t_mod = os.stat(self.filename).st_mtime
            print("load... %s / %s" % (t_mod, self.time_changed))
            if self.data is None or t_mod != self.time_changed:
                with open(self.filename, 'r') as f:
                    print("loading data from disk")
                    self.data = json.load(f)
                    self.time_changed = t_mod
        return self.data

    def save(self):
        """
        Save changes to disk.
        """
        to_save = json.dumps(copy.deepcopy(self.data))
        with open(self.filename, 'w') as f:
            f.write(to_save)
        self.time_changed = os.stat(self.filename).st_mtime
        self.changed = False

    def __setitem__(self, key, value):
        old = self.data.get(key)
        if value == old:
            return
        self.data.__setitem__(key, value)
        self.changed = True

    def __getitem__(self, item):
        self.load()
        return self.data.get(item)

    def get(self, item, default=None):
        self.load()
        return self.data.get(item, default)

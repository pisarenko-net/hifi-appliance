import os
import re
from pathlib import Path
import threading
import time

from filelock import FileLock
import pickledb

from ..config import DB_FILE_PATH
from ..config import DB_REBUILD_INTERVAL
from ..config import MUSIC_PATH_NAME


_TRACK_REGEX = re.compile(r'^\d\d .*\.flac$', re.IGNORECASE)


class TrackDB(object):
    def __init__(self):
        self._lock = FileLock('%s%s' % (DB_FILE_PATH, '.lock'))
        self._db = pickledb.load(DB_FILE_PATH, False)
        if not Path(DB_FILE_PATH).is_file():
            self.rebuild()

        self.updater = threading.Thread(
            target=self._rebuild_loop,
            name='db builder'
        )
        self.updater.daemon = True
        self.updater.start()

    def has_disc(self, disc_id):
        return self._db.exists(disc_id)

    def get_disc(self, disc_id):
        return self._db.get(disc_id)

    def store_disc(self, disc_id, disc_info):
        self._db.set(disc_id, disc_info)

    def persist(self):
        with self._lock:
            self._db().dump()

    def rebuild(self):
        discs = {}
        for root, _, files in os.walk(MUSIC_PATH_NAME):
            if '.disc_id' in files:
                disc_id = Path(root).joinpath('.disc_id').read_text().replace('\n', '')
                track_list = sorted([str(Path(root).joinpath(file)) for file in files if _TRACK_REGEX.match(file)])
                discs[disc_id] = {
                    'tracks': track_list
                }

        with self._lock:
            self._db.deldb()
            for disc_id in discs:
                self.store_disc(disc_id, discs[disc_id])
            self._db.dump()

    def _rebuild_loop(self):
        while True:
            time.sleep(DB_REBUILD_INTERVAL)
            self.rebuild()
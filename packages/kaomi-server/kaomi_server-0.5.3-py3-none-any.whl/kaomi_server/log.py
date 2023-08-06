import gzip
import os
import shutil

from logging import handlers

class CompressingRotatingFileHandler(handlers.RotatingFileHandler):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None

        if self.backupCount > 0:
            for i in range(self.backupCount - 1, 0, -1):
                sfn = self.rotation_filename("%s.%d.gz" % (self.baseFilename, i))
                dfn = self.rotation_filename("%s.%d.gz" % (self.baseFilename, i + 1))
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)
            dfn = self.rotation_filename(self.baseFilename + ".1")
            if os.path.exists(dfn):
                os.remove(dfn)
            self.rotate(self.baseFilename, dfn)
        if not self.delay:
            self.stream = self._open()


        log_dir = os.path.dirname(self.baseFilename)

        to_compress = [
            os.path.join(log_dir, f)
            for f in os.listdir(log_dir)
            if f.startswith(os.path.basename(os.path.splitext(self.baseFilename)[0])) and not f.endswith((".gz", ".log"))
        ]

        for f in to_compress:
            if os.path.exists(f):
                with open(f, "rb") as _old, gzip.open(f + ".gz", "wb") as _new:
                    shutil.copyfileobj(_old, _new)
                os.remove(f)
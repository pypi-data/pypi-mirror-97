from pythontools.core import logger
from threading import Thread
import time, traceback

_MANAGER = None
_CRONJOBS = []
_UPDATE_INTERVAL = 60

class CronJob:

    def __init__(self, name, interval, function, wait_for_last_job=True):
        self.name = name
        self.interval = interval
        self.function = function
        self.wait_for_last_job = wait_for_last_job
        self._current_thread = None
        self._last_run = 0

    def run(self):
        if self._current_thread is None:
            def _function(self):
                try:
                    self.function()
                except Exception as e:
                    logger.log("§cCronJob '" + self.name + "' throw exception: " + str(e))
                    traceback.print_exc()
                if self.wait_for_last_job is True:
                    self._current_thread = None
            self._current_thread = Thread(target=_function, args=[self])
            self._current_thread.start()
            self._last_run = time.time()
            if self.wait_for_last_job is False:
                self._current_thread = None

def registerCronJob(cronjob: CronJob):
    global _CRONJOBS, _MANAGER, _UPDATE_INTERVAL
    if cronjob.interval < _UPDATE_INTERVAL:
        _UPDATE_INTERVAL = cronjob.interval
    _CRONJOBS.append(cronjob)
    if _MANAGER is None:
        def _manager():
            while True:
                for job in _CRONJOBS:
                    if time.time() > job._last_run + job.interval:
                        job.run()
                time.sleep(_UPDATE_INTERVAL)
        _MANAGER = Thread(target=_manager)
        _MANAGER.start()
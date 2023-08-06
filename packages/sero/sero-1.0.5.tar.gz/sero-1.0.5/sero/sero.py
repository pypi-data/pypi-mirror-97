import sys
import time
import datetime as dt
import multiprocessing

from threading import Thread
from queue import Queue


MAX_THREADS = multiprocessing.cpu_count()


def parameterize(step, *params):
    if callable(step):
        def wrapper_func():
            return step(*params)

        wrapper_func.__name__ = 'parameterized_' + step.__name__

        return wrapper_func
    else:
        raise Exception('step must be callable')


class Pipeline:
    def __init__(self, logging_func=print, **kwargs):
        self._logging_func = logging_func
        self._steps = kwargs

    def execute(self, verbose=False):
        for step_num, (step, action) in enumerate(self._steps.items()):
            if verbose:
                self._log(f'Beginning {step}')

            if callable(action):
                action()
            elif isinstance(action, int):
                time.sleep(action)
            elif isinstance(action, list):
                self._run_actions(action, verbose)

    def _log(self, text):
        self._logging_func(f'[{dt.datetime.now()}]: {text}')

    def _run_actions(self, steps, verbose):

        exit_system = False
        still_threading = True

        def _run_concurrently():
            while still_threading:
                try:
                    queued_step = q.get()
                    if callable(queued_step):
                        if verbose:
                            self._log(f'Executing {queued_step.__name__}')
                        queued_step()
                    elif isinstance(queued_step, int):
                        if verbose:
                            self._log(f'Waiting for {queued_step} seconds...')
                        time.sleep(queued_step)
                except Exception as e:
                    if verbose:
                        self._log(e.with_traceback())
                    raise
                finally:
                    q.task_done()

        q = Queue(MAX_THREADS * 2)
        for _ in range(MAX_THREADS):
            thread = Thread(target=_run_concurrently)
            thread.daemon = True
            thread.start()

        try:
            for step in steps:
                q.put(step)
            q.join()
        except KeyboardInterrupt:
            exit_system = True
        except Exception as e:
            if verbose:
                self._log(e.with_traceback())
            raise
        finally:
            still_threading = False
            for _ in range(MAX_THREADS):
                q.put(None)

            if exit_system:
                sys.exit(0)

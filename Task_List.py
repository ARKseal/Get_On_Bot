import threading as _threading
import time as _time


class Tasklist(_threading.Thread):

    def __init__(self):
        super().__init__()
        self._check = True
        self._TASKS = {}
        self.start()

    def add(self, guild, task):
        if guild in self._TASKS:
            self._TASKS[guild].append(task)
        else:
            self._TASKS[guild] = [task]
        self._startTask(guild)
    
    def _startTask(self, guild):
        pass

    def _stopCheck(self):
        self._check = False

    def stop(self, guild):
        if guild not in self._TASKS: return
        for task in self._TASKS[guild]:
            if not task.done():
                task.cancel()

    def run(self):
        while True:
            if not self._check:
                break
            for key, tasks in self._TASKS.items():
                for task in tasks:
                    if task.done():
                        print('d')
                        self._TASKS[key].remove(task)
                    else:
                        print('nd')
            _time.sleep(5)
'''
class TEST(_threading.Thread):
    new_id = 0
    def __init__(self):
        super().__init__()
        self.id = TEST.new_id
        self.is_done = False
        self.start()
        TEST.new_id += 1
    
    def done(self):
        return self.is_done

    def run(self):
        _time.sleep(20)
        print("{} is done".format(self.id))
        self.is_done = True

t1 = TEST()
t2 = TEST()
t3 = TEST()

tsk = tasklist()

g1, g2, g3 = ('0', '1', '2')

for i in range(1, 4):
    eval(f'tsk.add(g{i}, t{i})')'''
import time, traceback, sys
from .core import Primitive, PyThread, synchronized
from .dequeue import DEQueue
from threading import Timer

class Task(Primitive):

    def __init__(self):
        Primitive.__init__(self)
        self._t_Started = None
        self._t_Ended = None
    
    #def __call__(self):
    #    pass

    def run(self):
        raise NotImplementedError
        
    @synchronized
    @property
    def started(self):
        return self._t_Started is not None
        
    @synchronized
    @property
    def running(self):
        return self._t_Started is not None and self._t_Ended is None
        
    @synchronized
    @property
    def ended(self):
        return self._t_Started is not None and self._t_Ended is not None
        
    @synchronized
    def start(self):
        self._t_Started = time.time()
        
    @synchronized
    def end(self):
        self._t_Ended = time.time()

class FunctionTask(Task):

    def __init__(self, fcn, *params, **args):
        Task.__init__(self)
        self.F = fcn
        self.Params = params
        self.Args = args
        
    def run(self):
        return self.F(*self.Params, **self.Args)
        
    
class TaskQueue(Primitive):
    
    class ExecutorThread(PyThread):
        def __init__(self, queue, task):
            PyThread.__init__(self, daemon=True)
            self.Queue = queue
            self.Task = task
            
        def run(self):
            task = self.Task
            task.start()
            try:
                if callable(task):
                    task()
                else:
                    task.run()
                task.end()
                self.Queue.taskEnded(self.Task)
            except:
                task.end()
                exc_type, value, tb = sys.exc_info()
                self.Queue.taskFailed(self.Task, exc_type, value, tb)
            finally:
                self.Queue.threadEnded(self)
                self.Queue = None
                    
    def __init__(self, nworkers, capacity=None, stagger=None, tasks = [], delegate=None):
        Primitive.__init__(self)
        self.NWorkers = nworkers
        self.Threads = []
        self.Queue = DEQueue(capacity)
        self.Held = False
        self.Stagger = stagger or 0.0
        self.LastStart = 0.0
        self.StartTimer = None
        self.Delegate = delegate
        for t in tasks:
            self.addTask(t)

    def addTask(self, task, timeout = None):
        #print "addTask() entry"
        self.Queue.append(task, timeout=timeout)
        #print "queue.append done"
        self.startThreads()
        return self
        
    def __iadd__(self, task):
        return self.addTask(task)
        
    def __lshift__(self, task):
        return self.addTask(task)
        
    def insertTask(self, task, timeout = None):
        self.Queue.insert(task, timeout = timeout)
        self.startThreads()
        return self
        
    def __rshift__(self, task):
        return self.insertTask(task)
        
    @synchronized
    def timer_fired(self):
        self.StartTimer = None
        self.startThreads()
        
    @synchronized
    def startThreads(self):
        #print "startThreads() entry"
        if not self.Held:
            while self.Queue \
                    and (self.NWorkers is None or len(self.Threads) < self.NWorkers) \
                    and not self.Held:
                if self.Stagger > 0.0:
                    delta = self.LastStart + self.Stagger - time.time()
                    #print "arming timer..."
                    if delta > 0.0:
                        if self.StartTimer is None:
                            self.StartTimer = Timer(delta, self.timer_fired)
                            self.StartTimer.daemon = True
                            self.StartTimer.start()
                        break
                # start next thread
                #print "staring thread..."
                self.LastStart = time.time()
                task = self.Queue.pop()
                t = self.ExecutorThread(self, task)
                t.kind = "%s.task" % (self.kind,)
                self.Threads.append(t)
                t.start()
        #print "startThreads() exit"
                   
            
    @synchronized
    def threadEnded(self, t):
        #print("queue.threadEnded: ", t)
        if t in self.Threads:
            self.Threads.remove(t)
        self.startThreads()
        self.wakeup()
        
    def taskEnded(self, task):
        if self.Delegate is not None:
            self.Delegate.taskEnded(self, task)
            
    def taskFailed(self, task, exc_type, exc_value, tb):
        if self.Delegate is None:
            sys.stdout.write("Exception in task %s:\n" % (task, ))
            traceback.print_exception(exc_type, exc_value, tb, file=sys.stderr)
        else:
            try:
                self.Delegate.taskFailed(self, task,  exc_type, exc_value, tb)
            except:
                traceback.print_exc(file=sys.stderr)
            
    @synchronized
    def tasks(self):
        return list(self.Queue.items()), [t.Task for t in self.Threads]
        
    @synchronized
    def activeTasks(self):
        return [t.Task for t in self.Threads]
        
    def nrunning(self):
        return len(self.Threads)
        
    def counts(self):
        return len(self.Queue), len(self.Threads)
        
    @synchronized
    def waitingTasks(self):
        return list(self.Queue.items())
        
    @synchronized
    def hold(self):
        self.Held = True
        
    @synchronized
    def release(self):
        self.Held = False
        self.startThreads()
        
    @synchronized
    def isEmpty(self):
        return len(self.Queue) == 0 and len(self.Threads) == 0
                
    def waitUntilEmpty(self):
        # wait until all tasks are done and the queue is empty
        if not self.isEmpty():
            while not self.sleep(function=self.isEmpty):
                pass
                
    join = waitUntilEmpty
                
    def drain(self):
        self.hold()
        self.waitUntilEmpty()
                
    @synchronized
    def flush(self):
        self.Queue.flush()
        self.wakeup()
            
    def __len__(self):
        return len(self.Queue)


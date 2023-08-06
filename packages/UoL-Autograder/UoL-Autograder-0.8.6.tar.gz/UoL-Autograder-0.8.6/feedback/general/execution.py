import subprocess
import threading
import psutil
import time
import os
from tempfile import TemporaryFile
from . import constants
from .util import decoder, dumb_decoder, read_from_start

pwd_imported = True
try:
    import pwd
except ModuleNotFoundError:
    pwd_imported = False

def setup_demotion(cwd, env):
    default_func = lambda: None

    env['LIBC_FATAL_STDERR_'] = "2" # Redirect c++ glibc backtraces. https://stackoverflow.com/questions/47741551/mysterious-linux-backtrace-and-memory-map

    try:
        pw_record = pwd.getpwnam(constants.RUNNER_USER)
    except KeyError:
        return env, default_func

    user_name = pw_record.pw_name
    user_home_dir = pw_record.pw_dir
    
    env['HOME']  = user_home_dir
    env['LOGNAME']  = user_name
    env['USER']  = user_name
    env['PWD']  = cwd

    subprocess.call([f"chown {constants.RUNNER_USER}: {cwd}"], shell=True)
    
    user_uid = pw_record.pw_uid
    user_gid = pw_record.pw_gid
    def demote():
        os.setgid(user_gid)
        os.setuid(user_uid)

    return env, demote

class ProcessOutOfMemoryError(Exception):
    def __init__(self):
        super().__init__("Total allowed memory usage exceeded by process")

class ProcessChildLimitHitError(Exception):
    def __init__(self):
        super().__init__("Total allowed number of child processes exceeded by process")

class ProcessOpenedSocketError(Exception):
    def __init__(self, conn=None):
        self.conn = conn
        super().__init__("Process attempted to open a socket connection")

class ProcessWatch(threading.Thread):
    # TODO: Write tests to cover this class
    def __init__(self, proc, memory_limit=-1, child_limit=-1, polling=0.05, allow_connections=False):
        threading.Thread.__init__(self)
        self._proc = proc
        self._memory_limit = memory_limit
        self._child_limit = child_limit
        self._polling = polling
        self._allow_connections = allow_connections
        self._pproc = psutil.Process(self._proc.pid)
        self.exception = None
        self.terminated = False
    
    def run(self):
        while self._pproc.is_running() and not self.terminated:
            children = []
            try:
                children = self._pproc.children(recursive=True)
            except psutil.NoSuchProcess:
                break

            if len(children) > self._child_limit and self._child_limit != -1:
                self.exception = ProcessChildLimitHitError()
                self.terminate_process()

            all_processes = [self._pproc] + list(children)
            rss, vms = 0, 0
            for p in all_processes:
                try:
                    mem = p.memory_info()
                    rss += mem[0]
                    vms += mem[1]
                except psutil.NoSuchProcess:
                    pass

            if (rss > self._memory_limit or vms > self._memory_limit) and self._memory_limit != -1:
                self.exception = ProcessOutOfMemoryError()
                self.terminate_process()

            conn = []
            try:
                conn = self._pproc.connections()
            except psutil.NoSuchProcess:
                pass
            except psutil.AccessDenied:
                pass

            if len(conn) > 0 and not self._allow_connections:
                print(conn)
                self.exception = ProcessOpenedSocketError(conn)
                self.terminate_process()
            
            time.sleep(self._polling)

    def terminate_process(self):
        try:
            children = self._pproc.children(recursive=True)
        except psutil.NoSuchProcess:
            return
        
        all_processes = [self._pproc] + list(children)
        for p in all_processes:
            try:
                p.kill()
            except psutil.NoSuchProcess:
                pass
            except psutil.AccessDenied:
                pass

    def terminate(self):
        self.terminated = True
        self.terminate_process()

class ExecuteResult:
    def __init__(self, retval, out, err, exception):
        self.retval = retval
        self.stdout = out
        self.stderr = err
        self.exception = exception

    def __repr__(self):
        return f"result: {self.retval}, {self.exception}\nstdout:\n{self.stdout}\nstderr:\n{self.stderr}"
    
    def sanitise_outputs(self, s, r=""):
        self.stdout = self.stdout.replace(s, r)
        self.stderr = self.stderr.replace(s, r)

def execute(args, working_dir, shell=False, timeout=None, env_add={}, child_limit=-1, memory_limit=constants.MAX_VIRTUAL_MEMORY, allow_connections=False):
    with TemporaryFile() as err, TemporaryFile() as out:
        env = {**os.environ.copy(), **env_add}

        if constants.IS_WINDOWS or not pwd_imported:
            proc = subprocess.Popen(args, cwd=working_dir, stderr=err, stdout=out, shell=shell, env=env)
        else:
            env, demote = setup_demotion(working_dir, env)
            proc = subprocess.Popen(args, cwd=working_dir, stderr=err, stdout=out, shell=shell, env=env, preexec_fn=demote)
        
        watch = ProcessWatch(
            proc, 
            memory_limit=memory_limit, 
            child_limit=child_limit, 
            allow_connections=allow_connections)
        watch.start()

        exception = None

        try:
            retval = proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired as e:
            proc.kill()
            retval = None
            exception = e
        
        out_raw = read_from_start(out)
        err_raw = read_from_start(err)

        watch.terminate()
        watch.join()
        
    if watch.exception:
        exception = watch.exception
        
    try:
        return ExecuteResult(
            retval,
            decoder(out_raw),
            decoder(err_raw),
            exception
        )
    except:
        return ExecuteResult(
            retval,
            dumb_decoder(out_raw),
            dumb_decoder(err_raw),
            exception
        )

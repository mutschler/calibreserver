#!/usr/bin/env python

""" pyservice module """

__author__ = 'Andrey Usov <http://devel.ownport.net>'
__version__ = '0.4.2'
__license__ = """
Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 'AS IS'
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE."""

__all__ = ['Process', 'Service']

import os
import sys
import time
import runpy
import errno
import signal
import atexit
import logging
import resource

# TODO support configuration file for service

sys.path.insert(0, os.getcwd())

# -----------------------------------------------------
#   classes
# -----------------------------------------------------
class Process(object):
    
    pidfile = None  # Override this field for your class
    logfile = None  # Override this field for your class
    
    def __init__(self):
        atexit.register(self.do_stop())
    
    def do_start(self):
        ''' You should override this method when you subclass Process. 
        It will be called before the process will be runned via Service class. '''
        pass

    def do_stop(self):
        ''' You should override this method when you subclass Process. 
        It will be called after the process has been stopped or interupted by 
        signal.SIGTERM'''
        pass
    
    def run(self):
        '''
        You should override this method when you subclass Process. 
        It will be called after the process has been daemonized by 
        start() or restart() via Service class.
        '''
        pass

class Service(object):
    ''' Service class  '''
    
    def __init__(self, process):
        ''' init '''
        
        self.process = process
        self.pidfile = Pidfile(process.pidfile)
        if process.logfile:
            set_logging(process.__name__, process.logfile)  
            self.logger = logging.getLogger(process.__name__)          


    def _fork(self, fid):
        ''' fid - fork id'''
        
        try: 
            pid = os.fork() 
        except OSError, e: 
            logging.error(
                "service._fork(), fork #%d failed: %d (%s)\n" % (fid, e.errno, e.strerror))
            raise OSError(e)  
        return pid
    
    def daemonize(self):
        '''
        do the UNIX double-fork magic, see Stevens' "Advanced 
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        '''

        def _maxfd(limit=1024):
            ''' Use the getrlimit method to retrieve the maximum file 
            descriptor number that can be opened by this process. If 
            there is not limit on the resource, use the default value
            
            limit - default maximum for the number of available file descriptors.
            '''
            maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
            if maxfd == resource.RLIM_INFINITY:
                return limit
            else:
                return maxfd
        
        def _devnull(default="/dev/null"):
            # The standard I/O file descriptors are redirected to /dev/null by default.
            if hasattr(os, "devnull"):
                return os.devnull
            else:
                return default

        def _close_fds(preserve=None):
            preserve = preserve or []
            for fd in xrange(0, _maxfd()):
                if fd not in preserve:
                    try:
                        os.close(fd)
                    except OSError: # fd wasn't open to begin with (ignored)
                        pass

        pid = self._fork(1) # first fork
        if pid == 0: # the first child
            os.setsid()
            pid = self._fork(2)
            if pid == 0: # the second child
                os.chdir("/") 
                os.umask(0) 
            else:
                os._exit(0)
            _close_fds(logging_file_descriptors())
        else:
            os._exit(0)             

        os.open(_devnull(), os.O_RDWR)
        os.dup2(0, 1)			# standard output (1)
        os.dup2(0, 2)			# standard error (2)

        return True
    
    def remove_pid(self):
        if self.pidfile.validate():
            self.pidfile.unlink()
        logging.info('the task completed, service was stopped')

    def start(self):
        '''
        Start the service
        '''
        
        # Check for a pidfile to see if the service already runs
        current_pid = self.pidfile.validate()
        if current_pid:
            message = "pidfile %s exists. Service is running already"
            logging.error(message % current_pid)
            print >> sys.stderr, message % current_pid
            return

        # Start the service
        if self.daemonize():
            # create pid file
            try:
                self.pidfile.create()
            except RuntimeError, err:
                logging.error('Error during service start, %s' % str(err))
                print >> sys.stderr, 'Error during service start, %s' % str(err)
                return
            # activate handler for stop the process
            atexit.register(self.remove_pid)

            try:            
                user_process = self.process()
                if getattr(user_process, 'do_start'):
                    user_process.do_start()
                user_process.run()
            except Exception, err:
                logging.error(err)
                print err
                return
            logging.info('process [%s] started' % self.process.__name__)
            print >> sys.stdout, 'process [%s] started' % self.process.__name__

    def stop(self):
        '''
        Stop the service
        '''
        pid = self.pidfile.validate()
        if not pid:
            message = "pidfile %s does not exist. Service is not running"
            logging.error(message % self.pidfile.fname)
            return # not an error in a restart

        # Try killing the service process    
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                self.pidfile.unlink()
            else:
                loggin.error('Error during service stop, %s' % str(err))
                raise OSError(err)
        logging.info('service [%s] was stopped by SIGTERM signal' % pid)
    
class ServiceControl(object):
    
    def __init__(self, process_path):
        self.process = load_process(process_path)
        if not callable(self.process):
            raise RuntimeError("The process {} is not valid".format(self.process_path))    
    
    def start(self):
        
        print "Starting process with {}...".format(self.process.__name__)
        Service(self.process).start()
                
    def stop(self):

        print "Stopping process {}...".format(self.process.__name__)
        Service(self.process).stop()
            
    def restart(self):

        self.stop()
        self.start()

    def status(self):
        srv = Service(self.process)
        pid = srv.pidfile.validate()
        if pid:
            try:
                os.kill(pid, 0)
                print 'Process {} is running, pid: {}'.format(srv.process.__name__, pid)
                return
            except (OSError, TypeError):
                pass
        print "Process is not running".format(srv.process.__name__)

#
#   Pidfile
#

class Pidfile(object):
    ''' Manage a PID file '''

    def __init__(self, fname):
        self.fname = fname
        self.pid = None

    def create(self):
        ''' create pid file '''
        pid = self.validate()
        if pid:
            if pid == os.getpid():
                return
            raise RuntimeError("Already running on PID %s " \
                "(or pid file '%s' is stale)" % (os.getpid(), self.fname))            
                
        self.pid = os.getpid()

        # Write pidfile
        fdir = os.path.dirname(self.fname)
        if fdir and not os.path.isdir(fdir):
            raise RuntimeError(
                    "%s doesn't exist. Can't create pidfile %s" % (fdir, self.fname))

        pfile = open(self.fname,'w')
        pfile.write("%s\n" % self.pid)
        pfile.close()

        # set permissions to -rw-r--r-- 
        os.chmod(self.fname, 420)
            
    def unlink(self):
        """ delete pidfile"""
        try:
            with open(self.fname, "r") as f:
                pid_in_file =  int(f.read() or 0)
            
            os.unlink(self.fname)
        except:
            pass

    def validate(self):
        """ Validate pidfile and make it stale if needed"""

        if not self.fname:
            return
        try:
            with open(self.fname, "r") as f:
                wpid = int(f.read() or 0)

                if wpid <= 0:
                    return

                try:
                    os.kill(wpid, 0)
                    return wpid
                except OSError, e:
                    if e[0] == errno.ESRCH:
                        return
                    raise
        except IOError, e:
            if e[0] == errno.ENOENT:
                return
            raise

# ---------------------------------------------------
#   Utils
# ---------------------------------------------------

#
#   Logging
#
        
DEFAULT_FORMAT = "%(asctime)s pid:%(process)d/{} <%(levelname)s> %(message)s"

def set_logging(process_name, logfile, output_format=DEFAULT_FORMAT, level=logging.DEBUG):
    ''' set logging '''
    output_format = output_format.format(process_name)
    logging.basicConfig(
                format=output_format, 
                filename = logfile, 
                level=logging.DEBUG)

def logging_file_descriptors():
    ''' logging file descriptors are used in core.Service.daemonize() '''
    return [handler.stream.fileno() for handler in [wr() for wr in
            logging._handlerList] if isinstance(handler, logging.FileHandler)]

#
#   Working with processes
#

def load_process(process_path):
    ''' load process 
    
    PEP 338 - Executing modules as scripts
    http://www.python.org/dev/peps/pep-0338
    '''
    if '.' not in process_path:
        raise RuntimeError("Invalid process path: {}".format(process_path))

    module_name, process_name = process_path.rsplit('.', 1)
    try:
        try:
            module = runpy.run_module(module_name)
        except ImportError:
            module = runpy.run_module(module_name + ".__init__")
    except ImportError, e:
        import traceback, pkgutil
        tb_tups = traceback.extract_tb(sys.exc_info()[2])
        if pkgutil.__file__.startswith(tb_tups[-1][0]):
            # If the bottommost frame in our stack was in pkgutil,
            # then we can safely say that this ImportError occurred
            # because the top level class path was not found.
            raise RuntimeError("Unable to load process path: {}:\n{}".format(process_path, e))
        else:
            # If the ImportError occurred further down,
            # raise original exception.
            raise
    try:
        return module[process_name]
    except KeyError, e:
        raise RuntimeError("Unable to find process in module: {}".format(process_path))
                    
def service(process=None, action=None):
    ''' control service '''
    try:
        getattr(ServiceControl(process), action)()
    except RuntimeError, e:
        print >> sys.stderr, e


def main():
    import argparse

    parser = argparse.ArgumentParser(prog="pyservice", add_help=False)
    parser.add_argument("-v", "--version",
        action="version", version="%(prog)s, v.{}".format(__version__))
    parser.add_argument("-h", "--help", 
        action="store_true", help="show program's help text and exit")
    parser.add_argument("process", nargs='?', help="""
        process class path to run (modulename.ProcessClass) or
        configuration file path to use (/path/to/config.py)
        """.strip())
    parser.add_argument("action", nargs='?', 
        choices="start stop restart status".split()) 
    
    try:        
        args = parser.parse_args()
    except TypeError:
        parser.print_help()
        return
        
    if args.help:
        parser.print_help()
        return

    if args.process and args.action in "start stop restart status".split():
        if not args.process:
            parser.error("You need to specify a process for {}".format(args.action))
        service(args.process, args.action)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()


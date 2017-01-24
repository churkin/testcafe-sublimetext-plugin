import sys
import subprocess
import os

def makeAbsolute(file_name, dirname):
    if dirname:
        localLookup = '(cd '+dirname+'; npm bin)'
    else:
        localLookup = 'npm bin'

    print(dirname)
    print(localLookup)

    proc = subprocess.Popen(localLookup + ' && npm bin -g', stdout=subprocess.PIPE, env=os.environ, shell=True)
    result = proc.communicate()[0]
    paths = result.decode('utf-8').strip().split('\n')
    localModulePath = os.path.join(paths[0], file_name)
    if os.path.isfile(localModulePath):
        return localModulePath
    return os.path.join(paths[1], file_name)


def run(cmd, dirname):
    proc = None

    if sys.platform == 'win32':
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    elif sys.platform == 'darwin':
        # https://github.com/int3h/SublimeFixMacPath
        proc = subprocess.Popen(['/usr/bin/login -fqpl $USER $SHELL -l -c \'' + cmd + '\''], stdout=subprocess.PIPE,
                                shell=True)
    elif sys.platform == 'linux':
        # TODO:
        cmd = cmd.split(' ')
        cmd[0] = makeAbsolute(cmd[0], dirname)
        cmd = ' '.join(cmd)
        print(cmd)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

    return proc


def kill(proc):
    if sys.platform == 'win32':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.Popen('taskkill /PID ' + str(proc.pid), startupinfo=startupinfo)
    else:
        try:
            proc.terminate()
        except:
            # ST2 on the Mac raises exception
            pass

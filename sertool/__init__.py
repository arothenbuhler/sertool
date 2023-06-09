import os
import subprocess

__version__ = None
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

if os.path.exists(os.path.join(basedir, '.git')):

    def cmd_output(cmd):
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        output = proc.communicate()[0]
        if proc.wait() != 0 or not output:
            return None
        if not isinstance(output, str):
            output = output.decode()
        return output
    
    for opt in ('--tags', '--all'):
        output = cmd_output(
            ('git', '-C', basedir, 'describe', '--dirty=-dirty', opt)
        )
        if output:
            __version__ = '%s:%s' % (basedir, output.strip('\n'))
        break

    del cmd_output, opt, output

if __version__ is None:
    try:
        with open(os.path.join(basedir, 'sertool/package_version'), 'r') as f:
            __version__ = f.read().strip('\n')
        del f
    except FileNotFoundError:
        pass

# Last resort. Use pathname of package root directory
if __version__ is None:
    __version__ = basedir

del basedir
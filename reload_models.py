import subprocess
import time

if __name__ == '__main__':
    ps = subprocess.Popen(('ps', 'aux'), stdout=subprocess.PIPE)
    output = subprocess.check_output(('grep', 'gunicorn: master'), stdin=ps.stdout)   
    ps.wait()
    pid = output.decode('utf-8').split()[1]
    print ('pid: %s' % pid) 
    subprocess.call(['kill', '-s', 'USR2', pid])
    time.sleep(600)
    subprocess.call(['kill', '-s', 'TERM', pid])
    """
    subprocess.call(['kill', '-s', 'TERM', pid])
    time.sleep(10)
    subprocess.call(['/data/category_suggestion/deployl.sh'])
    """

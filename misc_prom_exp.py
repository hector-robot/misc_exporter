#!/usr/bin/env python3
from prometheus_client import make_wsgi_app
from wsgiref.simple_server import make_server
import subprocess
import re
import platform

metrics_app = make_wsgi_app()

def my_app(environ, start_fn):
    if environ['PATH_INFO'] == '/metrics':
    #    return metrics_app(environ, start_fn)
        start_fn('200 OK', [])
        temp_command: str = "vcgencmd"
        temp_arg1: str = "measure_temp"
        temp_response: str
        if platform.machine() == "x86_64":
            temp_response = subprocess.check_output(['ssh', 'ubuntu@osd01.hq.vs', "sudo " + temp_command + " " + temp_arg1])
        else:
            temp_response = subprocess.check_output([temp_command, temp_arg1])
        p = re.compile('temp=(.*)\'C')
        m = p.match(temp_response.decode(encoding='UTF-8'))
        temp_output = 'main_temp ' + m.group(1) + "\nwife Megan"
        string_output = temp_output
        byte_output = string_output.encode(encoding='UTF-8')
        return [byte_output]
    elif environ['PATH_INFO'] == '/favicon.ico':
    #    return metrics_app(environ, start_fn)
        start_fn('200 OK', [])
        return [b'No Ico']

if __name__ == '__main__':
    httpd = make_server('', 8000, my_app)
    httpd.serve_forever()

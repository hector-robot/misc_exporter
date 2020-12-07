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
        vcgencmd_command: str = "vcgencmd"
        ### Temperature Section
        temp_arg1: str = "measure_temp"
        temp_response: str
        if platform.machine() == "x86_64":
            temp_response = subprocess.check_output(['ssh', 'ubuntu@osd01.hq.vs', "sudo " + vcgencmd_command + " " + temp_arg1])
        else:
            temp_response = subprocess.check_output([vcgencmd_command, temp_arg1])
        p = re.compile('temp=(.*)\'C')
        m = p.match(temp_response.decode(encoding='UTF-8'))
        temp_output = 'main_temp ' + m.group(1)
        ### Voltage Section
        volts_arg1: str = "measure_volts"
        volts_arg2: str = "core"
        temp_response: str
        if platform.machine() == "x86_64":
            volts_response = subprocess.check_output(['ssh', 'ubuntu@osd01.hq.vs', "sudo " + vcgencmd_command + " " + volts_arg1 + " " + volts_arg2])
        else:
            volts_response = subprocess.check_output([vcgencmd_command, volts_arg1, volts_arg2])
        p = re.compile('volt=(.*)V')
        m = p.match(volts_response.decode(encoding='UTF-8'))
        #volts_output = volts_response.decode(encoding='UTF-8')
        volts_output = 'core_volts ' + m.group(1)
        ### Consolidated Output
        string_output = temp_output + "\n" + volts_output
        byte_output = string_output.encode(encoding='UTF-8')
        return [byte_output]
    elif environ['PATH_INFO'] == '/favicon.ico':
    #    return metrics_app(environ, start_fn)
        start_fn('200 OK', [])
        return [b'No Ico']

if __name__ == '__main__':
    httpd = make_server('', 8000, my_app)
    httpd.serve_forever()

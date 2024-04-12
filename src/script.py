import subprocess

ports = [5000, 5001, 5002, 5003, 5004]

for port in ports:
    #subprocess.Popen(['start', 'cmd', '/k', 'python3', 'client_test.py', '-p', str(port)], shell=True)
    subprocess.run(["python3","client_test.py","-p",str(port)],capture_output=True)

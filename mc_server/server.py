from mc_server.mc_message import McMessage
import subprocess
import threading
import select
import time

class Server:
    def __init__(self, screen, log_path):
        self.screen = screen
        self.log_path = log_path
        self.events = []

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run_cmd(self, cmd):
        try:
            return subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError:
            print("Echec de la commande :" + cmd)

    def send(self, string):
        if len(string) > 600:
            length = 600
            chunks = [string[i:i + length] for i in range(0, len(string), length)]
            for chunk in chunks:
                chunk = chunk.replace('"', '\\"')
                self.run_cmd('screen -S %s -X stuff "%s"' % (self.screen, chunk))
            self.run_cmd('screen -S %s -X stuff "^M"' % self.screen)
        else:
            string = string.replace('"', '\\"')
            self.run_cmd('screen -p 0 -S %s -X stuff "%s $(printf \\\r)"' % (self.screen, string))

    def run(self):
        logfile = subprocess.Popen(['tail', '-f', '-n', '0', self.log_path],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        newlines = select.poll()
        while True:
            newlines.register(logfile.stdout)
            if newlines.poll(1):
                self.events.append(McMessage(logfile.stdout.readline()))
            time.sleep(0.05)

    def get_events(self):
        events = self.events
        self.events = []
        return events

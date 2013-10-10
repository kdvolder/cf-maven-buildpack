from subprocess import Popen
from subprocess import PIPE

class CurlCustomDownloader(object):
    def __init__(self, ctx):
        self._ctx = ctx

    def download(self, url, toFile):
        cmd = ["curl", "-s", "-L",
               "-o", toFile,
               "-w", "%{http_code}"]
        if url.find('download.oracle.com') >= 0:
            cmd.append("-H")
            cmd.append("Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2Ftechn"
                       "etwork%2Fjava%2Fjavase%2Fdownloads%2Fjdk7-downloads"
                       "-1880260.html;")
        cmd.append(url)
        proc = Popen(cmd, stdout=PIPE)
        output, unused_err = proc.communicate()
        proc.poll()
        if output and \
                (output.startswith('4') or
                 output.startswith('5')):
            raise RuntimeError("curl says [%s]" % output)
        print "Downloaded [%s] to [%s]" % (url, toFile)

import threading
import sys, os
import time
import unicodedata
from contextlib import contextmanager

@contextmanager
def spin(message):
    spin = SpinCursor(msg=message)
    spin.start()
    try:
        yield
    finally:
        spin.stop()


class SpinCursor(threading.Thread):
    """ A console spin cursor class """
    
    def __init__(self, msg='',maxspin=0,minspin=10,speed=5):
        # Count of a spin
        self.count = 0
        self.out = sys.stdout
        self.flag = False
        self.max = maxspin
        self.min = minspin
        # Any message to print first ?
        self.msg = msg
        # Complete printed string
        self.string = ''
        # Speed is given as number of spins a second
        # Use it to calculate spin wait time
        self.waittime = 1.0/float(speed*4)
        if os.name == 'posix':
            self.spinchars = (unicodedata.lookup('FIGURE DASH'),u'\\ ',u'| ',u'/ ')
        else:
            # The unicode dash character does not show
            # up properly in Windows console.
            self.spinchars = (u'-',u'\\ ',u'| ',u'/ ')        
        threading.Thread.__init__(self, None, None, "Spin Thread")
        
    def spin(self):
        """ Perform a single spin """

        for x in self.spinchars:
            self.string = self.msg + "...\t" + x + "\r"
            self.out.write(self.string)
            self.out.flush()
            time.sleep(self.waittime)

    def run(self):

        while (not self.flag):
            self.spin()
            self.count += 1

        # Clean up display...
        self.out.write(" "*(len(self.string) + 1))
        
    def stop(self):
        self.flag = True
        if self.is_alive():
            self.join()

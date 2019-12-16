import time
from threading import Thread
import sys
import random
import warnings
import hatespeech
import datetime

class Calculate(Thread):

    """Thread chargé simplement d'afficher une lettre dans la console."""

    def __init__(self, inputText):
        Thread.__init__(self)
        self.inputText = inputText

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        res = hatespeech.performFast(self.inputText)
        if(res == 0 or res == 2):
            print("banned")

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    threads = []
    while(True):
        date = datetime.datetime.now()
        hour = "["+str(date.hour)+":"+str(date.minute)+":"+str(date.second)+"]"
        message = input(hour+" Player  > ")
        thread = Calculate(message)
        threads.append(thread)
        thread.start()
        if(message == ""):
            break

    for thread in threads:
            thread.join()



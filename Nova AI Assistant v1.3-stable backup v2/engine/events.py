class EventManager:


    def __init__(self):

        self.events = []



    def push(self,event):

        self.events.append(event)



    def poll(self):

        events = self.events[:]

        self.events.clear()

        return events
class DelegateNotifier:
    def __init__(self):
        self.__subscribers = []

    def notify(self, *args, **kwargs):
        for subscriber in self.__subscribers:
            subscriber(*args, **kwargs)

    def subscribe(self, func):
        self.__subscribers.append(func)

property_value_delegate = DelegateNotifier()
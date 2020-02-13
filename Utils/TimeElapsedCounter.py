from datetime import datetime

class TimeElapsedCounter:

    def __init__(self):
        self.start_time = None
        self.stop_time = None
        self.is_started = False
        self.is_stoped = False
        self.elapsed_time = None

    def __enter__(self):
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def __str__(self):
        return str(self.get_elapsed_time())

    def start(self):
        if not self.is_started:
            self.start_time = datetime.now()
            self.is_started = True

        return self

    def stop(self):
        if self.is_started:
            self.stop_time = datetime.now()
            self.is_started = False
            self.is_stoped = True

            self.elapsed_time = self.stop_time - self.start_time

        return self

    def get_elapsed_time(self):
        if not self.is_started and self.is_stoped:
            return self. elapsed_time

    @staticmethod
    def run_time_measure(function):
        def wrapper(*args, **kwargs):
            time_differ = TimeElapsedCounter().start()

            wrapper_content = function(*args, **kwargs)
            print(kwargs)
            kwargs['self'].logger.info('Time needed to calculation: %s' % time_differ.stop().get_elapsed_time())

            args[0].logger.info('Time needed to calculation: %s' % time_differ.stop().get_elapsed_time())
            return wrapper_content

        return wrapper
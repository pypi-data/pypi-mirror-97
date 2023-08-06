import time
from functools import reduce
from operator import mul

class EtaPrinter():

    """Linear ETA (each step supposed taking the same time)"""
    def __init__(self, timezone=None):
        self.start_time = time.time()

    def print_eta(self, *tuples):
        """In : one or more pairs (tuples). Each tuple has 2 elements : [0] is progress, [1] is target (complete)
        Out : time as str in locale timezone
        """
        passed_steps_count, total_steps_count = count_steps(*tuples)

        # passed_steps_count = reduce(mul, map(lambda t : t[0], tuples))
        elapsed_time = time.time() - self.start_time

        if passed_steps_count == 0:
            return '--:--:--'


        #cross-product
        total_time = elapsed_time * total_steps_count / passed_steps_count

        eta_timestamp = self.start_time + total_time

        eta_struct = time.localtime(eta_timestamp)
        current_struct = time.localtime()

        eta_print = ''
        if eta_struct.tm_year > current_struct.tm_year:
            eta_print += str(eta_struct.tm_year) + ' '
        if eta_struct.tm_mon > current_struct.tm_mon or eta_struct.tm_mday > current_struct.tm_mday:
            eta_print += f"{eta_struct.tm_mday:02d}/{eta_struct.tm_mon:02d} "
        eta_print += f"{eta_struct.tm_hour:02d}:{eta_struct.tm_min:02d}:{eta_struct.tm_sec:02d}"

        return eta_print


def count_steps(*tuples):
    total_steps_count = reduce(mul, map(lambda t: t[1], tuples))
    passed_steps_count = 0
    for i, progress in enumerate(tuples):
        if i + 1 < len(tuples):
            underlying_steps_count = reduce(mul, map(lambda t: t[1], tuples[i + 1:len(tuples)]))
        else:
            underlying_steps_count = 1
        passed_steps_count += progress[0] * underlying_steps_count
    return passed_steps_count, total_steps_count


def get_progress_ratio(*tuples):
    """

    :param tuples:  Each tuple has 2 elements : [0] is progress, [1] is target (complete)
    :return: ratio of current progress out of total step count. You may want to apply to_progress() on it
    """
    passed_steps_count, total_steps_count = count_steps(*tuples)
    return passed_steps_count / total_steps_count
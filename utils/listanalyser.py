def decorate_list_in_iter(func):
    def shell_function(arg1, *arg2):
        iterable = iter(arg1)
        return func(iterable, *arg2)
    return shell_function

class ListAnalyser(object):

    def __init__(self):
        self._buffer = None

    @staticmethod
    def _is_keys_in_line(line, *keys):
        for key in keys:
            if key in line:
                return True
        return False

    @staticmethod
    def _skip_lines(iterable, number_of_lines):
        for i in range(number_of_lines):
            _ = next(iterable)
        return iterable

    def _is_key_in_list(self, iterable, *keys):
        for line in iterable:
            if self._is_keys_in_line(line, *keys):
                return True
        return False

    def _get_next_lines(self, iterable, number):
        if not self._buffer:
            self._buffer = []
        for i in range(number):
            try:
                self._buffer = next(iterable)
            except StopIteration:
                return
        return self._return_buffer()

    def _get_all_by_keys(self, iterable, *keys):
        for line in iterable:
            if not self._buffer:
                self._buffer = []
            self._buffer.append(line)
            if self._is_keys_in_line(line, *keys):
                try:
                    return self._return_buffer()
                except IndexError:
                    return
        return

    def _go_by_keys(self, iterable, *keys):
        for line in iterable:
            if self._is_keys_in_line(line, *keys):
                return line
        return

    def _keys_in_line(self, line, *keys):
        if self._is_keys_in_line(line, *keys):
            for key in keys:
                if key in line:
                    yield key
        return

    def _yield_part(self, iterable, start_keys, stop_keys):
        if not self._buffer:
            result = self._get_all_by_keys(iterable, *stop_keys)
            if not result and not self._buffer:
                yield result
            else:
                return
        while True:
            self._go_by_keys(iterable, *start_keys)
            result = self._get_all_by_keys(iterable, *stop_keys)
            if not result and not self._buffer:
                yield self._return_buffer()
            else:
                return

    def _get_all_by_end_and_keys(self, iterable, *keys):
        self._get_all_by_keys(iterable, *keys)
        return self._return_buffer()

    def _get_all_by_end(self, iterable):
        for l in iterable:
            self._buffer.append(l)
        return self._return_buffer()

    def _return_buffer(self):
        result = self._buffer
        self._buffer = None
        return result

def decorate_list_in_iter(func):
    def shell_function(arg1, *arg2):
        iterable = iter(arg1)
        return func(iterable, *arg2)
    return shell_function

def get_first_number(line: str):
    line = line.replace("=", "")
    line = line.replace(",", "")
    int_list = line.split()
    for i in int_list:
        try:
            return int(i)
        except:
            pass

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
                self._buffer.append(next(iterable))
            except StopIteration:
                return
        return self._return_buffer()

    def _get_all_by_keys(self, iterable, *keys):
        for line in iterable:
            if not self._buffer:
                self._buffer = []
            if self._is_keys_in_line(line, *keys):
                try:
                    return self._return_buffer()
                except IndexError:
                    return
            self._buffer.append(line)
        return

    def _get_all_if_keys(self, iterable, *keys):
        result = []
        for line in iterable:
            if self._is_keys_in_line(line, *keys):
                result.append(line)
            else:
                break
        return result

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


class ListReader(ListAnalyser):

    def __init__(self, iterable):
        super().__init__()
        self.iterable = iter(iterable)

    def add(self, iterable) -> None:
        self.iterable = iterable

    def get_all_by_end(self) -> list:
        return self._get_all_by_end(self.iterable)

    def get_all_by_end_and_keys(self, *keys) -> list:
        return self._get_all_by_end_and_keys(self.iterable, *keys)

    def go_by_keys(self, *keys) -> str:
        return self._go_by_keys(self.iterable, *keys)

    def yield_part(self, iterable, start_keys, stop_keys) -> list:
        yield from self._yield_part(self.iterable, start_keys, stop_keys)

    def get_next_lines(self, number) -> list:
        return self._get_next_lines(self.iterable, number)

    def get_all_by_keys(self, *keys) -> list:
        return self._get_all_by_keys(self.iterable, *keys)

    def get_all_if_keys(self, *keys):
        return self._get_all_if_keys(self.iterable, *keys)

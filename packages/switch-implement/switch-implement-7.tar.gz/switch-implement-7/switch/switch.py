# *-* coding utf-8 *-*

import re

class SwitchError(Exception): pass

class InvalidParameterError(SwitchError): pass

class sbreak(SwitchError):
    def __init__(self, switch):
        switch._breaked = True

class switch:
    def __init__(self, value, auto_break=False,
            comparator=lambda value, cases: \
                any(value == c for c in cases)
                    ):
        self._value = value
        self._auto_break = auto_break
        self._comparator = comparator
        self._switched = False
        self._breaked = False
        self._default_end = False
    @property
    def sbreak(self): # sbreak -> s break -> switch break
        return self._breaked
    @sbreak.getter
    def sbreak(self):
        self._breaked = True
        return self._breaked
    def fbreak(self): # fbreak -> f break -> function break
        return lambda: self.sbreak
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        return exc_type is SwitchError
    def __call__(self, case, *cases, sbreak=False, cmp=None):
        cases = (case,) + cases
        if cmp is None:
            comparator = self._comparator(self._value, cases)
        else:
            comparator = cmp(self._value, cases)
        return self.check(comparator, sbreak=sbreak)
    def case(self, case, *cases, sbreak=False, cmp=None):
        return self(case, *cases, sbreak=sbreak, cmp=cmp)
    def match(self, pattern, *patterns, sbreak=False):
        def match_test(value):
            v = str(value)
            all_regex = (re.compile(p) for p in (pattern,) + patterns)
            return any(r.match(v) for r in all_regex)
        return self.check(match_test, sbreak=sbreak)
    def check(self, test, sbreak=False):
        if self._default_end:
            raise SwitchError("you no can use default after a case")
        if callable(test):
            result = test(self._value)
        else:
            if isinstance(test, bool):
                result = test
            else:
                raise InvalidParameterError("error in the param test (pos 1). you needed give a callable object or bool")
        if result or self._switched and not self._breaked:
            self._switched = True
            if sbreak or self._auto_break:
                self.sbreak
            return True
        return False
    @property
    def default(self):
        self._default_end = True
        return not self._switched

class bswitch(switch): # bswitch -> b switch -> auto'B'reak switch
    def __init__(self, value, auto_break=True,
            comparator=lambda value, cases: \
                any(value == c for c in cases)
                ):
        super().__init__(value, auto_break=auto_break, comparator=comparator)



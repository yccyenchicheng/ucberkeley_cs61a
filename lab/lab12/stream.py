class Stream:
    empty = 'empty'
    def __init__(self, first, compute_rest=lambda: Stream.empty):
        self.first = first
        self.cached_rest = None
        assert callable(compute_rest)
        self.compute_rest = compute_rest
    @property
    def rest(self):
        """Return the rest, computing it if necessary."""
        if self.compute_rest is not None:
            self.cached_rest = self.compute_rest()
            self.compute_rest = None
        return self.cached_rest
    def __repr__(self):
        rest = self.cached_rest if self.compute_rest is None else '<Stream>'
        return 'Stream({}, {})'.format(self.first, rest)
def make_integer_stream(first=1):
    def compute_rest():
        return make_integer_stream(first+1)
    return Stream(first, compute_rest)
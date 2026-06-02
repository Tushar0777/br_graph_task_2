class RecomputeError(Exception):
    pass


class TransientRecomputeError(RecomputeError):
    pass


class PermanentRecomputeError(RecomputeError):
    pass
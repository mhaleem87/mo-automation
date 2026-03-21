import time


class TestResult:
    def __init__(self, category, test_name, status, severity, message, details=None, duration_ms=0):
        self.category = category
        self.test_name = test_name
        self.status = status  # pass, fail, warn, skip
        self.severity = severity  # info, low, medium, high, critical
        self.message = message
        self.details = details or {}
        self.duration_ms = duration_ms

    def to_dict(self):
        return {
            "category": self.category,
            "test_name": self.test_name,
            "status": self.status,
            "severity": self.severity,
            "message": self.message,
            "details": self.details,
            "duration_ms": self.duration_ms,
        }


class BaseTest:
    category = "general"

    def __init__(self, config, verbose=False):
        self.config = config
        self.verbose = verbose
        self.results = []

    def run(self):
        raise NotImplementedError

    def _timed(self, fn, *args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        elapsed_ms = int((time.time() - start) * 1000)
        return result, elapsed_ms

    def _add(self, test_name, status, severity, message, details=None, duration_ms=0):
        r = TestResult(self.category, test_name, status, severity, message, details, duration_ms)
        self.results.append(r)
        return r

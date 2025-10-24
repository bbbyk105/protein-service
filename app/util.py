import time, random, functools


def backoff(retries=3, base=0.5, factor=2.0):
    def deco(fn):
        @functools.wraps(fn)
        def wrap(*a, **kw):
            delay = base
            for i in range(retries):
                try:
                    return fn(*a, **kw)
                except Exception:
                    if i == retries - 1:
                        raise
                    time.sleep(delay + random.uniform(0, 0.25))
                    delay *= factor

        return wrap

    return deco


def uniq(seq):
    seen = set()
    out = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

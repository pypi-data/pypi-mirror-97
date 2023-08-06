def func_name(f):
    if hasattr(f, "__module__"):
        return "%s.%s" % (f.__module__, getattr(f, "__name__", f.__class__.__name__))
    return getattr(f, "__name__", f.__class__.__name__)

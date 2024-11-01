import importlib.util
import sys


def load_class_from_file(file_path, class_name):
    spec = importlib.util.spec_from_file_location("module_name", file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["module_name"] = module
    spec.loader.exec_module(module)

    cls = getattr(module, class_name)
    return cls()
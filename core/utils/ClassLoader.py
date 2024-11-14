import importlib.util
import sys
from typing import Optional


def load_class_from_file(file_path, class_name) -> Optional[object | None]:
    try:
        spec = importlib.util.spec_from_file_location("module_name", file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["module_name"] = module
        spec.loader.exec_module(module)

        cls = getattr(module, class_name)
        return cls()
    except Exception as e:
        print(e)
        print(f"Can't load python file {file_path} with name class {class_name}")
        return None
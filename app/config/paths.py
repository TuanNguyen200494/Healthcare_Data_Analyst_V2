from pathlib import Path

def find_root_project(path: Path|None = None):
    marker = "requirements.txt"
    if path is None:
        path  = Path.cwd()

    path = path.resolve()

    for path in [path,*path.parents]:
        if (path / marker).exists():
            return path
    raise FileNotFoundError("Không tìm thấy root project")
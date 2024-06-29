from pathlib import Path
from com_template import supported_languages

class Test:
    def __init__(self, input_, output):
        self.input = input_
        self.output = output

def verify_project():
    current = Path(".")
    bin_ = Path("./bin")
    tests = Path("./tests")

    has_main = any(current.joinpath(Path(f"main.{lang}")).is_file() for lang in supported_languages)
    return has_main and bin_.is_dir() and tests.is_dir()

def extract_language():
    current = Path(".")

    for lang in supported_languages:
        if current.joinpath(Path(f"main.{lang}")).is_file():
            return lang

def extract_tests():
    tests = Path("./tests/")

    found_tests = []

    for p in tests.glob("*.in"):
        if p.is_dir():
            continue

        found_tests.append(Test(p.absolute(), p.with_suffix(".out").absolute()))

    return sorted(found_tests, key=lambda t: t.input)

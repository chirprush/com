supported_languages = ["cpp", "py"]

template_languages = {
    "cf"    : "cpp",
    "usaco" : "cpp",
    "usacotrain"  : "cpp",
    "cfpy"  : "py",
    "python"  : "py",
    "usacopy"  : "py",
}

template_paths = {
    "cf" : "/home/rushil/Coding/olympiad/templates/template_cf.cpp",
    "usaco" : "/home/rushil/Coding/olympiad/templates/template_usaco.cpp",
    "usacotrain" : "/home/rushil/Coding/olympiad/templates/template_usacotraining.cpp",
    "cfpy" : "/home/rushil/Coding/olympiad/templates/template.py",
    "python" : "/home/rushil/Coding/olympiad/templates/template_blank.py",
    "usacopy" : "/home/rushil/Coding/olympiad/templates/template.py",
}

compile_commands = {
    "cpp" : ["g++", "-Wall", "main.cpp", "-o", "./bin/main"],
    "py"  : ["pylint", "main.py"], # Probably not needed but hey
}

run_commands = {
    "cpp" : ["./bin/main"],
    "py"  : ["python3", "main.py"]
}

for l in supported_languages:
    assert l in compile_commands and l in run_commands

for t in template_languages:
    assert t in template_paths

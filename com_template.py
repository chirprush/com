supported_languages = ["cpp"]

template_paths = {
    "cpp" : "/home/rushil/Coding/olympiad/templates/template.cpp"
}

compile_commands = {
    "cpp" : ["g++", "-Wall", "main.cpp", "-o", "./bin/main"]
}

run_commands = {
    "cpp" : ["./bin/main"]
}

for l in supported_languages:
    assert l in template_paths and l in compile_commands and l in run_commands

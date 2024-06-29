#!/usr/bin/env python3
from argparse import ArgumentParser
from sys import argv
from pathlib import Path
import shutil as sh
import subprocess as sub

from com_template import template_paths, template_languages, compile_commands, run_commands
from com_env import verify_project, extract_language, extract_tests

def do_test(args):
    current = Path(".")

    if verify_project():
        language = extract_language()
        tests = extract_tests()

        run_command = run_commands[language]
        
        passed = 0

        for j, test in enumerate(tests):
            with open(test.input, "r") as f:
                p = sub.run(run_command, stdin=f, capture_output=True, text=True)
            if p.returncode != 0:
                print("Failed at test {test.input.name}  (error while running)")
                print("Captured output from stderr:")
                print(p.stderr)
                return -1
            
            output_lines = p.stdout.split("\n")[:-1]

            with open(test.output, "r") as f:
                answer_lines = [l[:-1] for l in f.readlines()]

            max_length = max(len(output_lines), len(answer_lines))

            failed = False

            for i in range(max_length):
                got = output_lines[i] if i < len(output_lines) else ""
                expected = answer_lines[i] if i < len(answer_lines) else ""

                if got != expected:
                    failed = True
                    break

            if failed:
                print(f"Failed test {test.input.name} (input mismatch)")
                print(f"Expected output:")
                print("\n".join(answer_lines))

                print(f"\nGot instead:")
                print("\n".join(output_lines))
                print()
            else:
                print(f"Passed test {test.input.name}")
                passed += 1

        print()
        print(f"Passed {passed}/{len(tests)} tests")
        
        return int(passed == len(tests)) - 1
    else:
        print("You are not in a valid com directory")
        return -1

def do_check(args):
    current = Path(".")

    if verify_project():
        language = extract_language()
        compile_command = compile_commands[language]

        print("Checking...")
        print(" ".join(compile_command))
        p = sub.run(compile_command, capture_output=True, text=True)
        print()

        if p.returncode != 0:
            print("Compilation failed.")
            if p.stderr:
                print("\nCaptured output from stderr:")
                print(p.stderr)
            if p.stdout:
                print("\nCaptured output from stdout:")
                print(p.stdout)
            return -1
        else:
            print("All is A Okay")
            return 0
    else:
        print("You are not in a valid com directory")
        return -1

def do_run(args):
    current = Path(".")

    if verify_project():
        language = extract_language()
        compile_command = compile_commands[language]
        run_command = run_commands[language]

        print("Compiling...")
        print(" ".join(compile_command))
        p = sub.run(compile_command, capture_output=True, text=True)
        print()

        if p.returncode != 0:
            print("Compilation failed:")
            print(p.stderr)
            return -1
        else:
            print("Running...")
            print(" ".join(run_command))
            p = sub.run(run_command, text=True)

            return p.returncode
    else:
        print("You are not in a valid com directory")
        return -1

def do_create(args):
    project = Path(args.name)
    project.mkdir(parents=True, exist_ok=True)

    tests = project.joinpath(Path("tests"))
    tests.mkdir()

    bin_ = project.joinpath(Path("bin"))
    bin_.mkdir()

    if args.template not in template_languages:
        print(f"Could not find template \"{args.template}\". Make sure it's included in the com template paths")
        return -1

    main_name = f"main.{template_languages[args.template]}"
    sh.copy(template_paths[args.template], project.joinpath(Path(main_name)))

    return 0

parser = ArgumentParser(prog="com", description="A custom quality of life tool for competitive programming")

command_parser = parser.add_subparsers(title="commands", description="Valid actions", required=True)

test_parser = command_parser.add_parser("test")
test_parser.set_defaults(func=do_test)

# TODO: Add a feature so that one can overload which language
# is being used when compiling/running
check_parser = command_parser.add_parser("check")
check_parser.set_defaults(func=do_check)

run_parser = command_parser.add_parser("run")
run_parser.set_defaults(func=do_run)

create_parser = command_parser.add_parser("create")
create_parser.add_argument("name")
create_parser.add_argument("-t", "--template", default="cf")
create_parser.set_defaults(func=do_create)

namespace = parser.parse_args(argv[1:])

exit(namespace.func(namespace))

# TODO: Add some color I suppose

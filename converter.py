import re
import os

# --- Read rules.conf dynamically ---
rules = {}        # pattern -> list of replacement(s)
onstart_lines = []  # lines to run automatically

with open("rules.conf", "r") as f:
    for line in f:
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        if "->" in line:
            left, right = line.split("->", 1)
            pattern = left.strip()
            replacement = right.strip()
            if pattern == "onstart()":
                onstart_lines.append(replacement)
            else:
                if pattern not in rules:
                    rules[pattern] = []
                rules[pattern].append(replacement)

# --- Read Symple code from user ---
print("Enter your Symple code (type END to finish):")
code_lines = []
while True:
    line = input()
    if line.strip().upper() == "END":
        break
    code_lines.append(line)

# --- Output Python lines ---
output = []

# --- Add automatic onstart lines first ---
output.extend(onstart_lines)

# --- Function to convert a line based on rules ---
def convert_line(line):
    line = line.rstrip()
    output_lines = []

    for pattern, repl_list in rules.items():
        # build regex for placeholders
        tokens = pattern.split()
        regex = r"^"
        vars_ = []
        for token in tokens:
            if token.isupper():
                regex += r"(\S+)\s*"
                vars_.append(token)
            else:
                regex += re.escape(token) + r"\s*"
        regex += r"$"

        match = re.match(regex, line.strip())
        if match:
            for repl in repl_list:
                converted = repl
                for var, val in zip(vars_, match.groups()):
                    converted = converted.replace(var, val)
                output_lines.append(converted)
            return output_lines  # return all replacements

    # no match → return the line itself
    return [line]

# --- Process code lines ---
for line in code_lines:
    if line.strip() == "symple()":
        continue
    converted_lines = convert_line(line)
    if converted_lines:
        output.extend(converted_lines)

# --- Write output.py ---
with open("output.py", "w") as f:
    for l in output:
        f.write(l + "\n")
    f.write("\ninput('Press enter to continue...')\n")

# --- Run output.py ---
os.system("python output.py")

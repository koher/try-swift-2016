import re

def foo(line):
    time = None
    m = re.search(r"^\^ \(([0-9]+):([0-9]+), ([0-9]+):([0-9]+)\)", line)
    if m:
        time = int(m.group(3)) * 60 + int(m.group(4))
    elif re.search(r"^\^ \(", line):
        print("ERROR: " + line)
    return time, line

new_lines = []
with open('slides.md') as file:
    timed_lines = map(foo, file.readlines())
    current_time = 0
    for time, line in timed_lines:
        if time:
            minutes = current_time / 60
            seconds = current_time % 60
            new_lines.append(re.sub(r"^\^ \(([0-9]+):([0-9]+)", "^ (%d:%02d" % (minutes, seconds), line))
            current_time += time
        else:
            new_lines.append(line)

with open('slides.md', 'w') as file:
    file.writelines(new_lines)

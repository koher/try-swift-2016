import re

with open('slides.md') as file:
    lines = file.readlines()
    new_lines = filter(lambda(line): not re.search(r"^(\^|^autoscale:)", line), lines)

with open('codes.md', 'w') as file:
    file.writelines(new_lines)

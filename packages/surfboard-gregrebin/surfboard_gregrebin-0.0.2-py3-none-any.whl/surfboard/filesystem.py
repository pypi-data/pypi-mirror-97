from surfboard.project import Project
from typing import List
from csv import DictWriter, DictReader


def write(projects: List[Project], filename: str) -> None:
    print("Writing to file.")
    with open(filename, "w", newline="") as file:
        writer = DictWriter(file, fieldnames=Project.keys)
        writer.writeheader()
        writer.writerows([project.to_dict() for project in projects])


def read(filename: str) -> List[Project]:
    print("Reading file.")
    projects = []
    with open(filename) as file:
        clean_file = [line.replace("\0", "") for line in file]  # sometimes there may be NUL characters unreadable by CSV module, need to get rid of those
        reader = DictReader(clean_file)
        for row in reader:
            projects.append(Project.from_dict(row))
    return projects

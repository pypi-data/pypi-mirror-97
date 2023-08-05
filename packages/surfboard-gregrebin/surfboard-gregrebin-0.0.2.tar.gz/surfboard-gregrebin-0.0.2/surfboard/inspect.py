from surfboard.project import Project
from typing import List, Tuple, Callable, Dict


def count_by(projects: List[Project], key_type: str) -> List[Tuple[str, int]]:

    """Counts the quantity of projects for each key, keys can be project skills or groups,
    the type of key is specified by count_param, if provided an unsupported key type return the quantity of projects"""

    count = {}
    keys: Dict[str, Callable[[Project], List[str]]] = {
        "skill": lambda proj: proj.get_skills(),
        "group": lambda proj: [proj.group]
    }
    try:
        get_keys = keys[key_type]
    except KeyError:
        count = 0
        for _ in projects:
            count += 1
        return [("all", count)]

    for project in projects:
        for key in get_keys(project):
            if key in count:
                count[key] += 1
            else:
                count[key] = 1

    result = []
    for skill in count:
        result.append((skill, count[skill]))

    return sorted(result, key=lambda item: item[1])






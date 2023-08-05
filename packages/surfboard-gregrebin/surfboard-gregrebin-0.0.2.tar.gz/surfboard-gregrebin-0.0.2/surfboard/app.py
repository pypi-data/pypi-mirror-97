from surfboard.project import Project
from surfboard.exchanges import Freelancer
from surfboard.filesystem import read, write
from surfboard.inspect import count_by
from re import search
from typing import List, Dict, Tuple, NamedTuple, Callable


class FilterParams(NamedTuple):
    number: int
    keyword: str
    group: str
    skill: str
    category: str


class Application:
    """ Application state, contains a list of available freelance projects """

    count_params: Dict[str, Callable[[Project], List[str]]] = {
        "skill": lambda project: project.get_skills(),
        "group": lambda project: [project.group]
    }

    def __init__(self):
        self.projects: Dict[int, Project] = {}

    def load(self) -> None:
        """ Load projects from web """
        for project in Freelancer.freelancer_download():
            self.__add_project(project)

    def open(self, filename: str) -> None:
        """ Load projects from file """
        for project in read(filename):
            self.__add_project(project)

    def save(self, filename: str) -> None:
        """ Save projects to file """
        write(self.__all_projects(), filename)

    def list(self, params: FilterParams) -> List[Project]:
        """ List all projects """
        return self.__filter(params)

    def count(self, count_param: str, filter_params: FilterParams) -> List[Tuple[str, int]]:
        """ Count projects by parameter """
        try:
            return count_by(self.__filter(filter_params), count_param)
        except KeyError:
            return []

    def group_single(self, group_name: str, number: int):
        """ Assign single project to a group """
        self.projects[number].group = group_name

    def group_multi(self, group_name: str, force: bool, rewrite: bool, filter_params: FilterParams) -> None:
        """ Assign multiple projects to a group """
        for project in self.__filter(filter_params):
            if force or self.__belongs_to_group(project, group_name, rewrite):
                project.group = group_name

    @staticmethod
    def __belongs_to_group(project: Project, group_name: str, rewrite: bool) -> bool:
        """ Check if a projects belong to a group by checking for group name in the description """
        return (project.group == Project.default_group or rewrite) and search(group_name, project.description)

    def __filter(self, filter_params: FilterParams) -> List[Project]:
        """ Filter projects by number, keyword, group, skill or category and return the result """
        for project in self.projects.values():
            if ((filter_params.number is None or project.number == filter_params.number)
                    and (filter_params.keyword is None or search(filter_params.keyword, project.description))
                    and (filter_params.group is None or project.group == filter_params.group)
                    and (filter_params.skill is None or filter_params.skill in project.get_skills())
                    and (filter_params.category is None or filter_params.category in project.get_categories())):
                yield project

    def __all_projects(self) -> List[Project]:
        """ Return all projects as a list """
        return list(self.projects.values())

    def __add_project(self, project: Project) -> None:
        """ Add a project """
        self.projects[project.number] = project

from surfboard.exchanges import Freelancer
from surfboard.filesystem import read, write
from surfboard.inspect import count_by
from cmd import Cmd


class App(Cmd):
    intro = "Welcome to Surfboard, let's search for some job!"
    prompt = "(surfboard) "

    def __init__(self):
        super().__init__()
        self.projects_list = None
        self.skills = set()
        self.categories = set()

    def do_download(self, args):
        """Download a list of projects from freelancer.com"""
        self.projects_list = Freelancer.freelancer_download()

    def do_write(self, args):
        """Write the list of projects to the file"""
        write(self.projects_list, args)

    def do_read(self, args):
        """Read the list of projects from the file"""
        self.projects_list = read(args)

    def do_add_skill(self, args):
        """A new skill to the list of skills"""
        self.skills.add(args)

    def do_remove_skill(self, args):
        """Remove a skill from the list of skills"""
        self.skills.discard(args)

    def do_clear_skills(self, args):
        """Clear the list of skills"""
        self.skills.clear()

    def do_skills(self, args):
        """Show the list of skills"""
        print(self.skills)

    def do_add_category(self, args):
        """Add a new category to the list of categories"""
        self.categories.add(args)

    def do_remove_category(self, args):
        """Remove a category from the list of categories"""
        self.categories.discard(args)

    def do_clear_categories(self, args):
        """Clear the list of categories"""
        self.categories.clear()

    def do_categories(self, args):
        """Show the list of categories"""
        print(self.categories)

    def do_projects(self, args):
        """Show all projects for given skills and categories"""
        for project in self.projects_list:
            for skill in project.skills:
                if (skill.name in self.skills) or (skill.category in self.skills) or (len(self.skills) == 0 and len(self.categories) == 0):
                    print(project)
                    break

    def do_count_by_skill(self, args):
        """Count all projects by skill for given skills and categories"""
        projects_count = count_by(self.projects_list, lambda project: project.get_skills())
        for skill in projects_count:
            print(skill[0], skill[1])

    def do_quit(self, args):
        """Close the app"""
        return True


def run():
    app = App()
    app.cmdloop()


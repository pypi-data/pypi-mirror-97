from surfboard.project import Project, Skill, Budget
from typing import List
from freelancersdk.session import Session
from freelancersdk.resources.projects.projects import search_projects
from freelancersdk.resources.projects.helpers import create_search_projects_filter
from freelancersdk.resources.projects.helpers import create_get_projects_project_details_object


class Freelancer:

    @staticmethod
    def freelancer_project(project: dict) -> Project:
        return Project(
            number=project["id"],
            title=project["title"],
            description=project["description"],
            skills=[Skill(name=job["name"], category=job["category"]["name"]) for job in project["jobs"]],
            submit=project["submitdate"],
            currency=project["currency"]["code"],
            payment=project["type"],
            budget=Budget(minimum=project["budget"]["minimum"], maximum=project["budget"]["maximum"])
        )

    @staticmethod
    def freelancer_download() -> List[Project]:
        token = "NpgRpsRoAczwR9UNUzc7bAJgM5mTav"
        session = Session(oauth_token=token)
        search_filters = create_search_projects_filter(
            project_types=["fixed", "hourly"],
            min_avg_price=0.0,
            max_avg_price=10000.0,
            min_avg_hourly_rate=0.0,
            max_avg_hourly_rate=120.0,
            languages=["en", "it", "ru"],
            sort_field="time_updated",
            reverse_sort=False,
            jobs=None
        )
        project_details = create_get_projects_project_details_object(
            full_description=True,
            jobs=True,
        )
        page = 100
        count = 0
        terminated = False
        projects = []

        print("Downloading projects")

        while not terminated:
            response = search_projects(session, "", search_filter=search_filters, project_details=project_details,
                                       active_only=True, limit=page, offset=count)
            projects += [Freelancer.freelancer_project(project) for project in response["projects"]]
            count += len(response["projects"])
            terminated = count >= response["total_count"]

            print("Downloaded {} projects of {}".format(count, response["total_count"]))
            if terminated:
                print("Download complete.")

        return projects

from datetime import date
from typing import List, NamedTuple
from json import dumps, loads


class Skill(NamedTuple):
    name: str
    category: str

    def to_dict(self):
        return {"name": self.name, "category": self.category}

    @staticmethod
    def from_dict(dictionary):
        return Skill(name=dictionary["name"], category=dictionary["category"])


class Budget(NamedTuple):
    minimum: float
    maximum: float

    def to_dict(self):
        return {"minimum": self.minimum, "maximum": self.maximum}

    @staticmethod
    def from_dict(dictionary):
        return Budget(minimum=dictionary["minimum"], maximum=dictionary["maximum"])


class Project:
    keys = ["number", "title", "description", "skills", "submit", "currency", "payment", "budget", "group"]
    default_group = ""

    def __init__(self, number, title, description, skills, submit, currency, payment, budget, group=default_group):
        self.number: int = number
        self.title: str = title
        self.description: str = description
        self.skills: List[Skill] = skills
        self.submit: int = submit
        self.currency: str = currency
        self.payment: str = payment
        self.budget: Budget = budget
        self.group = group

    def __str__(self):
        return f"------- PROJECT -------\n" \
               f"{self.title}. Number {self.number}. Date {date.fromtimestamp(self.submit)}\n" \
               f"{self.budget.minimum} - {self.budget.maximum} {self.currency} {self.payment}\n" \
               f"{self.skills}\n" \
               f"{self.description}\n"

    def get_skills(self):
        return [skill.name for skill in self.skills]

    def get_categories(self):
        return [skill.category for skill in self.skills]

    def to_dict(self):
        dictionary = {
            "number": str(self.number),
            "title": self.title,
            "description": self.description,
            "skills": dumps([skill.to_dict() for skill in self.skills]),
            "submit": str(self.submit),
            "currency": self.currency,
            "payment": self.payment,
            "budget": dumps(self.budget.to_dict()),
            "group": self.group
        }
        return dictionary

    @staticmethod
    def from_dict(dictionary):
        project = Project(
            number=int(dictionary["number"]),
            title=dictionary["title"],
            description=dictionary["description"],
            skills=[Skill.from_dict(item) for item in loads(dictionary["skills"])],
            submit=int(dictionary["submit"]),
            currency=dictionary["currency"],
            payment=dictionary["payment"],
            budget=Budget.from_dict(loads(dictionary["budget"])),
            group=dictionary["group"]
        )
        return project



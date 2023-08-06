from jiraX.project import Project
from jiraX.issue import Issue
from jiraX.comment import Comment
from jiraX.role import Role
from jiraX.backlog import Backlog
from jiraX.sprintbacklog import SprintBacklog
from jiraX.board import Board
from jiraX.sprint import Sprint
from jiraX.user import User
import factory

class ProjectFactory(factory.Factory):
    class Meta:
        model = Project

    user = None
    apikey = None
    server = None

class IssueFactory(factory.Factory):
    class Meta:
        model = Issue

    user = None
    apikey = None
    server = None

class CommentFactory(factory.Factory):
    class Meta:
        model = Comment

    user = None
    apikey = None
    server = None

class RoleFactory(factory.Factory):
    class Meta:
        model = Role

    user = None
    apikey = None
    server = None

class BacklogFactory(factory.Factory):
    class Meta:
        model = Backlog

    user = None
    apikey = None
    server = None

class SprintBacklogFactory(factory.Factory):
    class Meta:
        model = SprintBacklog

    user = None
    apikey = None
    server = None

class BoardFactory(factory.Factory):
    class Meta:
        model = Board

    user = None
    apikey = None
    server = None

class SprintFactory(factory.Factory):
    class Meta:
        model = Sprint

    user = None
    apikey = None
    server = None

class UserFactory(factory.Factory):
    class Meta:
        model = User

    user = None
    apikey = None
    server = None


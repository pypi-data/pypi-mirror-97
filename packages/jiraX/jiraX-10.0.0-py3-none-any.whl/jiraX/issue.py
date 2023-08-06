import logging
logging.basicConfig(level=logging.INFO)
from .base import Base

class Issue(Base):
	"""
	Class responsable for documentation issues in Jira
	"""
	ERROR = "OS error: {0}"

	def __init__(self, user, apikey, server):
		Base.__init__(self, user, apikey, server)
		
	def find_by_id(self, issue_id): 
		"""
		Responsible for finding all infos from an issue

		Arguments:

			issue_id {Number} -- id of Jira issue

		Returns:
		
			Issue -- Issue object

		"""
		try:
			logging.info("Start function: find_by_id")
			return self.jira.issue(issue_id)
			logging.info("End function: find_by_id")
		except Exception as e: 
			logging.error(ERROR.format(e))
			logging.error(e.__dict__) 

	def find_by_sprint(self, sprint_id):
		"""
		Responsible for finding all issues from a sprint

		Arguments:

			sprint_id {Number} -- id of Jira Sprint

		Returns:
		
			List -- List of all issues from the given sprint

		"""
		try:
			logging.info("Start function: find_by_sprint")
			return self.jira.search_issues(f"Sprint={sprint_id}")
			logging.info("End function: find_by_sprint")
		except Exception as e: 
			logging.error(ERROR.format(e))
			logging.error(e.__dict__) 

	def find_by_project(self, project_key):
		"""
		Responsible for retreving all issue from a projects
		
		Arguments:

			project_key {String} -- project_key of Jira
		
		Returns:

			List -- Lits of issues of the given project
		
		"""
		try:
			logging.info("Start function: find_by_project")
			issues = self.jira.search_issues('project='+project_key, maxResults=100)
			tmp = issues
			contador = 100
			while(len(tmp) == 100):
				tmp = self.jira.search_issues(f'project = {project_key}', startAt=contador, maxResults=100)
				issues = issues + tmp
				contador = contador + 100
			return issues
			logging.info("End function: find_by_project")
		except Exception as e: 
			logging.error(ERROR.format(e))
			logging.error(e.__dict__) 

	def find_epic_by_project(self, project_key):
		"""
		Responsible for finding all project's epics that user has access

		Arguments:

			project_key {String} -- project_key of Jira

		Returns:
		
			List -- List of all issues from the given project with issuetype = 'Epic'

		"""
		return self.__find_all_issue(project_key, 'Epic')

	def find_story_by_project(self, project_key):
		"""
		Responsible for finding all project's storys that user has access

		Arguments:

			project_key {String} -- project_key of Jira

		Returns:
		
			List -- List of all issues from the given project with issuetype = 'Story'

		"""
		return self.__find_all_issue(project_key, 'Story')

	def find_task_by_project(self, project_key):
		"""
		Responsible for finding all project's tasks that user has access

		Arguments:

			project_key {String} -- project_key of Jira

		Returns:
		
			List -- List of all issues from the given project with issuetype = 'Task'

		"""
		return self.__find_all_issue(project_key, 'Task')

	def find_sub_task_by_project(self, project_key):
		"""
		Responsible for finding all project's sub-tasks that user has access

		Arguments:

			project_key {String} -- project_key of Jira

		Returns:
		
			List -- List of all issues from the given project with issuetype = 'Sub-task'

		"""
		return self.__find_all_issue(project_key, 'Sub-task')

	def find_bug_by_project(self, project_key):
		"""
		Responsible for finding all project's sub-tasks that user has access

		Arguments:

			project_key {String} -- project_key of Jira

		Returns:
		
			List -- List of all issues from the given project with issuetype = 'Sub-task'

		"""
		return self.__find_all_issue(project_key, 'Bug')


	def __find_all_issue(self, project_key, issue_type):
		try:
			logging.info("Start function: find_task")
			sub_tasks = self.jira.search_issues(f'project = {project_key} AND issuetype = {issue_type}',maxResults=100)
			tmp = sub_tasks
			contador = 100
			while(len(tmp) == 100):
				tmp = self.jira.search_issues(f'project = {project_key} AND issuetype = {issue_type}',startAt=contador,maxResults=100)
				sub_tasks = sub_tasks + tmp
				contador = contador + 100
			return sub_tasks
			logging.info("End function: find_task")
		except Exception as e: 
			logging.error(ERROR.format(e))
			logging.error(e.__dict__) 
import logging
logging.basicConfig(level=logging.INFO)
from .base import Base


class User(Base):
	"""
	Class responsable for documentation sprints backlog in Jira
	"""
	def __init__(self, user, apikey, server):
		Base.__init__(self, user, apikey, server)
		
	def find(self,id_or_key): 
		try:
			logging.info("Start function: find")
	
			#TO DO
	
			logging.info("End function: find")
		except Exception as e: # NOSONAR
			logging.error("OS error: {0}".format(e))# NOSONAR
			logging.error(e.__dict__) # NOSONAR

	def find_by_id(self, user_id):
		"""
		Responsible for finding all users that have access to the project

		Arguments:

			user_id {String} -- User's accountId from Jira

		Returns:
		
			User/None -- User if found

		"""
		try:
			logging.info("Start function: find_by_id")
			projects = self.jira.projects()
			for project in projects:
				users = self.jira.search_assignable_users_for_projects("", project.key, maxResults=100)
				for user in users:
					if user.accountId == user_id:
						return user
				tmp = users
				contador = 100
				while(len(tmp) == 100):
					tmp = self.jira.search_assignable_users_for_projects("", project_key, startAt=contador, maxResults=100)
					for user in tmp:
						if user.accountId == user_id:
							return user
					contador = contador + 100
			return None
			logging.info("End function: find_by_id")
		except Exception as e: # NOSONAR
			logging.error("OS error: {0}".format(e))# NOSONAR
			logging.error(e.__dict__) # NOSONAR

	def find_by_project(self, project_key):
		"""
		Responsible for finding all users that have access to the project

		Arguments:

			project_key {String} -- project_key of Jira

		Returns:
		
			List -- List of all Users with access to the project

		"""
		try:
			logging.info("Start function: find_by_project")
			users = self.jira.search_assignable_users_for_projects("", project_key, maxResults=100)
			tmp = users
			contador = 100
			while(len(tmp) == 100):
				tmp = self.jira.search_assignable_users_for_projects("", project_key, startAt=contador, maxResults=100)
				users = users + tmp
				contador = contador + 100
			return users
			logging.info("End function: find_by_project")
		except Exception as e: # NOSONAR
			logging.error("OS error: {0}".format(e))# NOSONAR
			logging.error(e.__dict__) # NOSONAR
	
	def find_by_project_key_and_accountId(self, project_key, user_id):
		"""
		Responsible for finding user that have access to the project

		Arguments:

			project_key {String} -- project_key of Jira

			user_id {String} -- accountId of Jira

		Returns:
		
			User/None -- User from jira if found

		"""
		try:
			logging.info("Start function: find_by_project_and_id")
			users = self.find_by_project(project_key)
			if users == None:
				return None
			for user in users:
				if user.accountId == user_id:
					return user
			return None
			logging.info("End function: find_by_project_and_id")
		except Exception as e: # NOSONAR
			logging.error("OS error: {0}".format(e))# NOSONAR
			logging.error(e.__dict__) # NOSONAR

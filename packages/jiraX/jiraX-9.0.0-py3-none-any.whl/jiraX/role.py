import logging
logging.basicConfig(level=logging.INFO)
from .base import Base

class Role(Base):
	"""
	Class responsable for documentation projects in Jira
	"""
	ERROR = "OS error: {0}"

	def __init__(self, user, apikey, server):
		Base.__init__(self, user, apikey, server)

	def find_by_proj_and_id(self, project_key, id):
		"""
		Responsible for finding project role with the given id

		Arguments:

			project_key {String} -- project_key of Jira

			id {Number} -- id of the role to get 

		Returns:
		
			Role -- Role object

		"""
		try:
			logging.info("Start function: find_by_proj_and_id")
			return self.jira.project_role(project_key, id)	
			logging.info("End function: find_by_proj_and_id")
		except Exception as e: 
			logging.error(ERROR.format(e))
			logging.error(e.__dict__) 

	def find_by_project(self, project_key):
		"""
		Responsible for finding all project's roles that user has access

		Arguments:

			project_key {String} -- project_key of Jira

		Returns:
		
			List -- List of all roles of the given project

		"""
		try:
			logging.info("Start function: find_by_project")
			return self.jira.project_roles(project_key)
			logging.info("End function: find_by_project")
		except Exception as e: 
			logging.error(ERROR.format(e))
			logging.error(e.__dict__) 


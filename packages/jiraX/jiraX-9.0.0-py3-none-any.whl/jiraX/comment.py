import logging
logging.basicConfig(level=logging.INFO)
from .base import Base

class Comment(Base):
	"""
	Class responsable for documentation comments in Jira
	"""
	ERROR = "OS error: {0}"

	def __init__(self, user, apikey, server):
		Base.__init__(self, user, apikey, server)
		
	def find_by_issue(self, issue_object): 
		"""
		Responsible for finding all comments from an issue

		Arguments:

			issue_object {Issue} -- issue of Jira

		Returns:
		
			List -- List of all comments from this issue
			
		"""
		try:
			logging.info("Start function: find_by_issue")
			comments = self.jira.comments(issue_object)
			if comments is not None:
				return comments
			return []
			logging.info("End function: find_by_issue")
		except Exception as e: 
			logging.error(ERROR.format(e))
			logging.error(e.__dict__) 
		

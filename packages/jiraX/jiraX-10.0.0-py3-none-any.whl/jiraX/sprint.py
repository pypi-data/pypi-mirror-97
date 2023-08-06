import logging
logging.basicConfig(level=logging.INFO)
from .base import Base

class Sprint(Base):
	"""
	Class responsable for documentation sprints in Jira
	"""

	def __init__(self, user, apikey, server):
		Base.__init__(self, user, apikey, server)
		
	def find_by_board(self, board_id):
		"""
		Responsible for finding all project's sprints that user has access

		Arguments:

			board_id {Number} -- board_id of Jira

		Returns:
		
			List -- List of all sprints of the given board

		"""
		try:
			logging.info("Start function: find_by_board")
			return self.jira.sprints(board_id)
			logging.info("End funcion: find_by_board")
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__)
	
	def find_by_id(self, sprint_id):
		"""
		Responsible for finding sprints with it's id

		Arguments:

			sprint_id {String} -- sprint_id of Jira

		Returns:
		
			Sprint/None -- Sprint if found

		"""
		try:
			logging.info("Start function: find_by_board")
			return self.jira.sprint(sprint_id)
			logging.info("End funcion: find_by_board")
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__)

    
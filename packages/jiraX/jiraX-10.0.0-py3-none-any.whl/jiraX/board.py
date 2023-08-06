import logging
logging.basicConfig(level=logging.INFO)
from .base import Base

class Board(Base):
	"""
	Class responsable for documentation boards in Jira
	"""
	ERROR = "OS error: {0}"

	def __init__(self, user, apikey, server):
		Base.__init__(self, user, apikey, server)
		
	def find_by_project(self, project_key):
		"""
		Responsible for finding all project's boards that user has access

		Arguments:

			project_key {String} -- project_key of Jira

		Returns:
		
			List -- List of all boards from the given project
			
		"""
		try:
			logging.info("Start function: find_by_project")
			return self.jira.boards(projectKeyOrID=project_key)
			logging.info("End funcion: find_by_project")
		except Exception as e:
			logging.error(ERROR.format(e))
			logging.error(e.__dict__)

	def find_by_id(self, board_id):
		"""
		Responsible for a board with given id

		Arguments:

			board_id {String} -- board_id of Jira

		Returns:
		
			Board/None -- Board if found
			
		"""
		try:
			logging.info("Start function: find_by_project")
			boards = self.jira.boards()
			if boards is None:
				return None
			for board in boards:
				if board.id == board_id:
					return board
			logging.info("End funcion: find_by_project")
		except Exception as e:
			logging.error(ERROR.format(e))
			logging.error(e.__dict__)
    


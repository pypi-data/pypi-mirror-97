import logging
logging.basicConfig(level=logging.INFO)
from .base import Base

class Project(Base):
	"""
	Class responsable for documentation projects in Jira
	"""
	ERROR = "OS error: {0}"
	
	def __init__(self, user, apikey, server):
		Base.__init__(self, user, apikey, server)
	
	def find_all(self): 
		"""
		Responsible for retreving information about projects

		Returns:
		
			List -- Lits of projects

		"""
		try:
			logging.info("Start function: find_all")
			return self.jira.projects()	
			self.jira.__init__
			logging.info("End function: find_all")
		except Exception as e: 
			logging.error(ERROR.format(e))
			logging.error(e.__dict__) 

	def find_by_key(self, project_key):
		"""
		Responsible for finding project with the given key

		Arguments:

			project_key {String} -- project_key of Jira

		Returns:
		
			Project -- Project object

		"""
		try:
			logging.info("Start function: find_by_key")
			return self.jira.project(project_key)
			logging.info("End funcion: find_by_key")
		except Exception as e:
			logging.error(ERROR.format(e))
			logging.error(e.__dict__)
	
	def find_by_id(self, project_id):
		"""
		Responsible for finding project with the given id

		Arguments:

			project_id {int} -- project_id of Jira

		Returns:
		
			Project -- Project object

		"""
		try:
			logging.info("Start function: find_by_id")
			return self.jira.project(project_id)
			logging.info("End funcion: find_by_id")
		except Exception as e:
			logging.error(ERROR.format(e))
			logging.error(e.__dict__)

	def find_by_board_id(self, board_id):
		"""
		Responsible for finding project with the board id

		Arguments:

			board_id {int} -- board_id of Jira

		Returns:
		
			Project -- Project object

		"""
		try:
			logging.info("Start function: find_by_board_id")
			boards = self.jira.boards()
			if boards is None:
				return None
			for board in boards:
				if board.id == board_id:
					return self.find_by_id(board.raw['location']['projectId'])
			logging.info("End funcion: find_by_board_id")
		except Exception as e:
			logging.error(ERROR.format(e))
			logging.error(e.__dict__)
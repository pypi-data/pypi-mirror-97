import logging
logging.basicConfig(level=logging.INFO)
from jira import JIRA

class Base():
	"""
	Class responsable for connect to Jira
	"""
	def __init__(self, user, apikey, server):
		
		options = {
		'server': server,
		'agile_rest_path': 'agile'
		}
		self.jira = JIRA(options, basic_auth=(user,apikey))

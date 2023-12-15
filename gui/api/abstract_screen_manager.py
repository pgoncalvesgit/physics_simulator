from abc import abstractmethod


def test():
	print("yes")


class AbstractScreenManager:

	@abstractmethod
	def new_screen(self, width: int, height: int):
		pass

	@abstractmethod
	def close_screen(self, index: int):
		pass

	@abstractmethod
	def run(self):
		pass

	def __init__(self):
		print("worked")

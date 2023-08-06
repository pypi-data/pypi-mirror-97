__version__ = '0.1.0'


presets = {'greetings': ['hello', 'hi', 'good morning', 'good afternoon', 'good evening', 'howdy', 'nice to meet you']}
class Trainer():
	def __init__(self, name, bot_presets=[]):
		'''
		Creates the bot.
		name: name of the bot
		bot_presets: pre-made data that the bot can come with. Current presets are:
		- greetings
		'''
		self.name = name
		self.trained = {'same': [], 'conversations': []}
		for preset in bot_presets:
			if preset in presets:
				self.trained['same'][preset] = presets[preset]
			else:
				raise AttributeError(preset + ' is not a valid preset.')
	def train(self, info):
		'''
		Trains the bot.
		'''

		self.trained['same'].append(info)






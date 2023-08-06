def prefix(name, prefix):
	return f'{name} = commands.Bot(command_prefix = "{prefix}")'

def start(name, token):
	return f'{name}.run("{token}")'

def remove_help(name):
	return f'{name}.remove_command("help")'


if __name__ == '__main__':
	print('import module')
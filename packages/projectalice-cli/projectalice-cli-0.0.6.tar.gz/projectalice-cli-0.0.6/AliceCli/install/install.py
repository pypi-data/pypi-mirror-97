from pathlib import Path
from typing import Tuple

import click
import yaml
from PyInquirer import prompt
import requests

from AliceCli.utils import commons
from AliceCli.utils.decorators import checkConnection


@click.command(name='installAlice')
@click.option('--force', '-f', is_flag=True)
@click.pass_context
@checkConnection
def installAlice(ctx: click.Context, force: bool):
	click.secho('\nInstalling Alice, yayyyy!', color='yellow')

	questions = [
		{
			'type': 'password',
			'name': 'adminPinCode',
			'message': 'Enter an admin pin code. It must be made of 4 characters, all digits only. (default: 1234)',
			'default': '1234',
			'validate': lambda code: code.isdigit() and int(code) < 10000
		},
		{
			'type'    : 'input',
			'name'    : 'mqttHost',
			'message' : 'Mqtt host:',
			'default' : 'localhost',
			'validate': lambda string: len(string) > 0
		},
		{
			'type'    : 'input',
			'name'    : 'mqttPort',
			'message' : 'Mqtt port:',
			'default' : '1883',
			'validate': lambda port: port.isdigit()
		},
		{
			'type'    : 'list',
			'name'    : 'activeLanguage',
			'message' : 'What language should Alice be using?',
			'default' : 'en',
			'choices' : [
				'en',
				'de',
				'fr',
				'it'
			]
		},
		{
			'type'    : 'input',
			'name'    : 'activeCountryCode',
			'message' : 'What country code should Alice be using?',
			'default' : 'US',
			'validate': lambda string: len(string) > 0
		}
	]

	answers = prompt(questions)
	if len(answers) < 5:
		commons.returnToMainMenu(ctx)
		return

	commons.waitAnimation()
	confFile = Path(Path.home(), '.pacli/projectalice.yaml')
	confFile.parent.mkdir(parents=True, exist_ok=True)

	try:
		with requests.get(url='https://raw.githubusercontent.com/project-alice-assistant/ProjectAlice/master/ProjectAlice.yaml', stream=True) as r:
			r.raise_for_status()
			with confFile.open('wb') as fp:
				for chunk in r.iter_content(chunk_size=8192):
					if chunk:
						fp.write(chunk)
	except Exception as e:
		commons.printError(f'Failed downloading ProjectAlice.yaml {e}')
		commons.returnToMainMenu(ctx)

	with confFile.open(mode='r') as f:
		try:
			confs = yaml.safe_load(f)
		except yaml.YAMLError as e:
			commons.printError(f'Failed reading projectalice.yaml {e}')
			commons.returnToMainMenu(ctx)

	confs['adminPinCode'] = int(answers['adminPinCode'])
	confs['mqttHost'] = answers['mqttHost']
	confs['mqttPort'] = int(answers['mqttPort'])
	confs['activeLanguage'] = answers['activeLanguage']
	confs['activeCountryCode'] = answers['activeCountryCode']

	with confFile.open(mode='w') as f:
		yaml.dump(confs, f)

	commons.printSuccess('Generated ProjectAlice.yaml')

	sshCmd('sudo apt-get update')
	sshCmd('sudo apt-get install git -y')
	sshCmd('git config --global user.name "An Other"')
	sshCmd('git config --global user.email "anotheruser@projectalice.io"')

	result = sshCmdWithReturn('test -d ~/ProjectAlice/ && echo "1"')[0].readline()
	if result:
		if not force:
			commons.printError('Alice seems to already exist on that host')
			answer = prompt(questions={
				'type': 'confirm',
				'message': 'Erase and reinstall',
				'name': 'confirm',
				'default': False
			})
			if not answer['confirm']:
				commons.returnToMainMenu(ctx)
				return

		commons.waitAnimation()
		sshCmd('sudo systemctl stop ProjectAlice')
		sshCmd('sudo rm -rf ~/ProjectAlice')

	sshCmd('git clone https://github.com/project-alice-assistant/ProjectAlice.git ~/ProjectAlice')
	sshCmd('git -C ~/ProjectAlice submodule init')
	sshCmd('git -C ~/ProjectAlice submodule update')
	sshCmd('git -C ~/ProjectAlice submodule foreach git checkout builds_master')
	sshCmd('git -C ~/ProjectAlice submodule foreach git pull')
	sshCmd(f'echo "{confFile.read_text()}" > ~/ProjectAlice/ProjectAlice.yaml')
	sshCmd('sudo cp ~/ProjectAlice/ProjectAlice.yaml /boot/ProjectAlice.yaml')
	sshCmd('python3 ~/ProjectAlice/main.py')

	commons.printSuccess('Alice is installing!')
	commons.returnToMainMenu(ctx)


def sshCmd(cmd: str):
	stdin, stdout, stderr = commons.SSH.exec_command(cmd)
	while line := stdout.readline():
		click.secho(line, nl=False, color='yellow')


def sshCmdWithReturn(cmd: str) -> Tuple:
	stdin, stdout, stderr = commons.SSH.exec_command(cmd)
	return stdout, stderr

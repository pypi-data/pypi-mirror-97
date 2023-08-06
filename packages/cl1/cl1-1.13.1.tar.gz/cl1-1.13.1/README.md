# CL1
Author(s):  Daan van den Bergh<br>
Copyright:  © 2020 Daan van den Bergh All Rights Reserved<br>
<br>
<br>
<p align="center">
  <img src="https://raw.githubusercontent.com/vandenberghinc/public-storage/master/vandenberghinc/icon/icon.png" alt="Bergh-Encryption" width="50"/>
</p>

## Installation
	pip3 install cl1

## Simple Example.

Simple cli.CLI code example.

```python
# the cli object class.
class CLI(cl1.CLI):
	def __init__(self):
		
		# defaults.
		cl1.CLI.__init__(self,
			modes={
				"--config":"Edit the ssht00ls configuration file (nano).",
				"-h / --help":"Show the documentation.",
			},
			alias="ssht00ls",
			executable=__file__,
		)

		#
	def start(self):
		
		# check arguments.
		self.arguments.check()

		# help.
		if self.arguments.present(['-h', '--help']):
			self.docs(success=True)

		# config.
		elif self.arguments.present('--config'):
			os.system(f"nano {CONFIG.file_path.path}")

		# invalid.
		else: self.invalid()

		#

# main.
if __name__ == "__main__":
	cli = CLI()
	cli.start()
```


## Advanced Example.

Advanced cli.CLI code example.

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, sys, syst3m ; sys.path.insert(1, syst3m.defaults.source_path(__file__, back=2))
from ssht00ls.classes.config import *
import ssht00ls

# the cli object class.
class CLI(cl1.CLI):
	def __init__(self):
		
		# defaults.
		cl1.CLI.__init__(self,
			modes={
				"Aliases:":"*chapter*",
				"    --create-alias":"Create a ssh alias.",
				"        --server myserver":"Specify the server's name.",
				"        --username myuser":"Specify the username.",
				"        --ip 0.0.0.0":"Specify the server's ip.",
				"        --port 22":"Specify the server's port.",
				"        for ssh keys:":"",
				"        --key /path/to/key/private_key":"Specify the path to the private key.",
				"        --passphrase 'MyPassphrase123'":"Specify the keys pasphrase (optional).",
				"        for smart cards:":"",
				"        --smart-cards":"Enable the smart cards boolean.",
				"        --pin 123456":"Specify the smart cards pin code (optional).",
				"Keys:":"*chapter*",
				"    --generate":"Generate a ssh key.",
				"        --path /keys/mykey/":"Specify the keys directory path.",
				"        --passphrase Passphrase123":"Specify the keys passphrase.",
				"        --comment 'My Key'":"Specify the keys comment.",
				"Sessions:":"*chapter*",
				"    --command <alias> 'ls .'":"Execute a command over ssh.",
				"    --session <alias>":"Start a ssh session.",
				"        --options '' ":"Specify additional ssh options (optional).",
				"Push & pull:":"*chapter*",
				"    --pull <path> <alias>:<remote>":"Pull a file / directory.",
				"        --delete":"Also update the deleted files (optional).",
				"        --safe":"Enable version control.",
				"        --forced":"Enable forced mode.",
				"    --push <alias>:<remote> <path>":"Push a file / directory.",
				"        --delete":"Also update the deleted files (optional).",
				"        --safe":"Enable version control.",
				"        --forced":"Enable forced mode.",
				"Mounts:":"*chapter*",
				"    --mount <alias>:<remote> <path>":"Mount a remote directory.",
				"    --unmount <path>":"Unmount a mounted remote directory.",
				"        --sudo":"Root permission required.",
				"        --forced":"Enable forced mode.",
				"    --index <path> / <alias>:<remote>":"Index the specified path / alias:remote.",
				"Agent:":"*chapter*",
				"    --start-agent":"Start the ssht00ls agent manually.",
				"    --stop-agent":"Stop the ssht00ls agent.",
				"Daemons:":"*chapter*",
				"    --start-daemon <alias>:<remote> <path>":"Start a ssync daemon manually.",
				"    --stop-daemon <path>":"Stop a ssync daemon.",
				"Basic:":"*chapter*",
				"    --kill <identifier>":"Kill all ssh processes that include the identifier.",
				"    --config":"Edit the ssht00ls configuration file (nano).",
				"    -h / --help":"Show the documentation.",
			},
			options={
				"-j / --json":"Print the response in json format.",
			},
			notes={
				"SSHT00LS_CONFIG":"Specify the $SSHT00LS_CONFIG environment variable to use a different ssht00ls config file.",
			},
			alias=ALIAS,
			executable=__file__,
		)

		#
	def start(self):
		
		# check arguments.
		self.arguments.check(exceptions=["--log-level", "--create-alias"], json=JSON)

		# help.
		if self.arguments.present(['-h', '--help']):
			self.docs(success=True, json=JSON)

		# check create ssh config.
		elif self.arguments.present('--create-alias'):
			
			# create an ssh alias for the key.
			if not self.arguments.present('--smart-card'):
				key = self.arguments.get('--key')
				response = ssht00ls.aliases.create( 
					# the alias.
					alias=self.arguments.get('--alias', chapter="aliases", mode="--create-alias"), 
					# the username.
					username=self.arguments.get('--username'), chapter="aliases", mode="--create-alias", 
					# the public ip of the server.
					public_ip=self.arguments.get('--public-ip', chapter="aliases", mode="--create-alias"),
					# the public port of the server.
					public_port=self.arguments.get('--public-port', chapter="aliases", mode="--create-alias"),
					# the private ip of the server.
					private_ip=self.arguments.get('--private-ip', chapter="aliases", mode="--create-alias"),
					# the private port of the server.
					private_port=self.arguments.get('--private-port', chapter="aliases", mode="--create-alias"),
					# the path to the private key.
					key=key,
					passphrase=getpass.getpass("Enter the passphrase of key [{key}]:"),
					# smart card.
					smartcard=False,)

			# create an ssh alias for a smart card.
			else:
				response = ssht00ls.aliases.create( 
					# the alias.
					alias=self.arguments.get('--alias', chapter="aliases", mode="--create-alias"), 
					# the username.
					username=self.arguments.get('--username', chapter="aliases", mode="--create-alias"), 
					# the public ip of the server.
					public_ip=self.arguments.get('--public-ip', chapter="aliases", mode="--create-alias"),
					# the public port of the server.
					public_port=self.arguments.get('--public-port', chapter="aliases", mode="--create-alias"),
					# the private ip of the server.
					private_ip=self.arguments.get('--private-ip', chapter="aliases", mode="--create-alias"),
					# the private port of the server.
					private_port=self.arguments.get('--private-port', chapter="aliases", mode="--create-alias"),
					# the path to the private key.
					key=smartcard.path,
					# smart card.
					smartcard=True,
					pin=self.arguments.get('--pin', required=False, default=None, chapter="aliases", mode="--create-alias"), )

			# log to console.
			self.stop(response=response, json=JSON)

		# check create ssh config.
		elif self.arguments.present('--generate'):
			
			# generate a key.
			passphrase = self.get_passphrase(required=False)
			if passphrase in ["", None, "null", "None", "none"]: passphrase = None
			response = ssht00ls.keys.generate(
				path=self.arguments.get("--path", chapter="keys", mode="--generate"), 
				passphrase=passphrase, 
				comment=self.arguments.get("--comment", chapter="keys", mode="--generate"),)
			self.stop(response=response, json=JSON)

		# kill ssh processes.
		elif self.arguments.present('--kill'):
			response = ssht00ls.utils.kill_ssh(
				identifier=self.arguments.get("--kill"), 
				sudo=self.arguments.present("--sudo"),)
			self.stop(response=response, json=JSON)

		# pull.
		elif self.arguments.present('--pull'):
			remote = self.arguments.get("--pull", index=1, chapter="push & pull", mode="--pull")
			path = self.arguments.get("--pull", index=2, chapter="push & pull", mode="--pull")
			if ":" not in remote:
				self.docs(
					error=f"Invalid <alias>:<remote> <path> format.", 
					chapter="push & pull", 
					mode="--pull", 
					notes={
						"<alias>:<path>":"Pack the alias & tuple together as one argument in the following format [<alias>:<path>]."
					},
					json=JSON,)
			alias,remote = remote.split(":")
			exclude = None
			if self.arguments.present("--exclude"): 
				exclude = self.arguments.get("--exclude", chapter="push & pull", mode="--pull").split(",")
			elif self.arguments.present("--no-exclude"): exclude = []
			response = ssht00ls.ssync.pull(
				alias=alias, 
				remote=remote, 
				path=path,
				exclude=exclude, 
				forced=self.arguments.present("--forced"), 
				delete=self.arguments.present("--delete"), 
				safe=self.arguments.present("--safe"), )
			self.stop(response=response, json=JSON)

		# push.
		elif self.arguments.present('--push'):
			path = self.arguments.get("--push", index=1, chapter="push & pull", mode="--push")
			remote = self.arguments.get("--push", index=2, chapter="push & pull", mode="--push")
			if ":" not in remote:
				self.docs(
					error=f"Invalid <alias>:<remote> <path>.", 
					chapter="push & pull", 
					mode="--push", 
					notes={
						"<alias>:<path>":"Pack the alias & tuple together as one argument in the following format [<alias>:<path>]."
					},
					json=JSON,)
			alias,remote = remote.split(":")
			exclude = None
			if self.arguments.present("--exclude"): 
				exclude = self.arguments.get("--exclude", chapter="push & pull", mode="--push").split(",")
			elif self.arguments.present("--no-exclude"): exclude = []
			response = ssht00ls.ssync.push(
				alias=alias, 
				remote=remote, 
				path=path,
				exclude=exclude, 
				forced=self.arguments.present("--forced"), 
				delete=self.arguments.present("--delete"), 
				safe=self.arguments.present("--safe"), )
			self.stop(response=response, json=JSON)

		# mount.
		elif self.arguments.present('--mount'):
			remote = self.arguments.get("--mount", index=1, chapter="mounts", mode="--mount", notes={})
			path = self.arguments.get("--mount", index=2, chapter="mounts", mode="--mount", notes={})
			if ":" not in remote:
				self.docs(
					error=f"Invalid <alias>:<remote> <path>.", 
					chapter="mounts", 
					mode="--mount", 
					notes={
						"<alias>:<path>":"Pack the alias & tuple together as one argument in the following format [<alias>:<path>]."
					},
					json=JSON,)
			alias,remote = remote.split(":")
			response = ssht00ls.ssync.mount(
				alias=alias, 
				remote=remote, 
				path=path,
				forced=self.arguments.present("--forced"), )
			self.stop(response=response, json=JSON)

		# unmount.
		elif self.arguments.present('--unmount'):
			path = self.arguments.get("--unmount", index=1, chapter="mounts", mode="--unmount")
			response = ssht00ls.ssync.unmount(
				path=path,
				forced=self.arguments.present("--forced"), 
				sudo=self.arguments.present("--sudo"), )
			self.stop(response=response, json=JSON)

		# index.
		elif self.arguments.present('--index'):
			index = self.arguments.get("--index", chapter="mounts", mode="--index")
			if ":" in index:
				alias,remote = index.split(":")
				response = ssht00ls.ssync.index(path=remote, alias=alias)
			else:
				response = ssht00ls.ssync.index(path=index)
			self.stop(response=response, json=JSON)

		# start daemon.
		elif self.arguments.present('--start-daemon'):
			remote = self.arguments.get("--start-daemon", index=1, chapter="daemons", mode="--start-daemon")
			path = self.arguments.get("--start-daemon", index=2, chapter="daemons", mode="--start-daemon")
			if ":" not in remote:
				self.docs(
					error=f"Invalid <alias>:<remote> <path>.", 
					chapter="damons", 
					mode="--start-daemon", 
					notes={
						"<alias>:<path>":"Pack the alias & tuple together as one argument in the following format [<alias>:<path>]."
					},
					json=JSON,)
			alias,remote = remote.split(":")
			response = ssht00ls.ssync.daemon(alias=alias, remote=remote, path=path)
			self.stop(response=response, json=JSON)

		# stop daemon.
		elif self.arguments.present('--stop-daemon'):
			path = self.arguments.get("--stop-daemon", index=1, chapter="daemon", mode="--stop-daemon")
			response = ssht00ls.ssync.stop_daemon(path)
			self.stop(response=response, json=JSON)

		# config.
		elif self.arguments.present('--config'):
			if JSON:
				print(CONFIG.dictionary)
			else:
				os.system(f"nano {CONFIG.file_path.path}")

		# invalid.
		else: self.invalid()

		#
	def get_passphrase(self, required=True):
		return self.arguments.get("--passphrase", required=required).replace("\\", "").replace("\ ", "")
# main.
if __name__ == "__main__":
	cli = CLI()
	cli.start()

```


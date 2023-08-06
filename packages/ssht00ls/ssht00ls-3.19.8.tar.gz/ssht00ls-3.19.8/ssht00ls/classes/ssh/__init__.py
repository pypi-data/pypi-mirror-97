#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from ssht00ls.classes.config import *
from ssht00ls.classes.ssh.tunnel import Tunnel
import ssht00ls.classes.ssh.utils as ssh_utils 

# the ssh object class.
class SSH(syst3m.objects.Traceback):
	def __init__(self,
		# initialize as specific not global (optional).
		# 	the alias.
		alias=None,
	):

		# defaults.
		syst3m.objects.Traceback.__init__(self, traceback="ssht00ls.ssh", raw_traceback="ssht00ls.classes.ssh.SSH")	

		# modules.
		self.utils = ssh_utils

		# objects.
		self.tunnel = Tunnel(
			alias=alias,)

		# specific args.
		self.specific = alias != None
		self.alias = alias

		#
	def session(self, 
		alias=None,
	):

		# check specific.
		if self.specific:
			if alias == None: alias = self.alias

		# checks.
		response = r3sponse.parameters.check(
			traceback=self.__traceback__(function="session"),
			parameters={
				"alias":alias,
			})
		if not response.success: return response

		# session.
		os.system(f"ssh {DEFAULT_SSH_OPTIONS} {alias}")

		# handler.
		return r3sponse.success(f"Successfully started ssh session [{alias}].")

		#
	def command(self,
		# the alias.
		alias=None,
		# the command to execute.
		command=None,
		# serialize the output to json.
		serialize=False,
		# the log level.
		log_level=0,
		# accept new host keys.
		accept_new_host_keys=True,
	):
		
		# check specific.
		if self.specific:
			if alias == None: alias = self.alias

		# checks.
		response = r3sponse.parameters.check(
			traceback=self.__traceback__(function="command"),
			parameters={
				"alias":alias,
				"command":command,
			})
		if not response.success: return response

		# command.
		response = self.utils.execute(
			command=f"""ssh {DEFAULT_SSH_OPTIONS} {alias} ' {command} ' """,
			log_level=log_level,
			serialize=serialize,
			accept_new_host_keys=accept_new_host_keys,)

		# handler.
		if log_level >= 0:
			if response.success: print(response.output)
			else: print(response.error)
		return response
	
		
# initialized objects.
ssh = SSH()
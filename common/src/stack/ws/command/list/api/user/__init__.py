#
# @copyright@
# @copyright@
#

import os
import sys
import stack.django_env

import stack.commands

from django.contrib.auth.models import User

class Command(stack.commands.Command):
	"""
	List all users registered to use the API
	and the groups they belong to.
	<dummy />
	"""
	def run(self, params, args):
		# Get all the Users
		u = User.objects.all()

		self.beginOutput()
		for user in u:
			# Get all the group each user is in
			grouplist = []
			for g in user.groups.all():
				grouplist.append(g.name)
			groupstring = " ".join(grouplist)
			self.addOutput(user.username, [user.is_superuser, groupstring])
		self.endOutput(header=["USER", "ADMIN", "GROUPS"], trimOwner=False)
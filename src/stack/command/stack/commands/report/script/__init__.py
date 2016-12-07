# @Copyright@
#  				Rocks(r)
#  		         www.rocksclusters.org
#  		         version 5.4 (Maverick)
#  
# Copyright (c) 2000 - 2010 The Regents of the University of California.
# All rights reserved.	
#  
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#  
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#  
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
#  
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
#  
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
#  
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# @Copyright@
#
# @SI_Copyright@
# @SI_Copyright@


import sys
import subprocess
import stack.commands
import stack.gen

class Command(stack.commands.report.command):
	"""
	Take STDIN XML input and create a shell script that can be executed
	on a host.

	<param optional='1' type='string' name='os'>
	The OS type.
	</param>

	<param optional='1' type='string' name='arch'>
	The architecture type.
	</param>

	<param optional='1' type='string' name='attrs'>
	Attributes to be used while building the output shell script.
	</param>

	<example cmd='report host interface compute-0-0 | stack report script'>
	Take the network interface XML output from 'stack report host interface'
	and create a shell script.
	</example>
	"""

	def run(self, params, args):
		osname, attrs = self.fillParams([
                        ('os', self.os),
			('attrs', {}) ])

		xml = '<?xml version="1.0" standalone="no"?>\n'

		if attrs:
			attrs = eval(attrs)
			xml += '<!DOCTYPE stacki-profile [\n'
			for (k, v) in attrs.items():
				xml += '\t<!ENTITY %s "%s">\n' % (k, v)
			xml += ']>\n'

		xml += '<profile os="%s" attrs="%s">\n' % (osname, attrs)
		xml += '<post>\n'

		for line in sys.stdin.readlines():
			xml += line

		xml += '</post>\n'
		xml += '</profile>\n' 

                p = subprocess.Popen('/opt/stack/bin/stack list host profile profile=shell chapter=bash',
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, shell=True)
                p.stdin.write(xml)
                (o, e) = p.communicate()
                if p.returncode == 0:
                        sys.stdout.write(o)
                else:
                        sys.stderr.write(e)




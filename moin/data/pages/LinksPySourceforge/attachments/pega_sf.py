#!/usr/bin/env python

import os
import re
from urllib import urlopen


sf_description_re = re.compile(r'<TD WIDTH="99%" VALIGN="top">\n<p>(.*?)<p>',re.M | re.S)

sf_links_txt = open('sf_py.txt')

sf_links = sf_links_txt.readlines()

sf_links_txt.close()

links_made = ''
if os.path.exists('sf_py_out.txt'):
	print 'Excluindo os já feitos'
	links_made = open('sf_py_out.txt').read()
links_ok = []
for link in links_made.split('\n'):
	if link.startswith('   * ['):
		project_link = link[6:link.find(']')]
		print 'Ignorando:%s' % project_link
		links_ok.append( project_link )
	else:
		print 'err:%s' % link


out_file = open('sf_py_out.txt','a')

for link in sf_links:
	link = link[6:-2]
	if link not in links_ok:
		#Pega apenas o link

		print "Reading page: %s" % link
		sf_page = urlopen(link).read()
		print "Pegando descrição..."
		match = sf_description_re.search(sf_page)
		if match is not None:
			desc = match.groups()[0]
			line = '   * [%s] - %s\n' % (link,desc)
			out_file.write(line)
			print line
		else:
			project_name = link.split('/')[-1]
			debug_filename = 'sf_%s.debug' % project_name
			debug_file = open(debug_filename,'w')
			debug_file.write(sf_page)
			debug_file.close()
			print "Não consegui pegar a descrição de %s, escrito log em %s" % (project_name,debug_filename)



print 'done.'
	



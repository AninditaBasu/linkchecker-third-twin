#
#
# third_twin.py
# Copyright (C) 2015  Anindita Basu
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/gpl-3.0.txt.
#
#
#
# In a workspace, if a DITA file is linked to another file multiple times, this program will find those instances and report them.
# This program will look at ditamap files for links through parent:child nesting, relationship tables, and family collections.
# This program will also look at dita files for related links and inline links.
#
#
import os
import re
import xml.etree.ElementTree as ET
import collections
#
# Open a file called "RepeatedLinks.html" to write the findings to.
#
reportfile = open("RepeatedLinks.html", "w")
reportfile.write("<html>")
reportfile.write("<head>")
reportfile.write("<title>Report of links repeated at multiple locations</title>")
reportfile.write("<style>h1{color:#A52A2A;}")
reportfile.write("h2{color:#A52A2A;}")
reportfile.write("h3{color:#A52A2A;}")
reportfile.write("h4{color:#A52A2A;}")
reportfile.write('p{font-family:"Trebuchet MS", Arial, Verdana, serif; font-size:16px;line-height:120%;}')
reportfile.write('li{font-family:"Trebuchet MS", Arial, Verdana, serif; font-size:16px;line-height:200%;}')
reportfile.write('td{font-family:"Trebuchet MS", Arial, Verdana, serif; font-size:16px;line-height:200%;}</style>')
reportfile.write("</head>")
reportfile.write("<body>")
#
# Prompt for the workspace directory.
#
print ("\n")
print ("Specify the full path to the directory that contains the plug-ins to be checked.\n")
print ("For example: C:\jazz_repo\RIT_87\n")
workspace=raw_input("Enter the directory: ")
#
# Traverse the supplied directory and count the number of plug-ins (sub directories).
#
reportfile.write("<h1>Report of same link occuring several times on one page</h1>")
print ("\n")
print ("The following folders were checked: \n")
counter = 0
try:
	for foldername in os.listdir(workspace):
		counter = counter + 1
		print (foldername)
except:
	print ("No. Wait. One second. Something is not right.")
	print ("The directory could not be found.")
	print ("The program will now close.")
	reportfile.write("<h4>No. Wait. One second. Something is not right.</h4>")
	reportfile.write("<p>The directory could not be found. The program was aborted.</p>")
	reportfile.write("</body>")
	reportfile.write("</html>")
	reportfile.close()
	raw_input ("Press any key to exit.")
	exit()
reportfile.write('<p>The <a href="file:///')
reportfile.write(workspace)
reportfile.write('" target = "_blank">')
reportfile.write(workspace)
reportfile.write("</a> directory has ")
counter = str(counter)
reportfile.write(counter)
reportfile.write(" folders,") # The "p" tag is closed a bit later, after " .ditamap files.."
#
# plug-ins counted, now count the files in each plug-in.
#
counter = 0
for (dirname, dirs, files) in os.walk(workspace):
	for filename in files:
		if filename.endswith('.dita') :
			counter = counter + 1
			print (filename)
x = str(counter)
reportfile.write(" "+x+" .dita files, and ")
#
# DITA files counted. Now count the ditamap files.
# While counting ditamap files, also write their names to a list called "maplist".
#
maplist = list()
for (dirname, dirs, files) in os.walk(workspace):
	for filename in files:
		if filename.endswith('.ditamap') :
			thefile=os.path.join(dirname,filename)
			maplist.append(thefile)
#
# The list called "maplist" contains names of ditamaps in the supplied directory.
# For some reason, the path in maplist contains \\. Not going to debug as of now. Also contains duplicate entries.
# Clean up the duplicate entries in the "maplist" list.
#
cleanmaplist=list() # List that will not contain the duplicate entries
print ("--\nThe directory contains the following .ditamap files:\n")
for filename in maplist:
	if filename not in cleanmaplist:
		cleanmaplist.append(filename)
		print (filename)
print ("------------\n")
x = len(cleanmaplist)
x = str(x)
reportfile.write(x)
reportfile.write(" .ditamap files. ")
reportfile.write('Links that were found to occur more than once in any topic are listed in the following sections:</p>')
reportfile.write('<ul><li><a href = "#rel">Links that are automatically inserted as child links in a parent topic and as "Related links" in a topic</a></li>')
reportfile.write('<li><a href = "#inline">Inline links in the body content of a topic</a></li>')
reportfile.write('<li><a href = "#family">The "family" attribute in topic references in a ditamap file</a></li></ul>')
reportfile.write('<hr/>')
#
# Now begins the real search for links.
#
# The search is in three parts: 
# Part 1 is for auto-generated links.
# Part 2 is for inline links in body content of topic.
# Part 3 is for family collections in ditamap files.
#
# ========================================================================================
# Begin Part 1
#
# Three kinds of links are auto-generated (the "family" link is dealt with later, as Part 3): 
# Through <reltable> in ditamap file, through parent-child <topicref> in <map> outside <reltable> in ditamap file, and through <related-links> in dita files.
#
# First, search for related links in the <related-links> tag in dita files.
#
linkfile = open("linkfile.txt", "w")
for (dirname, dirs, files) in os.walk(workspace):
	for filename in files:
		if filename.endswith('.dita'):
			thefile=os.path.join(dirname,filename)
			handle = open (thefile)
			for line in handle:
				line = line.rstrip()
				if re.search('link.+\.dita', line):
					fname=re.findall('\S+\.dita', line)
					link=fname[0]
					link=link.lstrip('"')
					linkpos = link.rfind("/") # to find instance of full path refs like ../topics/filename and return only the filename
					linkclean = link[linkpos+1:]
					link = linkclean
					linkpos = link.rfind('"') # to find and remove instances of "href = " from refs
					linkclean = link[linkpos+1:]
					string = filename+":"+linkclean+" in "+thefile
					print (string)
					linkfile.write(string)
					linkfile.write("\n")
handle.close()
linkfile.close()
#
# At this point, the file called linkfile.txt contains all related links found inside topics. 
#Sort this file alphabetically. First, create a list, then sort the list, then overwrite linkfile.txt with this list.
#
with open('linkfile.txt', 'r') as f:
    links = [line.strip() for line in f]
f.close()
#
# At this point, a list called "links" with links is generated.
# Now, sort the list alphabetically. Then, rewrite linkfile.text with this sorted list.
#
links.sort()
linkfile = open ("linkfile.txt", "w")
for entry in links:
	linkfile.write(entry)
	linkfile.write("\n")
linkfile.close()
#
# Taking stock: a list called "links" contains all related links in files, sorted alphabetically acc. to the filename that contains the link.
# Taking stock: a txt file called "linkfile.txt" contains the entries from the "links" list
#
# First part is over.
# Second, find links in reltables in ditamaps.
#
# Remember? The list called "cleanmaplist" contains a list of all the ditamaps?
# Open each ditamap file in the "cleanmaplist" list. 
# Go to the relrow node by drilling down: reltable, relrow. For each relrow, go to relcell and extract all topicref elements.
# In a topicref element, get the value of the href attribute.
# Write this href value to a list called "linklist".
# Within linklist, create 1:1 pair for each item in the list.
# Write these 1:1 pairs to a temporary text file called "temp.txt".
# Restart the "linklist" list at each row
#
temp = open ("temp.txt", "w")
for filename in cleanmaplist:
	map = ET.parse(filename)
	element = map.getroot()
	for table in element.findall('reltable'):
		for row in table.findall('relrow'):
			f = filename.split()
			linklist = list(f,)
			for cell in row.findall('relcell'):
				for topicref in cell.findall('topicref'):
					x = topicref.get('href')
					linklist.append(x)
			length = len(linklist)
			iteration = length - 1
			count = 1
			indx = 1
			while count < iteration:
				y = linklist[count]+ ":"+linklist[indx]+" in "+linklist[0]
				temp.write(y)
				temp.write("\n")
				indx = indx + 1
				if indx > iteration:
						count = count + 1
						indx = 1
temp.close()
#
# At this point, the temporary file called "temp.txt" contains 1:1 file linkages and the ditamap that contains the link.
# Because each element in a relrow is tagged to every element in that row, a topicref is tagged to itself as well. Such entries (A:A) need to be removed now.
# First, create a list with the links.
#
with open('temp.txt', 'r') as f:
    reltlinks = [line.strip() for line in f]
f.close()
#
# At this point, a list called "reltlinks" with links is generated.
#
howmany=len(reltlinks)
linksnoself=list() # This is the list that will not contain topicrefs that are tagged to self.
counter = 0
temp = open ("temp.txt", "w")
while counter < howmany:
	a=reltlinks[counter]
	b=a.find(":")
	c=a.find(" in")
	f1=a[0:b]
	f2=a[b+1:c]
	if f1 != f2:
		linksnoself.append(a)
		temp.write(a)
		temp.write("\n")
	counter = counter + 1
temp.close()
#
# At this point, the list called "linksnoself" contains all reltable links.
# The file called "temp.txt" is overwritten and now contains this new info.
#
# Now, sort the list alphabetically. Then, rewrite "temp.txt" with this sorted list.
#
linksnoself.sort()
temp = open ("temp.txt", "w")
for entry in linksnoself:
	temp.write(entry)
	temp.write("\n")
temp.close()
#
# Now, rewrite "temp.txt" so that only the topic name remains. No "../../plug-in/filename" or "topics/filename"
#
temp2 = open("temp2.txt","w")
handle = open ("temp.txt", "r")
for line in handle:
	line = line.rstrip()
	apos = line.find(":")
	a = line[:apos]
	bpos = line.find(" in ")
	b = line[apos+1:bpos]
	newapos = a.rfind("/")
	newa = a[newapos+1:]
	newbpos = b.rfind("/")
	newb = b[newbpos+1:]
	c = line[bpos:]
	string = newa+":"+newb+c
	temp2.write(string)
	temp2.write("\n")
handle.close()
temp2.close
#
# Second part is not yet over, but the remaining steps will be done together with the third part.
#
# Third, in ditamaps, find parent:child nesting. These are transformed as child links in parent topics.
#
# Traverse the nodes in a ditamap file, and create 1:1 pairs between a parent and its child nodes.
#
mapreflist = open ("mapreflist.txt", "w")
for (dirname, dirs, files) in os.walk(workspace):
	for filename in files:
		if filename.endswith('.ditamap') :
			thefile=os.path.join(dirname,filename)
			print (filename, thefile)
			try:				
				tree = ET.parse(thefile)
				for parent in tree.getiterator('topicref'):
					for child in parent:
						elem = child.tag
						if elem == "topicref":
							print (child.tag, child.attrib.get('href'), parent.tag, parent.attrib.get('href'))
							a = child.attrib.get('href')
							apos = a.rfind("/")
							newa = a[apos+1:]
							b = parent.attrib.get('href')
							bpos = b.rfind("/")
							newb = b[bpos+1:]
							string = newb+":"+newa+" in "+thefile
							mapreflist.write(string)
							mapreflist.write("\n")
			except:
				raw_input("something went wrong")
				exit()
mapreflist.close()
#
# At this point, there are four files with lists of links:
# One, "linkfile.txt", which contains all related-links/link from topic files. Sorted alphabetically.
# Two, "temp.txt", which contains all links inserted through relationship tables of ditamap files. Might contain abs. paths to refs.
# Three, "temp2.txt", which contains all reltable links, but without abs. paths.
# Four, "mapreflist.txt", which contains all parent:child links in the <map> element of ditamap files.
#
# The contents of "linkfile.txt", "temp2.txt", and "mapreflist.txt" are in the exact same format, which is "fileA:fileB in absolutePathToFileA".
# The next step would be to merge the contents of these three files, and sort the resultant list alphabtically.
#
# Merge "linkfile.txt", "temp2.txt", and "mapreflist.txt", and write the entries to "temp.txt".
#
temp = open("temp.txt", "w")
linkfile = open("linkfile.txt", "r")
for line in linkfile:
	line = line.rstrip()
	temp.write(line)
	temp.write("\n")
linkfile.close()
temp2 = open("temp2.txt", "r")
for line in temp2:
	line = line.rstrip()
	temp.write(line)
	temp.write("\n")
mapreflist = open("mapreflist.txt", "r")
for line in mapreflist:
	line = line.rstrip()
	temp.write(line)
	temp.write("\n")
temp.close()
linkfile.close()
temp2.close()
mapreflist.close()
#
# Now, "temp.txt" contains a list of all links in the workspace, inserted through either reltables in ditamaps or related links on dits files.
# Sort this file alphabetically.
#
with open('temp.txt', 'r') as f:
    listoflinks = [line.strip() for line in f]
f.close()
listoflinks.sort()
temp = open ("temp.txt", "w")
for entry in listoflinks:
	temp.write(entry)
	temp.write("\n")
temp.close()
#
# Next, read each line in temp.txt. If the next line also begins with the same substring (the file is alphabetically sorted), the linkages are duplicates.
#
handle = open ("temp.txt")
duplicatelinks = list() # A list to write duplicate links to.
prevline = ""
for line in handle:
	pos = line.find(" in")
	x = line[:pos]
	if prevline[:pos] == line[:pos]:
		duplicatelinks.append(prevline)
		duplicatelinks.append(line)
	prevline = line
handle.close()
#
# The list called "duplicatelinks" contains duplicate links in ditamaps in the supplied workspace.
# However, because every line became a previous line in the next iteration, this list can have duplicate entries if there is more than one pair of duplicates.
# So, now, remove these new duplicates.
#
counter = 1
howmany = len(duplicatelinks)
templist = list()
while counter < howmany:
	if duplicatelinks[counter] == duplicatelinks[counter-1]:
		try:
			if duplicatelinks[counter] == duplicatelinks[counter+1]:
				templist.append(duplicatelinks[counter])
		except:
			break
	counter = counter + 1
howmany = len(templist)
counter = 0
while counter < howmany:
	for item in duplicatelinks:
		if item == templist[counter]:
			duplicatelinks.remove(item)
			break
	counter = counter + 1
#
# Write these entries to the report file.
#
print ("These are the duplicate links through relationship tables in .ditamap files.\n")
print (duplicatelinks)
#
reportfile.write('<a name = "rel"></a>')
reportfile.write('<h2>Links that are automatically inserted as child links in a parent topic and as "Related links" in a topic</h2>')
reportfile.write('<p>These are the instances where links are inserted through the relationship table of a ditamap, the related-links tag of a dita file, or through a parent-child relationship in the ToC section of a ditamap file.</p>')
reportfile.write('<p>Whenever File A is thus linked to File B more than once, each instance is reported in the table. You might choose to retain one of these links and delete the others.</p>')
reportfile.write('<table border = "1">')
reportfile.write("<tr><td><h4>Where found</h4></td><td><h4>File A<h4></td><td><h4>File B</h4></td></tr>")
temp = open ("temp.txt", "r")
if len(duplicatelinks) == 0:
	reportfile.write("<tr><td><p>No duplicate links are created through relationship tables.</p></td><td>&nbsp;</td><td>&nbsp;</td></tr>")
else:	
	for entry in duplicatelinks:
		reportfile.write("<tr>")
		where = entry.find(" in ")
		file1 = entry.find(":")
		fileA = entry[0:file1] # gives the entire xref of file A
		fileB = entry[file1+1:where]
		containerfile = entry[where+4:] # okay to use full path in file name because the writer needs to be locate and open this file for editing
		reportfile.write("<td>")
		reportfile.write(containerfile)
		reportfile.write("</td><td>")
		reportfile.write(fileA)
		reportfile.write("</td><td>")
		reportfile.write(fileB)
		reportfile.write("</td></tr>")
temp.close()
#
reportfile.write("</table>")
#
# Reporting of duplicate links through <reltable> in ditamap file, <topicref> in <map> outside <reltable> in ditamap file, and <related-links> in dita files tags is now complete.
#
# Part 1 is over
#
# ========================================================================================
#
# Begin Part 2
#
# Check if a topic itself has cross-references to another topic more than once within the content body (inline links).
#
reportfile.write('<a name = "inline"></a>')
reportfile.write('<h2>Inline links that are present in the manually written body content of a topic</h2>')
reportfile.write('<p>These are the instances where the same cross-reference is repeated multiple times within the body of a topic file. In-topic jumps are also reckoned as a cross-reference. </p>')
#
# Create a list, called "hreflist", to store all files that contain an href.
#
hreflist = list()
#
# Traverse the supplied directory.
# For all files that end with .dita AND contain an href element to another .dita file, add filename to the "hreflist" list.
# In the following tuple, dirname is the full path to the plug-in, dirs is the list of subdirectories in the dirname directory, and files is the list of files in the subdirectories.
# The tuple doesn't seem to work if these 3 variables are not used, or if 2 or 4 variables are used.
#
counter = 0 #to count the total number of .dita files checked, irrespective of whether the file has an href
for (dirname, dirs, files) in os.walk(workspace):
	for filename in files:
		if filename.endswith('.dita') :
			counter = counter + 1
			print (filename)
			thefile=os.path.join(dirname,filename)
			handle = open (thefile)
			for line in handle:
				line = line.rstrip()
				if re.search('href.+\.dita', line) : 
					hreflist.append(thefile)
handle.close()
x = str(counter)
#
# Now, the list called "hreflist" contains the names and absolute paths of files that contain an href to another topic file.
# Next, parse "hreflist" to remove duplicate entries. Store these entries in a list called "cleanhreflist".
#
cleanhreflist=list()
for filename in hreflist:
	if filename not in cleanhreflist:
		cleanhreflist.append(filename)
#
# Now, this list called "cleanhreflist" contains the names and absolute paths of files that contain an href to another topic.
# Next, open each file in this list and see if an href occurs more than once.
# If it does, print it.
#
print ("\n")
print ("These are the duplicate in-line links:\n")
#
x = len(cleanhreflist)
if x == 0:
	print ("There are no duplicate in-line links in topic files.")
	reportfile.write("<p>There are no duplicate in-line links in topic files.</p>")
else:	
	reportfile.write('<table border = "1">')
	reportfile.write('<tr><td><h4>Where found</h4></td><td><h4>Cross-reference to</h4></td><td><h4>No. of occurences</h4></td></tr>')
	prevfilename = ""
	counter = 0
	reflist = list()
	for filename in cleanhreflist:
		#counthref = list() # counter for occurence of filename
		handle = open(filename)
		for line in handle:
			line = line.rstrip()
			if re.search('\.dita', line): 
				fname=re.findall('\S+\.dita', line)
				link=fname[0]
				link=link.lstrip('"')
				if re.search('prodnames', link):continue # because prodnames.dita can be conref-ed for the product names several times within a file
				string = filename+"+"+link
				reflist.append(string)
	c = collections.Counter()
	c.update(reflist)
	for key, value in c.iteritems():
		if value ==1:continue
		else:
			print (key, value)
			a = str(key)
			b = str(value)
			fileAfind = a.find("+")
			fileA = a[:fileAfind]
			fileB = a[fileAfind+1:]
			linkpos = fileB.rfind("/") # to find instance of full path refs like ../topics/filename and return only the filename
			linkclean = fileB[linkpos+1:]
			fileB = linkclean
			linkpos = fileB.rfind('"') # to find and remove the string "href = " from refs and retain only the filename
			linkclean = fileB[linkpos+1:]
			reportfile.write("<tr><td>"+fileA+"</td><td>"+linkclean+"</td><td>"+b+"</td></tr>")
	reportfile.write("</table>")
handle.close()
#
# Checking and reporting of in-file links is complete.
#
# Part 2 is over
#
# ========================================================================================
#
# Begin Part 3
#
# Find and report the number of times a family collection exists in a ditamap.
#
# First, find the number of occurences, and write the filename and number as a key:value pair in a dictionary
#
familylist = dict()
for filename in cleanmaplist:
	counter = 0
	handle = open(filename)
	for line in handle:
		line = line.rstrip()
		if line.find('family') == -1: # line.find returns -1 if string is not found
			continue
		counter = counter + 1
	familylist.update({filename: counter})
print (familylist)
handle.close()
#
# Next, open the "familylist" dictionary and ignore the filenames that have a count of 0 (zero). Write the remaining filenames to the report.
#
reportfile.write('<a name = "family"></a>')
reportfile.write('<h2>The "family" attribute in topic references in a ditamap file</h2>')
reportfile.write('<p>Because links are automatically generated for each topicref in a family collection, you might want to review these instances.</p>')
reportfile.write('<p>If the table has no entries, none of the ditamap files in your workspace have a family collection.</p>')
reportfile.write('<table border = "1">')
reportfile.write('<tr><td><h4>Where found</h4></td><td><h4>No. of "family" occurences</h4></td></tr>')
#
for filename, number in familylist.iteritems():
	if number != 0:
		print (filename, number)
		a = str(number)
		reportfile.write('<tr><td>'+filename+'</td><td>'+a+'</td></tr>')
reportfile.write('</table>')
#
# Part 3 is over
#
# ========================================================================================
#
# Write the closing HTML tags in the report file and begin the closing down of this program.
#
reportfile.write("</body>")
reportfile.write("</html>")
reportfile.close()
#
# Delete the four temporary text files that were created during program execution.
#
os.remove("temp.txt")
os.remove("temp2.txt")
os.remove("linkfile.txt")
os.remove("mapreflist.txt")
#
# Display a completion message on the program console.
#
print ("------------\n")
print ("------------\n")
print ("S T A R T   R E A D I N G   F R O M   H E R E")
print ("------------\n")
print ("\nA report file called RepeatedLinks.html was generated and placed in the same directory that has this program.\n")
print("The program will now close.\n")
#
raw_input("Press any key to exit.")
exit()
# The End

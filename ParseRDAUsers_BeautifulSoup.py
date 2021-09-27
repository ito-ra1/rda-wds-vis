# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 21:37:18 2019

@author: Alicia Urquidi Diaz and Seiya Terada
"""

# Import Beatiful Soup
from bs4 import BeautifulSoup
import os
import re

# Open output files for users and groups
out = open('UsersRDA.txt','a+',encoding='utf-8')
#gr = open('GroupsRDA.txt','a+',encoding='utf-8')

# Start counter from 1 to 25000
i = 1
# Create list of files to be parsed
files=[]
count = 0
while i:
    if i == 30000:
        print('All i are in files. Starting to parse.')
        break
    # Open file by appending i to folder path where HTML files are saved
    file = 'C:/Users/seiya/documents/Uni/Co-op/ONC Work/RDACrawl/RDA_Users/'+str(i)
    # Append each file to files[]
    if os.path.isfile(file):
        files.append(file)

    # unless it doesn't exist (remember I created more URLs than actually exist, so wget will return no files for many of them)
    else:
    	print('User '+str(i)+' doesn''t exist/no such file in RDA_Users')
    i = i + 1
    # I like to add feedback so I understand what my code is doing and when
    if i % 100 == 0:
        print('adding file '+str(i)+' to files')

# New counter to go through all files in file[]
c = 1
# for each file in file[], Beautiful Soup finds 1) the URLs (this is for reference) 2) title-username, 3) professional title, 4) field, 5) org type, 6) city, 7) country, 8) and groups.
for x in files:
    out.write('USER_'+str(c)+'|,|')
    f = open(x,'r',encoding='utf-8')
    soup = BeautifulSoup(f, 'lxml')
    try:
        canon = soup.find('link', rel='canonical')
        out.write(canon.get('href')+'|;|')
        #gr.write(canon.get('href')+'|;|')
    except:
        out.write('NULL|;|')
        #gr.write('NULL|;|')
        print('Could not find canonical link')
    try:
        short = soup.find('link', rel='shortlink')
        out.write(short.get('href')+'|;|')
        #gr.write(short.get('href')+'|;|')
    except:
        out.write('NULL|;|')
        #gr.write('NULL|;|')
        print('Could not find shortlink')
    try:
        name = soup.find('h2', class_='title-username')
    except:
        print('Could not find user''s name in file '+str(c))
    try:
        protitle = soup.find('div', class_='field-name-field-profile-professiona-title')
    except:
        print('Could not find professional title in file '+str(c))
    try:
        expert = soup.find('div', class_='field-name-field-profile-primary-domain')
    except:
        print('Could not find primary field of work in file '+str(c))
    try:
        organization = soup.find('div', class_='field-name-field-profile-organization-name')
    except:
        print('Could not find organization in file '+str(c))
    try:
        o_type = soup.find('div', class_='field-name-field-profile-organization-type')
    except:
        print('Could not find org type in file '+str(c))
    try:
        country = soup.find('div', class_='field-name-field-profile-country')
    except:
        print('Could not find country in file '+str(c))
    try:
        groups = soup.find('div',class_='view-mygroups')
    except:
        print('Could not find groups in file '+str(c))
    #then Python writes a line for each user file. If the field is empty, it writes NULL.
    try:
        out.write(name.text+'|name|')
    except:
        out.write('NULL|name|')
        print('Could not write name for '+str(c))
    try:
        out.write(protitle.text+'|;|')
    except:
        out.write('NULL|;|')
        print('Could not write professional title for '+str(c))
    try:
        out.write(expert.text+'|;|')
    except:
        out.write('NULL|;|')
        print('Could not write primary field of work for '+str(c))
    try:
        out.write(organization.text+'|;|')
    except:
        out.write('NULL|;|')
        print('Could not write org name for '+str(c))
    try:
        out.write(o_type.text+'|;|')
    except:
        out.write('NULL|;|')
        print('Could not write org type for '+str(c))
    try:
        out.write(country.text+'|country|')
    except:
        out.write('NULL|country|')
        print('Could not write country name for '+str(c))
    try:
        out.write('My groups:')
        for groups in soup.find_all('div', class_='view-mygroups'):
            for a in groups.find_all('a', href=re.compile('^/groups/')):
                out.write(a.text+'.') #for getting text between the link
        out.write('|.|')
    except:
        out.write('My groups:NULL|.|')
    #try:
        #gr.write('My groups:'+groups.text+'\n')
    #except:
        #gr.write('NULL\n')
        #print('Could not write groups for '+str(c))
    f.close()
    c = c + 1
    if c % 100 == 0:
        print('counter is at '+str(c))
out.close()

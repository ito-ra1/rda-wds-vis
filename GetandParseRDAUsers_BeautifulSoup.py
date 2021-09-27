# -*- coding: utf-8 -*-
"""
Alicia Urquidi Diaz, 2021 CC BY-NC 4.0.

Based on code by Seiya Terada (co-op student at WDS-ITO in Spring 2020) and Alicia Urquidi Diaz.

This script scrapes membership data from the rd-alliance.org website. We developed this to extract & visualize de-identified RDA membership data by different parameters (region, type of institution, disciplines, etc.).
Import packages and create output files

The output will be two text files: Users.txt and Groups.txt.

"""
from bs4 import BeautifulSoup
# Used requests to get HTML from RDA
import requests
# Regex used to match context inside tags.
import re

# Import the packages and create the files in tab-delimited format with headers.
out = open('Users.txt','a+',encoding='utf-8')
out.write('user_ID\tProfessional title\tPrimary Domain/Field of Expertise (Other)\tOrganization name\tOrganization type\tCountry\n')
gr = open('Groups.txt','a+',encoding='utf-8')
gr.write('user_ID\tGroup\n')

# I use a counter to generate all member page URLs following the `https://www.rd-alliance.org/user/[counter]` schema. As of August 25, 2021, the RDA boasted 12009 registered members. This does not mean that the highest user number is 12009, so this is a bit of trial and error and, as of the same date, the highest user number in the 29550s. 
# I set the counter higher (30000) to be on the safe side.
c = 30000
#ids = 3498034
l = []
while c > 0:
    c = c - 1
    #ids = (c * ids)/(c - 3)
    if c % 1000 == 0:
        print('counter is at '+str(c))
    r = requests.get("https://www.rd-alliance.org/user/"+str(c))
    # For every number, if `requests` returns `200` the script grabs the HTML, parses through it, and writes a tab-separated record into a text file.
    if r.status_code != 200:
        l.append(c)
        continue
    else:
        w = r.text  
        out.write(str(c)+'\t')
        soup = BeautifulSoup(w, 'lxml')
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
        try:
            p = re.sub(r'Professional title:', r'', protitle.text)
            out.write(p+'\t')
        except:
            out.write('NULL\t')
            print('Could not write professional title for '+str(c))
        try:
            e = re.sub(r'Primary Domain\/Field of Expertise \(Other\):', r'', expert.text)
            out.write(e+'\t')
        except:
            out.write('NULL\t')
            print('Could not write primary field of work for '+str(c))
        try:
            ot = re.sub(r'Organization name:', r'', organization.text)
            out.write(ot+'\t')
        except:
            out.write('NULL\t')
            print('Could not write org name for '+str(c))
        try:
            ty = re.sub(r'Organization type:', r'', o_type.text)
            out.write(ty+'\t')
        except:
            out.write('NULL\t')
            print('Could not write org type for '+str(c))
        try:
            co = re.sub(r'Country:', r'', country.text)
            out.write(co+'\n')
        except:
            out.write('NULL\n')
            print('Could not write country name for '+str(c))
        try:
            for groups in soup.find_all('div', class_='view-mygroups'):
                for a in groups.find_all('a', href=re.compile('^/groups/')):
                    gr.write(str(c)+'\t'+a.text+'\n') #for getting text between the link
        except:
            continue
out.close()
gr.close()

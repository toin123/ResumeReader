
# coding: utf-8

# In[3]:


# Imports
import copy
import os
from os import listdir
from os.path import isfile, join
import PyPDF2 
import textract
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import sklearn
from sklearn.ensemble import GradientBoostingClassifier as gbc
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier as rfc
from collections import *
nltk.download('punkt')
nltk.download('stopwords')
import numpy as np
import pickle


# In[5]:


mypath = "grabs"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]


# In[6]:


texts = []
for filename in onlyfiles:
  f = filename
  filename = mypath+"/"+filename
  print(filename)
  #open allows you to read the file
  pdfFileObj = open(filename,'rb')
  #The pdfReader variable is a readable object that will be parsed
  pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False)
  #discerning the number of pages will allow us to parse through all #the pages
  num_pages = pdfReader.numPages
  count = 0
  text = ""
  #The while loop will read each page
  while count < num_pages:
      pageObj = pdfReader.getPage(count)
      count +=1
      text += pageObj.extractText()
      text = text.replace('\r','!')
      text = text.replace('\n','')
      text = text.replace('\t','^')
      text = text.replace('\v','*')
      text = text.lower()
  # split into words by white space
  # split into words by white space

  # remove punctuation from each word
  import re
  words = re.split(r'\W+', text)
  #This if statement exists to check if the above library returned #words. It's done because PyPDF2 cannot read scanned files.
  if text != "":
     text = text
  #If the above returns as False, we run the OCR library textract to #convert scanned/image based PDF files into text
  else:
    try:
      text = textract.process(fileurl, method='tesseract', language='eng')
    except:
      text = ""
  # Now we have a text variable which contains all the text derived #from our PDF file. Type print(text) to see what it contains. It #likely contains a lot of spaces, possibly junk such as '\n' etc.
  # Now, we will clean our text variable, and return it as a list of keywords.
#   print(text)

  # texts.append(text)
  #words = re.split(r'\W+', text)
  texts.append((f, text))


# In[7]:


'''
anonymize:

DESCRIPTION:
takes in tokenized resume and removes identifying information. Approaches task 
by removing all text before a few 'action' words. This process
also conveniently cleans the data of a few garbage tokens.

PARAMS:
keywords - tokenized data from a single resume

RETURN:
a copy of keywords with id info scrubbed

'''
def anonymize(keywords):
  lk = len(keywords)
  keewords = copy.copy(keywords)
  education = ['Education', 'education', 'EDUCATION']
  school = ['School', 'school', 'SCHOOL']
  experience = ['Experience', 'experience', 'EXPERIENCE']
  skills = ['Skills', 'skills', 'SKILLS']
  technical = ['Technical', 'technical', 'TECHNICAL']
  research = ['Research', 'research', 'RESEARCH']
  projects = ['Projects', 'projects', 'PROJECTS']
  objective = ['Objective', 'objective', 'OBJECTIVE']
  activities = ['Activities', 'activities', 'ACTIVITIES']
  interests = ['Interests', 'interests', 'INTERESTS']
  for word in range(lk):
    if (keywords[word] in education or keywords[word] in experience or
        keywords[word] in skills or keywords[word] in technical or
       keywords[word] in research or keywords[word] in projects or
       keywords[word] in objective or keywords[word] in activities or
       keywords[word] in interests):
      break
    else:
      keewords = keewords[1:]
  return keewords


# In[8]:


def make_false(flag_array, target):
  flag_arr = copy.copy(flag_array)
  for flag in flag_arr:
    if flag is not target:
      flag[0] = False
  return flag_arr


# In[9]:


'''
categorize:

DESCRIPTION:
Sorts anonymized data into general resume categories retaining order

PARAMS:
keywords - anonymized list of resume data in order-ish

RETURN:
a dictionary of the categorized resume
'''
def categorize(keywords):
  education = ['Education', 'education', 'EDUCATION', 'School', 'school', 'SCHOOL']
  
  # Flag to determine both if we run into the word and are in the 
  # section (flag[0]), as well as if we have seen it before (flag[1])
  # Given nature of reumes, first time we encounter these words is 
  # overwhelmingly the section header
  edu = [False, False]
  experience = ['Experience', 'experience', 'EXPERIENCE']
  exp = [False, False]
  skills = ['Skills', 'skills', 'SKILLS', 'Technical', 'technical', 'TECHNICAL']
  tech = [False, False]
  research = ['Research', 'research', 'RESEARCH']
  res = [False, False]
  projects = ['Projects', 'projects', 'PROJECTS']
  pro = [False, False]
  objective = ['Objective', 'objective', 'OBJECTIVE']
  obj = [False, False]
  activities = ['Activities', 'activities', 'ACTIVITIES']
  act = [False, False]
  interests = ['Interests', 'interests', 'INTERESTS']
  inter = [False, False]
  flags = [edu, exp, tech, res, pro, obj, act, inter]
  categories_without_skills_and_tech = ['Education', 'education', 'EDUCATION',
                                        'School', 'school', 'SCHOOL'
                                       'Experience', 'experience', 'EXPERIENCE',
                                       'Research', 'research', 'RESEARCH',
                                        'Projects', 'projects', 'PROJECTS',
                                        'Objective', 'objective', 'OBJECTIVE',
                                        'Activities', 'activities', 'ACTIVITIES',
                                        'Interests', 'interests', 'INTERESTS']
  all_cats = ['Education', 'education', 'EDUCATION',
              'School', 'school', 'SCHOOL'
              'Experience', 'experience', 'EXPERIENCE',
              'Skills', 'skills', 'SKILLS',
              'Technical', 'technical', 'TECHNICAL',
              'Research', 'research', 'RESEARCH',
              'Projects', 'projects', 'PROJECTS',
              'Objective', 'objective', 'OBJECTIVE',
              'Activities', 'activities', 'ACTIVITIES',
              'Interests', 'interests', 'INTERESTS']
  
  categories = {'education':[], 'experience':[], 'skills':[], 'research':[],
                'projects':[], 'objective':[], 'activities':[], 'interests':[]}
  words = copy.copy(keywords)
  '''
  this counter + counter_val are to prevent accidentally going into the next
  section
  ** in future be sure to check for 'research intern' or 'research assistant' **
  '''
  counter = 0
  count_val = 3
  for word in words:
    if (word in education and edu[1] == False and counter <= 0):
      edu[0] = True
      edu[1] = True
      counter = count_val
      flags = make_false(flags, edu)
    elif (word in experience and exp[1] == False and counter <= 0):
      exp[0] = True
      exp[1] = True
      counter = count_val
      flags = make_false(flags, exp)
    elif (word in skills and tech[1] == False and counter <= 0):
      tech[0] = True
      tech[1] = True
      counter = count_val
      flags = make_false(flags, tech)
    elif (word in research and res[1] == False and counter <= 0):
      res[0] = True
      res[1] = True
      counter = count_val
      flags = make_false(flags, res)
    elif (word in projects and pro[1] == False and counter <= 0):
      pro[0] = True
      pro[1] = True
      counter = count_val
      flags = make_false(flags, pro)
    elif (word in objective and obj[1] == False and counter <= 0):
      obj[0] = True
      obj[1] = True
      counter = count_val
      flags = make_false(flags, obj)
    elif (word in activities and act[1] == False and counter <= 0):
      act[0] = True
      act[1] = True
      counter = count_val
      flags = make_false(flags, act)
    elif (word in interests and inter[1] == False and counter <= 0):
      inter[0] = True
      inter[1] = True
      counter = count_val
      flags = make_false(flags, inter)
    
    if (edu[0] and word not in education):
      categories['education'].append(word)
      counter -=1
    if (exp[0] and word not in experience):
      categories['experience'].append(word)
      counter -=1
    if (tech[0] and word not in skills):
      categories['skills'].append(word)
      counter -=1
    if (res[0] and word not in research):
      categories['research'].append(word)
      counter -=1
    if (pro[0] and word not in projects):
      categories['projects'].append(word)
      counter -=1
    if (obj[0] and word not in objective):
      categories['objective'].append(word)
      counter -=1
    if (act[0] and word not in activities):
      categories['activities'].append(word)
      counter -=1
    if (inter[0] and word not in interests):
      categories['interests'].append(word)
      counter -=1
  return categories


# In[10]:


tokenized_keywords = []
tokenized_categories = []
success_files = []
c = 0
for t in texts:
  #The word_tokenize() function will break our text phrases into #individual words
  tokens = word_tokenize(t[1])
  #we'll create a new list which contains punctuation we wish to clean
  punctuations = ['(',')',';',':','[',']',',']
  #We initialize the stopwords variable which is a list of words like #"The", "I", "and", etc. that don't hold much value as keywords
  stop_words = stopwords.words('english')
  #We create a list comprehension which only returns a list of words #that are NOT IN stop_words and NOT IN punctuations.
  keywords = [word for word in tokens if not word in stop_words and not word in punctuations]
  if keywords != []:
    k = anonymize(keywords)
    cats = categorize(k)
    if k == []:
      c += 1
    else:
      tokenized_keywords.append((t[0], k))
      tokenized_categories.append((t[0],cats))
      success_files.append(t[0])


# In[11]:


def loadGloveModel(gloveFile):
    print("Loading Glove Model")
    f = open(gloveFile,'r')
    model = {}
    for line in f:
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding
#     print("Done.",len(model)," words loaded!")
    return model


# In[12]:


glove_file = "glove_words.txt"
glove_model = loadGloveModel(glove_file)


# In[13]:


model_embeddings = {}
for tokenized_resume in tokenized_categories:
  resume_embeddings = {}
  # print(tokenized_resume)
  for cat in tokenized_resume[1]:
    # print(len(tokenized_resume[1][cat]))
    category_embeddings = {}
    for word in tokenized_resume[1][cat]:
      # print(word)
      if word in glove_model:
        if word in category_embeddings:
          # print(word)
          index = category_embeddings[word][0]
          index += 1
          category_embeddings[word] = (index, glove_model[word])
        else:
          category_embeddings[word] = (1, glove_model[word])
    # print(len(category_embeddings))
    if cat in resume_embeddings:
      index = resume_embeddings[cat][0]
      index += 1
      resume_embeddings[cat] = (index, category_embeddings)
    else:
      # print(category_embeddings)
      resume_embeddings[cat] = (1, category_embeddings)
  if tokenized_resume[0] in model_embeddings:
    index = model_embeddings[tokenized_resume[0]][0]
    index += 1
    model_embeddings[tokenized_resume[0]] = (index, resume_embeddings)
  else:
    model_embeddings[tokenized_resume[0]] = (1, resume_embeddings)


# In[14]:


single_embeddings = copy.deepcopy(model_embeddings)
for resume in single_embeddings:
  # print(resume)
  for activity in single_embeddings[resume][1]:
    # print(activity)
    for word_embedding in single_embeddings[resume][1][activity][1]:
      # print(model_embeddings[resume][1][activity][1][word_embedding])
      single_embeddings[resume][1][activity][1][word_embedding] = single_embeddings[resume][1][activity][1][word_embedding][0] * single_embeddings[resume][1][activity][1][word_embedding][1]


# In[15]:


resume_embeddings = []
for resume in single_embeddings:
  res_embedding = [resume, np.array([])]
  for activity in single_embeddings[resume][1]:
    activity_sum = np.zeros(50)
    counter = 0
    # print(single_embeddings[resume][1][activity][1])
    for word in single_embeddings[resume][1][activity][1]:
      activity_sum = np.add( activity_sum, single_embeddings[resume][1][activity][1][word])
      counter += 1
    if (counter != 0):
      activity_sum = activity_sum/counter
    res_embedding[1] = np.concatenate((res_embedding[1], activity_sum))
  resume_embeddings.append([res_embedding[0], res_embedding[1].tolist()])



# In[19]:


yx_label = {}
loaded_model = pickle.load(open("rf_model.sav", 'rb'))
prediction = loaded_model.predict_proba([resume_embeddings[0][1]])
# [('AI', 0),('Full_Stack', 1), ('Hardware', 2), ('Informatics', 3), ('Other', 4), ('SWE', 5),('Web_Developer', 6)]
yx_label[resume_embeddings[0][0]] = {
    "AI": prediction[0][0],
    "Full_Stack": prediction[0][1],
    "Hardware": prediction[0][2],
    "Informatics": prediction[0][3],
    "Other": prediction[0][4],
    "SWE": prediction[0][5],
    "Web_Developer": prediction[0][6],
}
print(yx_label)


# In[17]:


if os.path.exists(filename):
  os.remove(filename)
else:
  print("The file does not exist")


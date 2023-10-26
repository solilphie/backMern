from application.models import Application
from jobpost.models import Post
# from application.views import ListApplications
from api.serializers import ApplicationSerializer
from api.serializers import PostSerializer
import os 
from django.conf import settings
# import pickle
from rest_framework import viewsets
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from django.views.generic.list import ListView
from rest_framework import generics
from django.shortcuts import render
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import tensorflow as tf
import tensorflow.experimental.numpy as tnp
from tika import parser

tnp.experimental_enable_numpy_behavior()



def prep_text(text):
    punct = re.compile(r'[-.?!,:;()|]')
    no_punct = []
    for word in word_tokenize(text) :
        x=punct.sub("", word) #replace caracters in punt with "" in each word then put the word in x
        if len(x)>0 :
            no_punct.append(x)
  
    #stop_words = set(nltk.corpus.stopwords.words("english"))
    filtered_words = []
    for word in no_punct :
        if word not in (stopwords.words("english")) :
            filtered_words.append(word.lower())
    s_bigrams = list(nltk.bigrams(filtered_words))
    #type(s_bigrams[1])
    bg_words = []
    for bw in s_bigrams :
        bs = bw[0]+" "+bw[1]
        filtered_words.append(bs.lower())
    s_ngrams = list(nltk.ngrams(filtered_words , 3))
    for trig in s_ngrams:
      tgs = trig[0]+" "+trig[1]+" "+trig[2]
      filtered_words.append(tgs.lower())
    return filtered_words

all_skills = pd.read_excel(os.path.join(settings.BASE_DIR, 'models/skills.xlsx')) 
#print(all_skills)


def findhardskills(filtered_words,all_skills):
  foundhardSkills=[]
  for word in filtered_words :
    for skill in all_skills["technical"] :
      if (word.lower() == str(skill).lower()) and not (skill in foundhardSkills) :
        foundhardSkills.append(skill.lower()) 
  #foundhardSkills_df = pd.DataFrame(foundhardSkills)
  #foundhardSkills_df = foundhardSkills_df .drop_duplicates()   
  foundhardSkills = list(set(foundhardSkills))
  return(foundhardSkills)

def findsoftskills(filtered_words,all_skills):

  foundsoftSkills=[]
  for word in filtered_words :
      for skill in all_skills["soft"] :
          if word.lower() == str(skill).lower() and not (skill in foundsoftSkills):
            foundsoftSkills.append(skill.lower())
  #foundsoftSkills_df = pd.DataFrame(foundsoftSkills)
  #foundsoftSkills_df = foundsoftSkills_df .drop_duplicates() 
  foundsoftSkills = list(set(foundsoftSkills))      
  return(foundsoftSkills)

def nhardskills(foundhardskills):
  nhardSkills=len(foundhardskills)
  return(nhardSkills)


def nsoftskills(foundsoftskills):
  nsoftskills=len(foundsoftskills)
  return(nsoftskills)

def intersectskills(foundhardskills,jobhardskills,foundsoftskills, jobsoftskills):
  skills_intersec = []
  for f in foundhardskills:
    for fj in jobhardskills :
      if str(f) == str(fj):
        skills_intersec.append(str(f))
  for f in foundsoftskills:
    for fj in jobsoftskills :
      if str(f) == str(fj):
        skills_intersec.append(str(f))
  #skills_intersec = pd.DataFrame(skills_intersec).drop_duplicates()  
  nbr_skill_intersec = len(skills_intersec)
  print(skills_intersec)
  return skills_intersec

def degree(txt):
  cv = txt.lower()
  score_degree=0
  if "doctoral" in cv or "doctorate" in cv or "phd" in cv:
    score_degree=3
  elif "master" in cv or "masters" in cv or "mba" in cv :
    score_degree=2
  elif "bachelors" in cv or "bachelor" in cv or "bs" in cv:
    score_degree=1
  elif "high school/equivalent" in cv:
    score_degree=1
  return(score_degree)

def intersectdegree(job_txt,score_degree):
  job = job_txt.lower()
  degree_match = 0
  if score_degree in range(1,4):
    if "doctoral" in job or "doctorate" in job or "phd" in job: 
      degree_match = 1
    elif "master" in job or "masters" in job or "mba" in job :
      degree_match = 1
    elif "bachelors" in job or "bachelor" in job or "bs" in job:
      degree_match = 1
    elif "high school/equivalent" in job:
      degree_match = 1
  return(degree_match)

def years_exp_resume(cv):
  second_maximum=0
  sentences = []
  resume_words = word_tokenize(cv)
  first_result = 0
  numbers = []
  numbers_list = []
  for i in range(len(resume_words)):
    word = resume_words[i]
    if (word.lower()=="year") or (word.lower()=="years") :
      sentence = " ".join(resume_words[i-2:i+2])
      sentences.append(sentence) #all sentences that contain the word year or years
  if not sentences : 
    first_result = 0
  else : # if we found sentences containing year or years
    for s in sentences :
      num = re.findall(r'\d+', s) #find numbers in each sentence, this will return a list of lists that we will turn to list of integers
      numbers_list.append(num)
      int_numbers = []
      for i in range(len(numbers_list)) : 
        for j in range(len(numbers_list[i])) : 
          if int(numbers_list[i][j])<=50:
            int_numbers.append(int(numbers_list[i][j]))
    if not int_numbers:
      first_result=0
    else:
      first_result = max(int_numbers) #get the max of these ntegers(extracted years)
  exp=[] 
  list_years=[]
  list_years_numbers = []
  for line  in cv.splitlines():
    if "Date Posted" in line or "Availability Date" in line:
      continue
    for number in line.split():
      exp.append(number)
  for e in exp:
    list_years = re.findall(r'\d+', e)
    list_years_numbers.append(list_years)
  int_list = []
  for i in range(len(list_years_numbers)) : 
    for j in range(len(list_years_numbers[i])) :
      if  (int(list_years_numbers[i][j])>=1970) and (int(list_years_numbers[i][j])) <=2022 :
        int_list.append(int(list_years_numbers[i][j]))
  if not int_list :
    maxim = float("NaN")
  else :
    maximum=int_list[0]
    minimum=int_list[0]
  
    for elem in int_list:

      if elem>maximum:
        maximum = elem
      if elem<minimum:
        minimum=elem
      second_maximum = maximum-minimum
  resultat = max(first_result,second_maximum)
  return (resultat)

def distance(cv,job):
  count_vect = CountVectorizer()
  text_list = [cv, job]
  count_matrix = count_vect.fit_transform(text_list)
  matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
  matchPercentage = round(matchPercentage, 2) # round to two decimal
  return(matchPercentage)




class ViewRanking(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ApplicationSerializer
    def get(self, request, pk, *args, **kwargs):
      features_dataset = pd.DataFrame(columns = ["nbr_hardSkills_resume",
      "nbr_softSkills_resume",
      "skills_intersec",
      "degree_intersec",
      "years_of_exp",
      "distance"])
      
      #pk = self.kwargs['pk']
      jobcontent = Post.objects.filter(id=pk).values("content")
      for j in jobcontent:
        jobtext = j["content"]
      applications = Application.objects.filter(jobid=pk)
      inputs = pd.DataFrame(columns = ["job","resume"])
      for application in applications :
        f = parser.from_file("media/"+str(application.resume))
        file_content = str(f['content'])
        #print("file_content", type(file_content))
        #f = open("media/"+str(application.resume), 'r',encoding="utf8")
        #file_content = f.read()
        #f.close()
        inputs = inputs.append({"job":jobtext,"resume":file_content},ignore_index="True")
      #print(inputs)
      #df = pd.DataFrame()
      #print(df)
      for i in range(len(inputs)) :
        #print("i = ",i)
        resume_text = inputs["resume"].iloc[i]
        job_text = inputs["job"].iloc[i]
        print("resume_text",type(resume_text))
        resume_words = prep_text(resume_text)
        job_words = prep_text(job_text)
        resume_hard_skills = findhardskills(resume_words,all_skills)
        resume_soft_skills = findsoftskills(resume_words,all_skills)
        job_hard_skills = findhardskills(job_words,all_skills)
        job_soft_skills = findsoftskills(job_words,all_skills)
        resumeskills = resume_hard_skills + resume_soft_skills
        jobskills = job_hard_skills + job_soft_skills
        nbr_resume_hard_skills = len(resume_hard_skills)
        nbr_resume_soft_skills = len(resume_soft_skills)
        skills_intersection = len(intersectskills(resume_hard_skills,job_hard_skills,resume_soft_skills, job_soft_skills))
        
        degree_score = degree(resume_text)
        degree_intersection = intersectdegree(job_text,degree_score)
        
        years_experience = years_exp_resume(resume_text)
        dist = distance(resume_text,job_text)
        #
        #
        #
        features_dataset = features_dataset.append({"nbr_hardSkills_resume":nbr_resume_hard_skills,
                                                    "nbr_softSkills_resume":nbr_resume_soft_skills,
                                                    "skills_intersec":skills_intersection,
                                                    "degree_intersec":degree_intersection,
                                                    "years_of_exp":years_experience ,
                                                    "distance":dist},ignore_index=True)
      features_dataset=features_dataset.astype({"nbr_hardSkills_resume":"int",
                                        "nbr_softSkills_resume":"int",
                                        "skills_intersec":"int",
                                        "degree_intersec":"int",
                                        "years_of_exp":"int"
                                       })
      
      #print("features_dataset",features_dataset)
      my_model = tf.keras.models.load_model(os.path.join(settings.BASE_DIR, "models/keras97.h5"))

      numpy_dataset = features_dataset.to_numpy()
      numpy_dataset=np.asarray(numpy_dataset).astype(np.int)

      #print("numpy dataset",numpy_dataset)
      y_pred = my_model.predict(numpy_dataset)

      percentages = []
      predictions = []
      for p in y_pred:
        for pp in p:
          percentages.append("{0:.0%}".format(pp))
          predictions.append(1 if pp>0.5 else 0)
      #print("y_pred",y_pred)
      print("percentages",percentages)
      print("predictions",predictions)
      distances = features_dataset["distance"]
      iii = np.argsort(distances)
      indexes = iii[::-1]
      print(indexes)
      print("distance",features_dataset["distance"])

      return Response ({#"applications":applications,
                        "predictions":predictions,
                        "percentages":percentages,
                        "index":indexes,
                        "distance":features_dataset["distance"]})




def openapp (applications):
  for application in applications :
    print(application)
    f = open("media/"+str(application.resume), 'r',encoding="utf8")
    resume_text = f.read()
    f.close()
  return resume_text


class ViewDetails(generics.ListAPIView):
  # permission_classes = [IsAuthenticated]
  serializer_class = ApplicationSerializer
  def get(self, request, pk, *args, **kwargs):
    #pk = self.kwargs['pk']
    applications = Application.objects.filter(id=pk)
    idjob = applications[0].jobid
    for application in applications :
      #print(application)
      f = parser.from_file("media/"+str(application.resume))
      resume_text = str(f['content'])
      #f = open("media/"+str(application.resume), 'r',encoding="utf8")
      #resume_text = f.read()
      #f.close()
    jobcontent = Post.objects.filter(id=idjob).values("content")
    #job_text =""
    for j in jobcontent:
      print("j",j)
      job_text = j["content"]
    #print("job ",job_text)
    #print("resume ",resume_text)
    resume_words = prep_text(resume_text)
    job_words = prep_text(job_text)
    resume_hard_skills = findhardskills(resume_words,all_skills)
    resume_soft_skills = findsoftskills(resume_words,all_skills)
    job_hard_skills = findhardskills(job_words,all_skills)
    job_soft_skills = findsoftskills(job_words,all_skills)
    #resumeskills = resume_hard_skills + resume_soft_skills
    #jobskills = job_hard_skills + job_soft_skills
    #nbr_resume_hard_skills = len(resume_hard_skills)
    #nbr_resume_soft_skills = len(resume_soft_skills)
    skills_intersection = intersectskills(resume_hard_skills,job_hard_skills,resume_soft_skills, job_soft_skills)
    #nbr_skills_intersection = len(skills_intersection)
    
    degree_score = degree(resume_text)
    #degree_intersection = intersectdegree(job_text,degree_score)
    dist = distance(resume_text,job_text)
    years_experience = years_exp_resume(resume_text)
    #print("resume_soft_skills",job_text)
    return Response ({"hard" : resume_hard_skills,
                      "soft":resume_soft_skills,
                      "intersec":skills_intersection,
                      "degree":degree_score,
                      "yearsexp":years_experience,
                      "distance":dist
                      })
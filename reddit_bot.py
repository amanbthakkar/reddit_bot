
# coding: utf-8

# In[1]:


import praw
import os
import time
import requests
username="" #enter your details in these fields
password=""
client_id=""
client_secret=""


# In[2]:


def bot_login():
    print("Loggin in...")
    r=praw.Reddit(username=username,
        password=password,
        client_id=client_id,
        client_secret=client_secret,
        user_agent="aman tests stuff out");
    print ("Logged in!")
    return r


# In[3]:


def run_bot(r, replied_comments):
    for comment in r.subreddit("test").comments(limit=125):
        if "!joke" in comment.body and comment.id not in replied_comments and not comment.author == r.user.me():
            print ("joke request "+comment.id+" found in post")
            replied_comments.append(comment.id)
            #print(replied_comments)
            intro="It seems you requested for a joke! Here you go:\n\n>"
            joke=requests.get("http://api.icndb.com/jokes/random").json()['value']['joke']
            outro="\n\nThis joke is brought to you by ICNDB.com"
            comment.reply(intro+joke+outro)
            print(replied_comments)
            print("Replied to comment "+comment.id)
            with open ("repliedtocomments.txt","a") as f:
                f.write(comment.id+"\n")
        else:
            print ("No new joke request found")
    time.sleep(10)
    


# In[4]:


def get_saved_comments():
    if not os.path.isfile("repliedtocomments.txt"):
        repliedcomments=[]
    else:
        with open("repliedtocomments.txt", "r") as f:
            repliedcomments=f.read()
            repliedcomments=repliedcomments.split("\n")
            
            #repliedcomments=filter(None, repliedcomments)
    return repliedcomments
    


# In[5]:


replied_comments=get_saved_comments()
r=bot_login()
while True:
    run_bot(r, replied_comments)


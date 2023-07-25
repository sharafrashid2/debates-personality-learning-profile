import requests
import json
import praw

reddit = praw.Reddit(
    client_id="FILL WITH YOUR OWN CLIENT ID",
    client_secret="FILL WITH YOUR OWN SECRET ID",
    user_agent="my user agent",
)

def get_latest_submissions():
    submissions = set()
    # choose the subreddits you want to retrieve comments from here
    
    for submission in reddit.subreddit('spirituality+awakened+religion').top(time_filter='all'):
        submissions.add(submission)
    for submission in reddit.subreddit('spirituality+awakened+religion').hot(limit=500):
        submissions.add(submission)
    return submissions

submissions = get_latest_submissions()
print(len(submissions))

comments = []
count = 0
for submission in submissions:
    submission.comments.replace_more(limit=15)
    for comment in submission.comments.list():
        if count % 100 == 0:
            print('check')
        comments.append(comment.body)
        count += 1

print('finished')

comments_json = json.dumps(comments)

# saves comments in a json
jsonFile = open("spiritualist.json", "w")
jsonFile.write(comments_json)
jsonFile.close()

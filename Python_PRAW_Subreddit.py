#import praw + In Terminal run: python -m textblob.download_corpora
import praw
reddit = praw.Reddit(client_id = "", client_secret = "", password = "", username = "", user_agent = "")

subreddit = reddit.subreddit("dubstep")
submissions = list(subreddit.top('week'))
for submission in submissions:
    if not submission.stickied:
        print("Title: {}, ups: {}, Have we visited?: {}".format(submission.title,submission.ups, submission.visited))

# grab the x submission comments by which number you choose
submission = submissions[0]
# the actual text is in the body
# attribute of a Comment
def get_comments(submission, n= 256):
    """
    Return a list of comments from a submission.
    
    We can't just use submission.comments, because some
    of those comments may be MoreComments classes and those don't
    have bodies.
    
    n is the number of comments we want to limit ourselves to
    from the submission.
    """
    count = 0
    def barf_comments(iterable=submission.comments):
        nonlocal count
        for c in iterable:
            if hasattr(c, 'body') and count < n:
                count += 1
                yield c.body
            elif hasattr(c, '__iter__'):
                # handle MoreComments classes
                yield from barf_comments(c)
            else:
                # c was a Comment and did not have a body
                continue
    return barf_comments()
                
comments = list(get_comments(submission))
list(comments)    

for comment in submission.comments.list():
    print(comment.ups)
    print(comment.author)
    print(comment.body)


#Sentiment Analysis
from textblob import TextBlob
comment_blob = TextBlob(''.join(comments))
more_comments = []
for submission in submissions:
    more_comments.extend(get_comments(submission, 200))
len(more_comments)

#Get the amount of words of comments
bigger_blob = TextBlob(''.join(more_comments))
print(len(bigger_blob.words))

#Count the certain amount of words you would like/frequency
from collections import Counter
counter = Counter(bigger_blob.words)
#the most common words are pretty mundane common parts of speech, so we'll skip the first few
counter.most_common()[50:200]

# The sentiment property returns a namedtuple of the form Sentiment(polarity, subjectivity). The polarity score is a float within the range [-1.0, 1.0]. The subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.
bigger_blob.sentiment

####copy and paste what you get from counter.most_common()
data =

import numpy as np
import pandas as pd
df = pd.DataFrame(np.array(data), columns=['Word', 'Amount'])
print(pd.DataFrame(df))
df.to_csv("test.csv", encoding='utf-8')

dubstep = pd.read_csv("test.csv", encoding = "ISO-8859-1")
fans = dubstep[["Word", "Amount"]]
fans.head()

rcParams['figure.figsize'] = 8, 36
plt.rc('ytick', labelsize = 8)

my_plot = fans.plot.barh(title="Words used on r/dubstep for Lost Lands Lineup Announcement")
my_plot.set_xlabel("Amount")
my_plot.set_ylabel("Words")
plt.grid(True)
plt.show()
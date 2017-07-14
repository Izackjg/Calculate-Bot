from sympy import *
import praw
import re

def is_numeric(s):
    allowed_chars = ["+", "-", "*", "/", "**", "^", "//", "(", ")"]
    if any(x in s for x in allowed_chars) and re.compile("\d+"):
        return True
    return False


def type_calculation(type):
    f_index = type.index("(")
    l_index = type.index(")")
    if type == "expand":
        result = expand(type[f_index + 1:l_index])
        return result
    elif type == "simplify":
        result = simplify(type[f_index + 1:l_index])
        return result


def did_reply(filepath, id):
    if id in open(filepath).read():
        return True
    return False

def reply(reddit, amount):
    for comment in reddit.subreddit(test_sub).comments(limit=amount):
        has_replied = did_reply(comments_replied_filename, comment.id)
        valid_string = is_numeric(comment.body)
        not_bot = comment.author != reddit.user.me()
        if not has_replied and valid_string and not_bot:
            f_index = comment.body.index("(")
            l_index = comment.body.index(")", len(comment.body) - 1)
            if comment.body[:f_index] == "expand":
                result = expand(comment.body[f_index + 1:l_index])
                quote = "> {}".format(comment.body[f_index + 1:l_index])
                comment_reply = "{q} \n\n = {r}".format(q=quote.replace(" ", ""), r=result).replace("**", "^")
                print("Replying")
                comment.reply(comment_reply)

                

        
reddit = praw.Reddit("bot1")
test_sub = "PythonInfoBotTest"
submission_id = "6mmzhz"
bot_name = "UserInfo_Bot"
bot_profile = reddit.redditor(bot_name) 

blacklisted_subs_filepath = "C:\\Users\\Gutman\\Desktop\\Reddit_Bot\\blacklisted_subreddits.txt"
blacklisted_users_filepath = "C:\\Users\\Gutman\\Desktop\\Reddit_Bot\\blacklisted_users.txt"
posts_replied_filepath = "C:\\Users\\Gutman\\Desktop\\Reddit_Bot\\posts_replied.txt"
comments_replied_filename = "C:\\Users\\Gutman\\Desktop\\Reddit_Bot\\comment_replied.txt"

reply(reddit, 5)

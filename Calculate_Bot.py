import sys
import praw
import re   
from time import sleep
from sympy import *

DEBUG = True
DEBUG_TYPE = "sub"
TEST_SUBREDDIT_NAME = "PythonInfoBotTest"
TEST_SUBMISSION_ID = "6x9gmo"
COMMENT_LIMIT = 500

BOT_USERNAME = "UserInfo_Bot"
EXCLUDE_STRINGS = ["ExcludeMe", "ExcludeSubreddit"]
INCLUDE_STRING = "IncludeMe"
DOWNVOTE_REMOVE_FOOTER = "^(Downvote To Remove)"
FOOTER_SEPERATOR = "^|"

blacklisted_subs_filepath = "blacklisted_subreddits.txt"
blacklisted_users_filepath = "blacklisted_users.txt"
posts_replied_filepath = "posts_replied.txt"
comments_replied_filename = "comment_replied.txt"

reddit = praw.Reddit("bot1")
calculation_types = {"expand" : expand, "solve" : solve, "diff" : diff, "simplify" : simplify}


def contains_symbols(comment_body):
    allowed_chars = ["+", "-", "*", "/", "**", "^", "//", "(", ")"]
    return any(char in comment_body for char in allowed_chars)

def did_reply(file_path, comment_id):
    return comment_id in open(file_path).read()

def write_id_to_file(file_path, comment_id):
    with open(file_path, "a") as f:
        f.write(comment_id + "\n")

def remove_comment(bot_profile):
    threshold = 0
    for comment in bot_profile.comments.controversial(limit=None):
        if comment.score < threshold:
            comment.delete()
        elif comment.author == None:
            if comment.boy == "[removed]" or comment.body == "[deleted]":
                comment.delete()

def string_prefix(calc_types, comment):
    if type(comment) is not str:
        raise TypeError("type of comment body must be of type string")
    elif type(calc_types) is not dict:
        raise TypeError("type of calc_types must be of type dict")
    else:
        if comment.body:
            paren_index_one = comment.body.index("(")
            paren_index_two = comment.body.index(")", comment.body[-1])
            calculation_prefix = comment.body[:paren_index_one]
            equation = comment.body[paren_index_one + 1:paren_index_two]
            for key, item in calc_types.items():
                if key == calculation_prefix:
                    return calculation_prefix, equation, calc_types[calculation_prefix](equation)
            return None    
        
def generate_reply(comment):
    comment_prefix, equation, result = string_prefix(calculation_types, comment)
    if "**" in equation:
        equation = equation.remove("**", "^")
    quote = "> {}({})".format(comment_prefix, equation)
    footer = "[{}]".format(DOWNVOTE_REMOVE_FOOTER)
    reply = "{} \n\n= {} \n\n*** {}".format(quote, result, footer)
    return reply
            
def main():
    try:
        for comment in reddit.submission(TEST_SUBMISSION_ID).comments(limit=50):
            if not did_reply(comments_replied_filename, comment.id):
                if not comment.author == reddit.user.me():
                    if contains_symbols(comment.body):
                        comment_reply = generate_reply(comment)
                        comment.reply(comment_reply)
                        print("replying")

                        write_id_to_file(comments_replied_filename, comment.id)
    except Exception as e:
        if e == praw.exceptions.APIException:
            print("rate limit exceeded, sleeping 100 seconds")
            sleep(100)

            
if __name__ == "__main__":
    sys.exit(int(main() or 0)) 

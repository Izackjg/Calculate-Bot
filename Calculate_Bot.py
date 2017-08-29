import sys
import praw
import re
from time import sleep
from sympy import *

# TODO - Have solve function return +-(result) instead of a list of results. Maybe?

def contains_symbols(comment_body):
    allowed_chars = ["+", "-", "*", "/", "**", "^", "//", "(", ")"]
    if any(char in comment_body for char in allowed_chars):
        return True
    return False

def did_reply(file_path, id):
    if id in open(file_path).read():
        return True
    return False

def remove_comment(bot_profile):
    threshold = 0
    for comment in bot_profile.comments.controversial(limit=None):
        if comment.score < threshold:
            comment.delete()
            print("comment deleted - downvoted @ {} with {} score".format(comment.id, comment.score))
        elif comment.author == None:
            if comment.body == "[removed]" or comment.body == "[deleted]":
                comment.delete()
                print("comment author deleted/removed")

def calculate_string(comment_body):
    """ Pass the comment body object from the praw API.
        No need to pass the comment body formatted in any way.
        Since this function will do the calculations and string formatting. """
    if type(comment_body) is not str:
        raise TypeError("type of comment body must be type of string")
    else:
        if comment_body:
            dict_types = {"expand" : expand, "solve" : solve, "diff" : diff, "simplify" : simplify}
            paren_index_one = comment_body.index("(")
            paren_index_two = comment_body.index(")", len(comment_body) - 1)
            type_string = comment_body[:paren_index_one]
            eq_string = comment_body[paren_index_one + 1:paren_index_two]
            for key, item in dict_types.items():
                if key == type_string:
                    return type_string, eq_string, dict_types[type_string](eq_string)
            return None

def reply(reddit, amount, debug=True):  
    test_sub = reddit.subreddit("PythonInfoBotTest")
    test_submission = reddit.submission("6w5mcu")
    replied_comments_file = "C:\\Users\\Gutman\\Desktop\\Reddit_Bot\\comment_replied.txt"

    if debug:
        try:
            for comment in test_sub.comments():
                has_replied = did_reply(replied_comments_file, comment.id)
                is_bot = comment.author == reddit.user.me()
                valid_string = contains_symbols(comment.body)
                if not has_replied and not is_bot and valid_string:
                    calculation_type, comment_equation, equation_result = calculate_string(comment.body)
                    if "**" in comment_equation:
                        comment_equation = comment_equation.replace("**", "^")
                    quote_reply = "> {}({})".format(calculation_type, comment_equation)
                    comment_reply = "{} \n\n= {}".format(quote_reply, equation_result)
                    comment.reply(comment_reply)
                    print("replying")

                    with open(replied_comments_file, "a") as f:
                        f.write(comment.id + "\n")
        except Exception as e:
            if e == praw.exceptions.APIException:
                print("rate_limit reached, sleeping 100 seconds")
                sleep(100)




def main():
    reddit = praw.Reddit("bot1")
    test_sub = "PythonInfoBotTest"
    submission_id = "6mmzhz"
    bot_name = "UserInfo_Bot"
    bot_profile = reddit.redditor(bot_name) 

    blacklisted_subs_filepath = "C:\\Users\\Gutman\\Desktop\\Reddit_Bot\\blacklisted_subreddits.txt"
    blacklisted_users_filepath = "C:\\Users\\Gutman\\Desktop\\Reddit_Bot\\blacklisted_users.txt"
    posts_replied_filepath = "C:\\Users\\Gutman\\Desktop\\Reddit_Bot\\posts_replied.txt"
    comments_replied_filename = "C:\\Users\\Gutman\\Desktop\\Reddit_Bot\\comment_replied.txt"

    remove_comment(bot_profile)
    reply(reddit, None)
     

if __name__ == "__main__":
    sys.exit(int(main() or 0))      

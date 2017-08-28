import sys
import praw
import re
from sympy import *

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
            dict_types = {"expand" : expand, "solve" : solve, "diff" : diff}
            paren_index_one = comment_body.index("(")
            paren_index_two = comment_body.index(")", len(comment_body) - 1)
            type_string = comment_body[:paren_index_one]
            eq_string = comment_body[paren_index_one + 1:paren_index_two]
            for key, item in dict_types.items():
                if key == type_string:
                    return type_string, eq_string, dict_types[type_string](eq_string)
            return None

def reply(reddit, amount):
    items = ["PythonInfoBotTest", "C:\\Users\\Gutman\\Desktop\\Reddit_Bot\\comment_replied.txt"]
    replace_char = "^"
    white_space = " "
    try:
        for comment in reddit.subreddit(items[0]).comments(limit=amount):
            has_replied = did_reply(items[1], comment.id)
            valid_string = contains_symbols(comment.body)
            not_bot = comment.author != reddit.user.me()
            if not has_replied and valid_string and not_bot:
                calc_type_str, equation_str, result = calculate_string(comment.body)
                if replace_char in equation_str:
                    equation_str = equation_str.replace(replace_char, "**")
                if white_space in equation_str:
                    equation_str = equation_str.replace(white_space, "")
                quote_string = "> {}({})".format(calc_type_str, equation_str)
                comment_reply = "{q} \n\n = {r}".format(q=quote_string, r=result)
                comment.reply(comment_reply)
                print("replying")

                with open(items[1], "a") as f:
                    f.write(comment.id + "\n")
    except Exception as e:
        pass 

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
    reply(reddit, 50)
     

if __name__ == "__main__":
    sys.exit(int(main() or 0))      

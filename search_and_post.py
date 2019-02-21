from twitter import search_tweets
from slack import read_last_id, post_message
from const import post_message_template, result_header_format, query_strings
from secret_info import slack_channel_id, slack_direct_message_id
from jinja2 import Template


def post_tweets_to_slack(tweets):
    """
    Search tweets and post them to a Slack channel
    :param Status tweets: Status object (tweet) to post to Slack
    :return: the id of the latest tweet among the tweets
    :rtype: int
    """
    max_id = 0
    for tw in tweets:
        tw_template = Template(post_message_template)
        post_text = tw_template.render(tweet=tw)
        post_message(post_text, slack_channel_id)
        # Update max_id when the tweet has larger ID than current one.
        if tw.id > max_id:
            max_id = tw.id
    return max_id


def main():
    since_id = read_last_id()
    # If since_id can not be convertible to int, refresh it.
    if not since_id.isdigit():
        since_id = '1'
    # Initialize largest_id which will be new since_id
    largest_id = int(since_id)

    for q in query_strings:
        tweets = search_tweets(q, since_id)
        if len(tweets) > 0:
            # Post a header
            post_message(result_header_format.format(query=q), slack_channel_id)
            max_id = post_tweets_to_slack(tweets)
            # Update largest_id when one of tweets has larger ID than the
            # current.
            if max_id > largest_id:
                largest_id = max_id

    post_message(largest_id, slack_direct_message_id)


if __name__ == '__main__':
    main()

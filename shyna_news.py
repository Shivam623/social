from newsapi import NewsApiClient
from shyna_back import news_api_key, send_msg_to_master, get_date,subtract_date
news_api = NewsApiClient(api_key=news_api_key())


def get_news_where_topic_is(topic):
    top_headlines = news_api.get_top_headlines(q=topic,language='en',country='in')
    send_msg_to_master(message="Collecting news on"+str(topic))
    for row in top_headlines['articles']:
        send_msg_to_master(message="News I Found is Published on: "+str(row['publishedAt']))
        send_msg_to_master(message="Title: "+str(row['title']))
        send_msg_to_master(message="Description: "+str(row['description']))
        send_msg_to_master(message="content: "+str(row['content']))
        send_msg_to_master(message=str(row['url']))
        send_msg_to_master(message =str(row['urlToImage']))
        send_msg_to_master(message="Next News I Found is:")


def get_everything_where_topic_is(topic):
    top_headlines = news_api.get_top_headlines(q=topic,language='en')
    send_msg_to_master(message="Collecting news on"+str(topic))
    for row in top_headlines['articles']:
        send_msg_to_master(message="News I Found is Published on: "+str(row['publishedAt']))
        send_msg_to_master(message="Title: "+str(row['title']))
        send_msg_to_master(message="Description: "+str(row['description']))
        send_msg_to_master(message="content: "+str(row['content']))
        send_msg_to_master(message=str(row['url']))
        send_msg_to_master(message =str(row['urlToImage']))
        send_msg_to_master(message="Next News I Found is:")


def get_sources_where_country_is(country):
    sources = news_api.get_sources(country=country)
    for row in sources['sources']:
        print(row)


def news_where_source_is(source):
    news = news_api.get_everything(sources=source)
    for row in news['articles']:
        send_msg_to_master(message="News I Found is Published on: "+str(row['publishedAt']))
        send_msg_to_master(message="Title: "+str(row['title']))
        send_msg_to_master(message="Description: "+str(row['description']))
        send_msg_to_master(message="content: "+str(row['content']))
        send_msg_to_master(message=str(row['url']))
        send_msg_to_master(message =str(row['urlToImage']))


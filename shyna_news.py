from newsapi import NewsApiClient
from shyna_back import news_api_key, send_msg_to_master, convert_time_zone
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
    source_list=[]
    sources = news_api.get_sources(country=country, language='en')
    for row in sources['sources']:
        source_list.append(row['id'])
    return source_list


def news_where_source_is(source):
    news = news_api.get_everything(sources=source)
    for row in news['articles']:
        send_msg_to_master(message="News I Found is Published on: "+str(row['publishedAt']))
        send_msg_to_master(message="Title: "+str(row['title']))
        send_msg_to_master(message="Description: "+str(row['description']))
        send_msg_to_master(message="content: "+str(row['content']))
        send_msg_to_master(message=str(row['url']))
        send_msg_to_master(message =str(row['urlToImage']))


def news_for_anlysis():
    try:
        news=[]
        country_list = ['in','us','cn','it']
        for country in country_list:
            print("News from ",country," source")
            source_list=get_sources_where_country_is(country)
            for source in source_list:
                news = news_api.get_everything(sources=source, language='en')
                for row in news['articles']:
                    title ="row_is"+str(row['title'])
                    description = 'row_is'+str(row['description'])
                    if str(title) == 'row_is' or description == 'row_is':
                        pass
                    else:
                        published_At= convert_time_zone(from_zone='UTC', time_value=str(row['publishedAt']))
                        title=row['title']
                        description=row['description']
                        content_link=row['url']
                        image=row['urlToImage']
                        analysis(publish_at=published_At, title=title, description=description, content_link=content_link, image_link=image)
                print("PRINTING HEADLINES")
                news = news_api.get_top_headlines(sources=source, language='en')
                for row in news['articles']:
                    title ="row_is"+str(row['title'])
                    description = 'row_is'+str(row['description'])
                    if str(title) == 'row_is' or description == 'row_is':
                        pass
                    else:
                        published_At= convert_time_zone(from_zone='UTC', time_value=str(row['publishedAt']))
                        title=row['title']
                        description=row['description']
                        content_link=row['url']
                        image=row['urlToImage']
                        analysis(publish_at=published_At, title=title, description=description, content_link=content_link, image_link=image)
                        print("\n\n\n\n\n")
    except Exception as e:
        print(e)



def analysis(publish_at, title, description, content_link, image_link):
    new_keyword = ['COVID-19', 'covid-19', 'corona virus', 'donation','dead', 'death', 'cases', 'rape', 'murder']
    try:
        for keyword in new_keyword:
            if str(title).__contains__(keyword) or str(description).__contains__(keyword):
                print(publish_at)
                print(title)
                print(description)
                print(content_link)
                print(image_link)
    except Exception as e:
        print(e)


news_for_anlysis()
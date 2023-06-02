if __name__ == '__main__':
    from pymongo.mongo_client import MongoClient
    from pymongo.server_api import ServerApi
    import botsecrets
    import json
    import codecs


    def open_json():
        with codecs.open('q.json', 'r', 'utf-8') as file:
            return json.load(file)

    # Create a new client and connect to the server
    # c = MongoClient(botsecrets.mongo_uri, server_api=ServerApi('1'))
    # db = c["Vewem"]
    # qs = db["quotes"]

    j = open_json()
    quotes = j['Quotes']

    q = quotes[0]
    a = q['author']

    attachments = q['attachments']
    embeds = q['embeds']
    reactions = q['reactions']
    print(q)
    print(a)

    row_author = {
        'id': a['id'],
        'username': a['username'],
        'avatar': a['avatar'],
        'discriminator': a['discriminator'],
        'bot': a['bot'],
    }

    row = {
        'id': q['id'],
        'channel_id': q['channel_id'],
        'content': q['content'],
        'timestamp': q['timestamp'],  # date
        'author': row_author,
        'attachments': q['attachments'],
        'embeds': q['embeds'],
    }
    # for q in quotes:
    #     a = q['author']
    #     print(q)
    #     print(a)
    #     pass
    # for q in data['Quotes']:
    #     a = q['author']
    #     print(q)
    #     ins_author = {
    #         'id': a['id'],
    #         'username': a['username'],
    #         'avatar': a['avatar'],
    #         'discriminator': a['discriminator'],
    #         'bot': a['bot'],
    #     }
    #     ins_quote = {
    #         'id': q['id'],
    #         'channel_id': q['channel_id'],
    #         'content': q['content'],
    #         'timestamp': q['timestamp'],
    #         'author': ins_author,
    #         attachments
    #         embeds
    #         mentions
    #
    #     }

from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import datetime
import random
import json
import emoji

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"
    
@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if incoming_msg == 'hello' or 'hi' or 'hola' or 'hiya' or 'hey' or 'sup' or 'wassup':
        response = emoji.emojize("""
Hello, I am your friendly neighbourhood bot :grinning_face_with_big_eyes:
I was built by *Sadhana Kalyana Raman*. 
If you type:
:black_small_square: '*quote*': You'll hear an inspirational quote! :star:
:black_small_square: '*cat*': I will send you a cute cat picture :cat:
:black_small_square: '*dog*': You'll get a lovely dog picture :dog:
:black_small_square: '*meme*': You'll receive the top memes from reddit. :beaming_face_with_smiling_eyes:
:black_small_square: '*news*': You can read the latest news. :newspaper:
But this is not all, I was designed to converse and can make small talk. 
Don't hesitate to tell me about your day or ask me for a joke. 
Let's chat! :beaming_face_with_smiling_eyes:
""")
        msg.body(response)
        responded = True

    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True
    elif 'cat' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True
    elif 'dog' in incoming_msg:
        # return a dog pic
        r = requests.get('https://dog.ceo/api/breeds/image/random')
        data = r.json()
        msg.media(data['message'])
        responded = True
    elif 'meme' in incoming_msg:
        
        r = requests.get('https://www.reddit.com/r/memes/top.json?limit=20?t=day', headers = {'User-agent': 'your bot 0.1'})
            
        if r.status_code == 200:
            data = r.json()
            memes = data['data']['children']
            random_meme = random.choice(memes)
            meme_data = random_meme['data']
            title = meme_data['title']
            image = meme_data['url']

            msg.body(title)
            msg.media(image)
            
        else:
            msg.body('Sorry, I cannot retrieve memes at this time.')
        responded = True
    elif 'news' in incoming_msg:
        r = requests.get('https://newsapi.org/v2/top-headlines?sources=bbc-news,the-washington-post,the-wall-street-journal,cnn,fox-news,cnbc,abc-news,business-insider-uk,google-news-uk,independent&apiKey=3ff5909978da49b68997fd2a1e21fae8')
            
        if r.status_code == 200:
            data = r.json()
            articles = data['articles'][:5]
            result = ''
                
            for article in articles:
                title = article['title']
                url = article['url']
                if 'Z' in article['publishedAt']:
                    published_at = datetime.datetime.strptime(article['publishedAt'][:19], "%Y-%m-%dT%H:%M:%S")
                else:
                    published_at = datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%S%z")
                result += """
*{}*
Read more: {}
_Published at {:02}/{:02}/{:02} {:02}:{:02}:{:02} UTC_
""".format(
    title,
    url, 
    published_at.day, 
    published_at.month, 
    published_at.year, 
    published_at.hour, 
    published_at.minute, 
    published_at.second
    )

        else:
            result = 'I cannot fetch news at this time. Sorry!'

        msg.body(result)
        responded = True    
    if not responded:
        msg.body('Sorry, but I do not understand, try again?')
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

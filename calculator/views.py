from django.shortcuts import render, redirect
from .models import Word
from bs4 import BeautifulSoup as soup
from nltk.tokenize import word_tokenize
from urllib.request import urlopen as uReq
from django.contrib import messages
import validators


def home(request):
    return redirect('frequency')


def frequency(request):
    if request.method == "POST":
        words = Word.objects.all()
        address = request.POST['url']
        if not validators.url(address):
            messages.error(request, 'Enter a valid URL address')
            return redirect('frequency')
        else:
            for i in words:
                if i.url == address:
                    request.session['url'] = address
                    messages.success(request, 'Url found in Database')
                    return redirect('result')
            uclient = uReq(address)
            if uclient.getcode() == 200:
                page_html = uclient.read()
                uclient.close()
                page_soup = soup(page_html, 'html.parser')
                text = word_tokenize(page_soup.body.text)

                count = {}
                for x in text:
                    if x in count.keys():
                        count[x] += 1
                    else:
                        count[x] = 1

                def get_key(val):
                    for key, value in count.items():
                        if val == value:
                            return key

                keys = [i for i in count.keys()]
                values = [i for i in count.values()]
                values = sorted(values, reverse=True)
                arranged_words = []
                for i in values:
                    arranged_words.append(get_key(i))
                    del count[str(get_key(i))]
                arranged_words = list(dict.fromkeys(arranged_words))
                valid_words = []
                for i in arranged_words:
                    if len(i) > 4 and len(i) < 12:
                        valid_words.append(i)
                temp = {}
                for x in text:
                    if x in temp.keys():
                        temp[x] += 1
                    else:
                        temp[x] = 1
                for i in range(0, 10):
                    word = valid_words[i]
                    key = temp[valid_words[i]]
                    newWord = Word(url=address, word=word, repeat=key)
                    newWord.save()
                request.session['url'] = address
                messages.success(request, 'URL is Freshly Processed')
                return redirect('result')
            else:
                messages.error(request, 'Website not found')
                return redirect('frequency')
    return render(request, 'calculator/frequency.html')


def result(request):
    url = request.session.get('url')
    words = Word.objects.filter(url=url)
    context = {'words': words, 'url': url}
    request.session['url'] = ''
    return render(request, 'calculator/result.html', context)

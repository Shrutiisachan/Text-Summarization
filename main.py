from flask import Flask, request, render_template
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form.get('text')
        stopWords = set(stopwords.words("english"))
        words = word_tokenize(text)
        freqTable = dict()
        for word in words:
            word = word.lower()
            if word in freqTable and word not in stopWords:
                freqTable[word] += 1
            else:
                freqTable[word] = 1
        sentences = sent_tokenize(text)
        sentenceValue = dict()
        for sentence in sentences:
            for word, freq in freqTable.items():
                if word in sentence.lower():
                    if sentence in sentenceValue:
                        sentenceValue[sentence] += freq
                    else:
                        sentenceValue[sentence] = freq
        sumValues = 0
        for sentence in sentenceValue:
            sumValues += sentenceValue[sentence]
        average = int(sumValues / len(sentenceValue))
        summary = ''
        summary_list = []
        for sentence in sentences:
            if (sentence in sentenceValue) and (sentenceValue[sentence] > average):
                summary_list.append(sentence)
        summary_list.sort(reverse=True)
        summary = " ".join(summary_list[0:int(len(sentences))])
        return render_template('index.html', summary=summary)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
import re
import nltk
import heapq
article_text = 'We have entered and have always been in a network era. Realizing it or not, there are all sorts of network around us such as Internet, power station network, water flow network and so on. Among all those networks, a huge amount ofthem share a common feature ofpossible node failure and failure propagation to neighbors. Routers could get jammed by hackers or simply by too many unintentional data packages and there is a high chance that your neighbor routers be jammed too. The goal ofthis project is to use Monte Carlo simulation technique to simulate such phenomenon in order to obtain some useful information so that it can be used to compare with results ofother more advanced study. Since there are so many networks around us, try to simulate all ofthem will be impossible and unnecessary. A typical network representation of such networks, United States power station network will be used to fulfil our goal based on several reasons. First of all U.S. power network is a relatively well-defmed network compared with other networks such as Internet. Secondly U.S. power station network is more static, we wont build a power station every day, while to Internet, many new nodes appear each day. Thirdly it is relatively simpler than some other networks, there arent so many nodes in the network, small number of nodes makes visualization possible. The final reason is that there is some fmancial application with the simulation ofU.S. power station networks. There are many contractors who want to buy power from power stations and sell power from consumers. Ifeach power station can generate the desired power and each consumer restricted himselfto assigned power and the number ofconsumers stay fixed, then the problem degenerates to a static network problem. However, things are not always so simple and perfect. There is always a chance that each power station can fail or 3 consumers can ask for more power or there is simply higher population such as current power crisis in c.A. or even more unpredictably, nature disasters can shut down power plants or connection wires. Contractors need to worry about these problems in order to make it more profitable. One feature of such problem is that when a power plant fails, for example, caused by higher demands or nature disasters, there is a high chance that some neighborhood power plants will fail too. When one power plant fails due to high demand, consumers will turn to neighbor power plants and make them fail too. Nature disasters can happen in a broad area, not just a specific area. Meanwhile, if a linkage between power plants or power plants and consumers fail, neighbor linkages can fail too. This report and the software package is used for this specific kind ofnetworks with emphasis on U.S. power plant network. A detailed topology ofU.S. power plant network is also available, which makes the study easier and more direct. This report uses Monte Carlo simulation technique to do the study. The result ofthe simulation will be used to compare with some common sense in order to make sure there is bug in the software package. The choice ofMonte Carlo simulation technique is mainly because ofthe stochastic feature of the problem itself and the simulation technique.  '

article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
article_text = re.sub(r'\s+', ' ', article_text)
formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

sentence_list = nltk.sent_tokenize(article_text)

stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}
for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

maximum_frequncy = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

sentence_scores = {}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 30:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]

summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

summary = ' '.join(summary_sentences)
print(summary)

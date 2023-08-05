class SlyText(object):
    def __init__(self, *text):
        self.text = text
        print(self.text)

    @property
    def translate(self):
        import translators as ts
        return [ts.bing(i, if_use_cn_host=True) for i in self.text]

    @property
    def gender(self):
        import ngender as nd
        return [nd.guess(i) for i in self.text]

    def compare(self, accurate=True):
        from fuzzywuzzy import fuzz
        if accurate == True:
            return fuzz.ratio(self.text[0], self.text[1])/100
        else:
            return fuzz.partial_ratio(self.text[0], self.text[1])/100

    def sentiment(self, language='C'):
        if language == 'E':
            from textblob import TextBlob
            result = {}
            for i in self.text:
                blob = TextBlob(i)
                result[i] = blob.sentiment[0]
            return result
        elif language == 'C':
            from snownlp import SnowNLP
            result = {}
            for i in self.text:
                s = SnowNLP(i)
                result[i] = s.sentiments
            return result
        else:
            print('Please choose a correct languge!')

    def heart(self):
        for name in self.text:
            try:
                print('\n'.join([''.join([(name[(x-y) % len(list(name))]if((x*0.05)**2+(y*0.1)**2-1)**3-(
                    x*0.05)**2*(y*0.1)**3 <= 0 else' ')for x in range(-30, 30)])for y in range(15, -15, -1)]))
            except:
                print('请输入字符串！')

    @property
    def voice(self):
        import pyttsx3
        engine = pyttsx3.init()
        for i in self.text:
            engine.say(i)
            engine.runAndWait()

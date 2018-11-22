# python-snippets
Just a place to store some often used Python snippets.


### Simple Logger

```
class Logger:
    def __init__(self, logname, verbose):
        self._verbose = verbose
        print("Logging to file: " + logname + ".log")
        self._log_file = open(logname + ".log", "w")
        self._result_file = open(logname + ".result", "w")

    def logmsg(self, msg):
        self._log_file.write(msg)
        if self._verbose:
            print(msg, end='')

    def resultmsg(self, msg):
        self._result_file.write(msg)
        if self._verbose:
            print(msg)

    def logclose(self):
        self._log_file.write("\n\n")
        self._result_file.write("\n\n")
        self._log_file.close()
```

### Text

```
with open("Project1TestQuestions.txt", "r", encoding="utf-8") as f:
    _questions = f.readlines()

for _question in _questions:
    words = _question.rstrip('\n').split(' ')
    print(words)
```
```
with open("vacabulary.txt", "r", encoding="utf-8") as f:
    _vocabulary = [line.rstrip() for line in f]

with open("sentences.txt", "r", encoding="utf-8") as f:
    _sentences = [line.rstrip() for line in f]

for _sentence in _sentences:
    _words = _sentence.split(' ')
    for _word in _words:
        if _word not in _vocabulary:
            print(_word)
```

### Checking text for vocabulary

```
with open("vacabulary.txt", "r", encoding="utf-8") as f:
    _vocabulary = [line.rstrip().lower() for line in f]

with open("sentences.txt", "r", encoding="utf-8") as f:
    _sentences = [line.rstrip().lower() for line in f]

_max_words_in_sentence = 0
_new_words = list()
for _sentence in _sentences:
    _words = _sentence.split(' ')
    _max_words_in_sentence = max(_max_words_in_sentence,len(_words))
    for _word in _words:
        if _word not in _vocabulary:
            if not _word.isdigit():
                _new_words.append(_word)
_unique_words = set(_new_words)
for _word in _unique_words:
    print(_word)

print("Max words in sentence: ", _max_words_in_sentence)
```


### json

```
import json
    try:
        with open(_frame_filename, encoding='utf-8') as json_data:
            _ground_truth_frames = json.load(json_data)
    except Exception as e:
        print("Failure opening or reading frames: " + str(e))
        return 1

import json
with open('TestQuestions.json', 'w') as outfile:
    json.dump(listOfDicts, outfile)
```


### Command Line Interface

```
import sys, getopt

def main(argv):

    parameters = {
                    'verbose': False,
                    'frames': "ExampleQuestions.json",
                    'log': "results"
                 }

    print(__doc__)
    try:
        opts, args = getopt.getopt(argv, "vf:l:")
    except getopt.GetoptError:
        sys.exit(1)
    for opt, arg in opts:
        if opt in ("-v"):  # -v verbose
            parameters['verbose'] = True
        elif opt in ("-f"):  # -f <json containing dictionary frames>
            parameters['frames'] = arg
        elif opt in ("-l"):  # -l <path/filename to log file>
            parameters['log'] = arg

    return AgentAutograder(parameters)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
```


### Django Snippets

```
class Status(View):

    def get(self, request, *args, **kwargs):
        _status = StatusEntry.objects.values('jwrun')[0]
        saveit = StatusEntry(id=0, jwrun=False)
        saveit.save()
        return JsonResponse(_status)

class UserInput(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        _page_data = {
                        'question': request.session.get('nquestion', "Enter question then click Post to Piazza"),
                        'debugdata': request.session.get('ndebugdata', "")
                    }

        return render(request, 'indexform.html', _page_data)


    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        request.session['ndebugdata'] = ""

        # Read POST data
        username = request.user.username
        randomquestion = request.POST.get('randomquestion')
        posttopiazza = request.POST.get('posttopiazza')
        postalltopiazza = request.POST.get('postalltopiazza')
        runjw = request.POST.get('runjw')
        cleanpiazza = request.POST.get('cleanpiazza')

        if randomquestion is not None:
            request = self._button_randomquestion(request)

        .......

        return self.get(request, *args, **kwargs)


    def _button_randomquestion(self, request):
        # Database queries
        all_questions = Log.objects.values('question')
        request.session['nquestion'] = all_questions[random.randrange(len(all_questions))]['question']
        return request

    def _button_posttopiazza(self, request):
        userquestion = request.POST.get('userinput', None)
        if userquestion == "":
            request.session['ndebugdata'] = "Please enter a question"
            return request

        _questions = [a['question'] for a in Log.objects.values('question')]
        if userquestion not in _questions:
            logit = Log(question=userquestion)
            logit.save()

        .......

        request.session['ndebugdata'] = "Posting: "+userquestion
        return self._post_to_piazza(request, [userquestion])

    def _button_postalltopiazza(self, request):
        _questions = [a['question'] for a in Log.objects.values('question')]
        return self._post_to_piazza(request, _questions)

    def _button_runjw(self, request):
        _saveit = StatusEntry(id=0, jwrun=True)
        _saveit.save()
        return request

    def _post_to_piazza(self, request, questions):
        if not questions:
            request.session['ndebugdata'] = "Attempting blank post"
            return request

        ......

        request.session['ndebugdata'] = "Posting Questions:\n"
        for _question in questions:
            if _question == "":
                request.session['ndebugdata'] = "Attempting blank post"
                break

            post_type = 'question'
            post_folders = ['other']
            post_subject = _question
            post_content = _question

            request.session['ndebugdata'] += (_question+"\n")

            try:
                my_class.create_post(   post_type,      \
                                        post_folders,   \
                                        post_subject,   \
                                        post_content )
            except Exception as _err:
                request.session['ndebugdata'] += "Error posting: "+str(_err)+"\n"

        request.session['ndebugdata'] += "Posting successful: "+str(len(questions))
        return request
```

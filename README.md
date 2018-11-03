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

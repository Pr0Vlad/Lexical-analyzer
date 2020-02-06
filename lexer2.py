import re
import sys
from itertools import chain
class Reading:
    tokens = list()
    class Comment(object):
        def __init__(self):
            self._x = None
        @property
        def x(self):
            return self._x
        @x.setter
        def x(self, value):
            self._x = value
    def token(self, key, tokens):
        tokens.append((key, self))
    def tokenizer(self, token, tokens, comments):
        while self:
            self = self.strip()
            in_block = comments.x
            if in_block:
                while self:
                    if re.match('\\*/', self):
                        self = self[2:]
                        self = self.strip()
                        comments.x = False
                        break
                    else:
                        self = self[1:]
                        self = self.strip()
                        pass
            elif re.match('\\bint\\b|\\bwhile\\b|\\bvoid\\b|\\breturn\\b|\\belse\\b|\\bif\\b', self) and not in_block:
                key = re.match('int|while|void|return|else|if', self).group()
                token(key, 'KEYWORD:', tokens)
                self = self[len(key):]
                print('KEYWORD: ' + key)
                pass
            elif re.match('[a-zA-Z]+', self) and not in_block:
                key = re.match('[a-zA-Z]+', self).group()
                token(key, 'ID:', tokens)
                self = self[len(key):]
                print('ID: ' + key)
                pass
            elif re.match('[0-9]+', self) and not in_block:
                key = re.match('[0-9]+', self).group()
                token(key, 'NUM:', tokens)
                self = self[len(key):]
                print('NUM: ' + key)
                pass
            elif re.match('[^\\s0-9a-zA-Z]+', self) and not in_block:
                key = re.match('[^\\s0-9a-zA-Z]+', self).group()
                if key.startswith(';') and not in_block:
                    token(key, 'TERMINATOR:', tokens)
                    self = self[len(key):]
                    print('TERMINATOR: ' + key)
                elif re.match('//[\\s\\S]*?', self):
                    self = self[:0]
                elif re.match('/\\*[\\s\\S]*?\\*/', self) and not in_block:
                    comment = re.match('/\\*[\\s\\S]*?\\*/', self).group()
                    self = self[len(comment):]
                elif re.match('/\\*', self):
                    comments.x = True
                    break
                elif re.match('==|<=|>=|!=', key) and not in_block:
                    key = key[:2]
                    token(key, 'RELATION:', tokens)
                    self = self[len(key):]
                    print('RELATION: ' + key)
                elif re.match('[*]|/|[+]|=|-|<|>|,|[(]|[)]|[{]|[}]|\\]|\\[', key) and not in_block:
                    key = key[:1]
                    token(key, 'OPERATION:', tokens)
                    self = self[len(key):]
                    print('OPERATION: ' + key)
                    pass
                else:
                    key = re.match('[\\S]*', self).group()
                    key = key[:len(key)]
                    self = self[len(key):]
                    print('ERROR: ' + key)
                    pass
    def remove(self, token, tokenizer, tokens, comments):
        is_comment = False
        for line in self:
            if line.strip() != '':
                print('INPUT:' + line.strip())
            if line.startswith('/*') or is_comment:
                is_comment = True
                line = line[2:]
                line = line.strip()
                while line:
                    if line.startswith('*/'):
                        line = line[2:]
                        line = line.strip()
                        is_comment = False
                        break
                    else:
                        line = line[1:]
                        line = line.strip()
                        pass
            tokenizer(line.strip(), token, tokens, comments)
    comments = Comment()
    file_name = sys.argv[1]
    with open(file_name, 'r') as f:
        remove(f, token, tokenizer, tokens, comments)
#    print(*chain(tokens))

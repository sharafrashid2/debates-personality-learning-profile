import re
import os
import copy
import pandas as pd
from dateutil.parser import parse


class WhatsParser:
    def __init__(self, file_path):
        self._header = []
        self._messages = self._get_messages_from_file(file_path)

    def _get_absolute_file_path(self, file_path):
        '''Returns the absolute path for the target .txt file'''
        return os.path.abspath(file_path)

    def _get_messages_from_file(self, file_path):
        '''Iterates trough all messages inside .txt file and creates messages
        instances that are loaded inside self.messages. All the first lines
        inside the file that are not messanges are considered as headers.'''

        messages = []
        line_count = 0

        with open(file_path) as file:
            for line in file:
                if self._is_start_of_new_message(line) and line_count < 2:
                    line_count += 1
                elif self._is_start_of_new_message(line):
                    message = self._construct_message(line)
                    messages.append(message)
                elif any(messages):
                    messages[-1]['content'] += f' {line.strip()}'
                else:
                    self._header.append(line.strip())

        return messages

    def _construct_message(self, line):
        '''Removes data from each line inside the file and returns a Message'''
        datetime = self._get_datetime_from_line(line)
        author = self._get_author_from_line(line)
        content = self._get_content_from_line(line, author)
        return {'datetime': datetime, 'author': author, 'content': content}

    def to_dataframe(self):
        '''Converts the WhatsParser object into a pandas dataframe'''
        messages = [item for item in self._messages]
        return pd.DataFrame(messages)

    @staticmethod
    def _is_start_of_new_message(line):
        '''All lines starting with a datetime are considered the beginnig of
        a new messange'''
        if re.match(r'[0-9]+\/[0-9]+\/[0-9]+,\s[0-9]+:[0-9]+', line):
            return True
        return False

    @staticmethod
    def _get_datetime_from_line(line):
        '''Extracts datetime data from a line'''
        datetime = re.search(r'[0-9]+\/[0-9]+\/[0-9]+,\s[0-9]+:[0-9]+', line).group()
        return parse(datetime)

    @staticmethod
    def _get_author_from_line(line):
        '''Extracts author data from a line'''
        author = re.search(r'-\s(.*?): ', line).group()
        return author[2:-2]

    @staticmethod
    def _get_content_from_line(line, author):
        '''Extracts content data from a line'''
        start = re.search(author, line).span()[1]
        content = re.search(r'(?<=:\s).*$', line[start:]).group().strip()
        return content

    @property
    def authors(self):
        '''Returns an array listing all unique authors of all messages'''
        return list(set([msg['author'] for msg in self._messages]))

    @property
    def header(self):
        return self._header

    def __getitem__(self, position):
        '''Returns a dictionary with all message public properties'''
        return self._messages[position]

    def __setitem__(self, position, value):
        self._messages[position] = value

    def __iter__(self):
        '''Makes object iterable'''
        msgs = copy.deepcopy(self._messages)
        count = 0
        while count < len(msgs):
            yield msgs.pop(0)
            count += 1

    @property
    def data(self):
        return iter(self._messages)

    @data.setter
    def data(self, new_messages):
        self._messages = new_messages

    def __len__(self):
        '''Returns total number of messages'''
        return len(self._messages)

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import unicodedata

from tokenization_utils import _is_punctuation, _is_whitespace, _is_control, _is_chinese


# Common method.

# Converts the input text to unicode encoding if it is not already,
# assume the unicode encoding of input is utf-8.
def convert_to_unicode(text):
    if isinstance(text, str):
        return text
    elif isinstance(text, bytes):
        return text.decode("utf-8", "ignore")
    else:
        raise ValueError("Unsupported string type: %s" % (type(text)))


# Runs basic whitespace cleaning and splitting on a piece of text.
def whitespace_tokenize(text):
    text = text.strip()
    if not text:
        return []
    # Splits text into tokens according to whitespace, and the result excludes
    # the whitespace.
    tokens = text.split()
    return tokens


class BasicTokenizer(object):
    def __init__(self, do_lower_case=True):
        self.do_lower_case = do_lower_case

    # Tokenizes a piece of text.
    def tokenize(self, text):
        text = convert_to_unicode(text)
        text = self._clean_text(text)

        # This was added on November 1st, 2018 for the multilingual and Chinese
        # models. This is also applied to the English models now, but it doesn't
        # matter since the English models were not trained on any Chinese data
        # and generally don't have any Chinese data in them (there are Chinese
        # characters in the vocabulary because Wikipedia does have some Chinese
        # words in the English Wikipedia.).
        text = self._tokenize_chinese_chars(text)

        orig_tokens = whitespace_tokenize(text)
        split_tokens = []
        for token in orig_tokens:
            if self.do_lower_case:
                token = token.lower()
                token = self._run_strip_accents(token)
            split_tokens.extend(self._run_split_on_punc(token))

        output_tokens = whitespace_tokenize(" ".join(split_tokens))
        return output_tokens

    # Performs invalid character removal and whitespace cleanup on text.
    def _clean_text(self, text):
        output = []
        for char in text:
            # Gets a value of character, which is a hexadecimal or decimal number.
            # More information about unicode chart, please infer to
            # https://www.ssec.wisc.edu/~tomw/java/unicode.html.
            cp = ord(char)
            if cp == 0 or cp == 0xfffd or _is_control(char):
                continue
            if _is_whitespace(char):
                output.append(" ")
            else:
                output.append(char)
        return "".join(output)

    # Adds whitespace around any CJK character.
    def _tokenize_chinese_chars(self, text):
        output = []
        for char in text:
            if _is_chinese(char):
                output.append(" ")
                output.append(char)
                output.append(" ")
            else:
                output.append(char)
        return "".join(output)

    # Strips accents from a piece of text.
    def _run_strip_accents(self, text):
        text = unicodedata.normalize("NFD", text)
        output = []
        for char in text:
            cat = unicodedata.category(char)
            if cat == "Mn":
                continue
            output.append(char)
        return "".join(output)

    def _run_split_on_punc(self, text):
        chars = list(text)
        i = 0
        start_new_word = True
        output = []
        while i < len(chars):
            char = chars[i]
            if _is_punctuation(char):
                output.append([char])
                start_new_word = True
            else:
                if start_new_word:
                    output.append([])
                start_new_word = False
                output[-1].append(char)
            i += 1
        return ["".join(x) for x in output]

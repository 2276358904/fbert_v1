from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import tensorflow as tf

import tokenization


class TokenizationTest(tf.test.TestCase):
    def test_basic_tokenizer_lower(self):
        tokenizer = tokenization.BasicTokenizer(do_lower_case=True)

        self.assertAllEqual(
            tokenizer.tokenize(u" \tHeLLo!how  \n Are yoU?  "),
            ["hello", "!", "how", "are", "you", "?"])
        self.assertAllEqual(tokenizer.tokenize(u"H\u00E9llo"), ["hello"])


if __name__ == "__main__":
    tf.test.main()

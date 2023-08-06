#!/usr/bin/env python3

import collections
import regex as re

from somajo import doubly_linked_list
from somajo import token
from somajo import utils


class SentenceSplitter():
    def __init__(self, is_tuple=False, language="de_CMC"):
        """Create a SentenceSplitter object. If the tokenized paragraphs
        contain token classes or extra info, set is_tuple=True.

        """
        self.is_tuple = is_tuple
        # full stop, ellipsis, exclamation and question marks
        self.sentence_ending_punct = re.compile(r"^(?:\.+|…+\.*|[!?]+)$")
        self.opening_punct = re.compile(r"^(?:['\"¿¡\p{Pi}\p{Ps}–—]|-{2,})$")
        self.closing_punct = re.compile(r"^(?:['\"\p{Pf}\p{Pe}])$")
        # International quotes: «» “” ‹› ‘’
        # German quotes: »« „“ ›‹ ‚‘
        self.problematic_quotes = set(['"'])
        if language == "de" or language == "de_CMC":
            # German opening quotes [»›] have category Pf
            # German closing quotes [“‘«‹] have category Pi
            self.problematic_quotes = set(['"', "»", "«", "›", "‹", "“", "‘"])
        self.eos_abbreviations = utils.read_abbreviation_file("eos_abbreviations.txt")

    def _get_sentence_boundaries(self, tokens):
        sentence_boundaries = []
        n = len(tokens)
        for i, t in enumerate(tokens, start=1):
            if t.last_in_sentence:
                boundary = i
                for j in range(i, n):
                    if tokens[j].markup_class == "end":
                        boundary += 1
                    else:
                        break
                sentence_boundaries.append(boundary)
        if len(sentence_boundaries) == 0:
            sentence_boundaries.append(n)
        if sentence_boundaries[-1] != n:
            sentence_boundaries[-1] = n
        return sentence_boundaries

    def _add_xml_tags(self, tokens, s_tag="s"):
        """Mark sentence boundaries with XML tags."""
        # Positions of XML tags w.r.t. the actual sentence:
        start, inside, end, na = 1, 2, 3, 4
        open_tags = collections.deque()
        reopen_after_start = collections.deque()
        reopen_after_end = collections.deque()
        start_tag = re.compile(r"^<([^ ]+)[ ]?[^>]*>$")
        end_tag = re.compile(r"^</(.+)>$")
        for sentence in tokens:
            # print([(t.text, t.first_in_sentence, t.last_in_sentence) for t in sentence])
            sentence_dll = doubly_linked_list.DLL(sentence)
            position = start
            tags = collections.deque()
            first_token, last_token = None, None
            for tag in reversed(reopen_after_end):
                top = open_tags.pop()
                assert top is tag
            while len(reopen_after_end) > 0:
                tag = reopen_after_end.pop()
                sentence_dll.insert_left(tag["start_token"], sentence_dll.first)
            for tok in sentence_dll:
                if tok.value.markup:
                    # better store tag name in Token object
                    if tok.value.markup_class == "start":
                        m = start_tag.search(tok.value.text)
                        assert m
                        tag_name = m.group(1)
                        tag = {"tag_name": tag_name, "start_token": tok, "end_token": None, "start": position, "end": na}
                        open_tags.append(tag)
                        tags.append(tag)
                    elif tok.value.markup_class == "end":
                        m = end_tag.search(tok.value.text)
                        assert m
                        tag_name = m.group(1)
                        top = open_tags.pop()
                        assert tag_name == top["tag_name"]
                        top["end_token"] = tok
                        top["end"] = position
                        if top["start"] == na:
                            tags.appendleft(top)
                if tok.value.first_in_sentence:
                    position = inside
                    first_token = tok
                if tok.value.last_in_sentence:
                    position = end
                    last_token = tok
            if first_token is None:
                yield sentence_dll.to_list()
                continue
            s_start = first_token  # left of first token
            s_end = last_token     # right of last token
            lot = sentence_dll.last
            for tag in tags:
                # print(tag)
                if tag["start"] == na:
                    if tag["end"] == inside:
                        ft = sentence_dll.first
                        # close tag
                        closing_tag = token.Token("</%s>" % tag["tag_name"], markup=True, markup_class="end", markup_eos=False, locked=True)
                        sentence_dll.insert_left(closing_tag, ft)
                        # put starting s-tag to the right
                        assert sentence_dll.is_right_of(s_start, ft.prev)
                        # re-open tag
                        reopen_after_start.append(tag)
                elif tag["start"] == start:
                    if tag["end"] == inside:
                        # put starting s-tag to the left
                        if not sentence_dll.is_left_of(s_start, tag["start_token"]):
                            s_start = tag["start_token"]
                elif tag["start"] == inside:
                    if tag["end"] == end:
                        # put ending s-tag to the right
                        if not sentence_dll.is_right_of(s_end, tag["end_token"]):
                            s_end = tag["end_token"]
                    elif tag["end"] == na:
                        # close tag
                        closing_tag = token.Token("</%s>" % tag["tag_name"], markup=True, markup_class="end", markup_eos=False, locked=True)
                        sentence_dll.insert_right(closing_tag, lot)
                        # put ending s-tag
                        if not sentence_dll.is_right_of(s_end, lot.next):
                            # s_end = sentence_dll.last
                            s_end = lot.next
                        # re-open tag
                        reopen_after_end.append(tag)
            # starting s-tag
            sentence_dll.insert_left(token.Token("<%s>" % s_tag, markup=True, markup_class="start", markup_eos=True, locked=True), s_start)
            while len(reopen_after_start) > 0:
                tag = reopen_after_start.popleft()
                sentence_dll.insert_left(tag["start_token"], s_start)
            # ending s-tag
            sentence_dll.insert_right(token.Token("</%s>" % s_tag, markup=True, markup_class="end", markup_eos=True, locked=True), s_end)
            # for all tags on the stack, change start to na
            for tag in open_tags:
                tag["start"] = na
            yield sentence_dll.to_list()
        assert len(open_tags) == 0

    def _merge_empty_sentences(self, tokens):
        """Merge empty sentences with preceding sentence"""
        empty_first = True
        previous = []
        for sentence in tokens:
            empty_sentence = not any([tok.first_in_sentence for tok in sentence])
            if empty_first:
                previous.extend(sentence)
                empty_first = empty_sentence
            else:
                if empty_sentence:
                    previous.extend(sentence)
                else:
                    yield previous
                    previous = sentence
        yield previous

    def _split_sentences(self, tokens):
        """Split list of Token objects into sentences."""
        tokens, sentence_boundaries = self._split_token_objects(tokens)
        return [tokens[i:j] for i, j in zip([0] + sentence_boundaries[:-1], sentence_boundaries)]

    def split(self, tokenized_paragraph):
        """Split tokenized_paragraph into sentences."""
        if self.is_tuple:
            tokens = [token.Token(t[0]) for t in tokenized_paragraph]
        else:
            tokens = [token.Token(t) for t in tokenized_paragraph]
        tokens, sentence_boundaries = self._split_token_objects(tokens)
        return [tokenized_paragraph[i:j] for i, j in zip([0] + sentence_boundaries[:-1], sentence_boundaries)]

    def split_xml(self, tokenized_xml, eos_tags=set()):
        """Split tokenized XML into sentences."""
        opening_tag = re.compile(r"""<(?:[^\s:]+:)?([_A-Z][-.\w]*)(?:\s+[_:A-Z][-.:\w]*\s*=\s*(?:"[^"]*"|'[^']*'))*\s*/?>""", re.IGNORECASE)
        closing_tag = re.compile(r"^</([_:A-Z][-.:\w]*)\s*>$", re.IGNORECASE)
        if self.is_tuple:
            tokens = [token.Token(t[0]) for t in tokenized_xml]
        else:
            tokens = [token.Token(t) for t in tokenized_xml]
        first_token_in_sentence = True
        for i, t in enumerate(tokens):
            opening = opening_tag.search(t.text)
            closing = closing_tag.search(t.text)
            if opening:
                t.markup = True
                t.markup_class = "start"
                tagname = opening.group(1)
            if closing:
                t.markup = True
                t.markup_class = "end"
                tagname = closing.group(1)
            if t.markup:
                if tagname in eos_tags:
                    # previous non-markup is last_in_sentence
                    for j in range(i - 1, -1, -1):
                        if not tokens[j].markup:
                            tokens[j].last_in_sentence = True
                            break
                    # next non-markup is first_in_sentence
                    first_token_in_sentence = True
                continue
            if first_token_in_sentence:
                t.first_in_sentence = True
                first_token_in_sentence = False
        tokens, sentence_boundaries = self._split_token_objects(tokens)
        return [tokenized_xml[i:j] for i, j in zip([0] + sentence_boundaries[:-1], sentence_boundaries)]

    def _split_token_objects(self, tokens):
        n = len(tokens)
        # the first non-markup token is first_in_sentence
        for tok in tokens:
            if not tok.markup:
                tok.first_in_sentence = True
                break
        # the last non-markup token is last_in_sentence
        for tok in reversed(tokens):
            if not tok.markup:
                tok.last_in_sentence = True
                break
        for i, tok in enumerate(tokens):
            if tok.markup:
                continue
            if tok.last_in_sentence:
                continue
            if self.sentence_ending_punct.search(tok.text) or tok.text.lower() in self.eos_abbreviations:
                last = None
                last_token_in_sentence = tok
                first_token_in_sentence = None
                for j in range(i + 1, n):
                    tok_j = tokens[j]
                    if tok_j.markup:
                        continue
                    opening, closing = False, False
                    if first_token_in_sentence is None:
                        first_token_in_sentence = tok_j
                    # Heuristically disambiguate problematic quotes:
                    if tok_j.text in self.problematic_quotes:
                        # opening: preceded by space or opening
                        if tokens[j - 1].space_after or self.opening_punct.search(tokens[j - 1].text):
                            opening = True
                        # closing: last token or followed by space or closing
                        elif j == n - 1 or tok_j.space_after or self.closing_punct.search(tokens[j + 1].text):
                            closing = True
                    if tok_j.text[0].isupper() or tok_j.text.isnumeric():
                        last_token_in_sentence.last_in_sentence = True
                        first_token_in_sentence.first_in_sentence = True
                        break
                    elif opening or (self.opening_punct.search(tok_j.text) and not closing):
                        last = "opening"
                    elif closing or (self.closing_punct.search(tok_j.text) and not opening) and last != "opening":
                        last_token_in_sentence = tok_j
                        first_token_in_sentence = None
                        last = "closing"
                    else:
                        break
        sentence_boundaries = self._get_sentence_boundaries(tokens)
        return tokens, sentence_boundaries

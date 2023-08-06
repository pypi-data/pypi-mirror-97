
class TokenTrie:
    def __init__(self):
        self.root = dict()

    def add_token(self, text, token):
        """Associate a value with a string token."""
        current = self.root
        for l in text:
            current = current.setdefault(l, {})
        current['_t_'] = token

    def next_token(self, text):
        """Return either text and value of the next token or a string which matches no token."""
        if text[0] not in self.root:
            # initial letter not in trie, no match
            return text[0], None

        current = self.root
        for i in range(0, len(text)):
            if text[i] not in current:
                # match if prefix in trie
                return text[:i], current.get('_t_')
            current = current[text[i]]
        return text, current.get('_t_')


class TokenSet:
    def __init__(self):
        self.token_to_string = dict()
        self.string_to_token = TokenTrie()
        self.raw = False

    def add_tokens(self, tokens):
        # populate token trie
        for s, t in tokens:
            self.string_to_token.add_token(s, t)
        if self.raw:
            new_tokens = {t: s for s, t in tokens}
        else:
            new_tokens = {t: s.encode() for s, t in tokens}
        self.token_to_string.update(new_tokens)

    def tokenize(self, line, encoding):
        ret = bytearray()
        while line:
            match_text, token = self.string_to_token.next_token(line)
            if token is None:
                # no token, just encode text
                if self.raw:
                    ret += match_text.encode()
                else:
                    ret += match_text.encode(encoding)
            else:
                ret.append(token)
            line = line[len(match_text):]
        return ret

    def expand(self, line_encoded, encoding):
        ret = ''
        for b in line_encoded:
            if b in self.token_to_string:
                if self.raw or not self.token_to_string[b].isascii():
                    ret += self.token_to_string[b]
                else:
                    ret += self.token_to_string[b].decode(encoding)
            else:
                ret += bytes([b]).decode(encoding)
        return ret


_token_set_register = {}


def lookup(set_name):
    """Return the token set for a given name."""
    if set_name in _token_set_register:
        return _token_set_register[set_name]
    raise LookupError("unknown token set: "+set_name)


def token_set_names():
    return _token_set_register.keys()

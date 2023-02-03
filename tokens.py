class Token:
    def __init__(self, d_type: str, value: any = None, token_width: int = 1):
        self.type = d_type
        self.value = value
        self.width = token_width

    def __repr__(self):
        if not self.value:
            return "%s[%i]" % (self.type, self.width)
        return "%s:%s[%i]" % (self.type, self.value, self.width)

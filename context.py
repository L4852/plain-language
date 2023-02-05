class Context:
    def __init__(self, context_name, parent_context=None, context_change_line=None):
        self.context_name = context_name
        self.parent_context = parent_context
        self.change_line = context_change_line
        self.symbol_table = None
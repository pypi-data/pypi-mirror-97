import onetrick
@onetrick
def build(function):
    def convert():
        for part in function():
            yield str(part)

    return str.join('', convert())
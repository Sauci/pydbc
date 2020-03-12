class FormatException(Exception):
    def __init__(self, message, position, string=None):
        self.value = str(message) + str(position)
        if string:
            delta = 120
            s = position - delta if position >= delta else 0
            e = position + delta if len(string) >= position + delta else -1
            substring = string[s:e].replace('\r', ' ').replace('\n', ' ')
            indicator = ' ' * (delta if position >= delta else position) + '^'
            self.value += '\r\n\t' + ('...' if s else '   ') + substring + '\r\n\t   ' + indicator

        super(FormatException, self).__init__(self.value)

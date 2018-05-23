

class Tire(object):
    def __init__(self):
        self.type = 'tire'

    def forward(self):
        print('{} forward'.format(self.type))

    def backward(self):
        print('{} backward'.format(self.type))

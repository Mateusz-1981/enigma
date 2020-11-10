'''computer imitation of the enigma'''

import pickle as _pi

board = ()
key = ()

def read(pos, lis):
    '''reads a corresponding value form a list'''
    for w in range(len(lis)):
        if lis[w][0] == pos:
            return lis[w][1]
        elif lis[w][1] == pos:
            return lis[w][0]
    else:
        return pos

def transform(tupl):
    '''transforms a tuple rotor/board into a list rotor/board'''
    a = []
    for w in range(len(tupl)):
        a.append([tupl[w][0], tupl[w][1]])
    return a

def translate(text):
    '''translates numbers to letters and back using 'key'''
    if isinstance(text, str):
        text = list(text)
    for w in range(len(text)):
        text[w] = read(text[w], key)
    if isinstance(text[w], str):
        text = ''.join(text)
    return text

def boardset(table):
    global board
    board = table

def keyset(keys):
    global key
    key = keys


class Rotor:
    '''the rotor object used in enigma'''

    def __init__(self, *wheels):
        self.def_wheel = wheels
        self.wheel = []
        for w in range(len(wheels)):
            self.wheel.append(transform(wheels[w]))

    def move(self, rot: 'index of a rotor in wheel list', num):
        '''moves the rotor a 'num' amount of times'''
        for w in range(num):
            u = self.wheel[rot][-1][1]
            for i in range(len(self.wheel[rot])):
                u, self.wheel[rot][i][1] = self.wheel[rot][i][1], u

    def wheelset(self, wheel, pos):
        '''sets a wheel's position to a desired one'''
        while self.wheel[wheel] != transform(self.def_wheel[wheel]):
            self.move(wheel, 1)
        self.move(wheel, pos)

    def wheelpos(self, wheel):
        '''returns the position of a wheel'''
        temp = []
        for w in range(len(self.def_wheel[wheel])):
            if self.wheel[wheel] == transform(self.def_wheel[wheel]):
                x = w
                break
            self.move(wheel, 1)
        x = len(self.wheel[wheel]) - x
        if x == len(self.wheel[wheel]):
            return 0
        else:
            self.move(wheel, x)
            return x

    def revolve(self):
        '''turns the rotor one position'''
        for w in range(len(self.wheel) - 1):
            self.move(w, 1)
            if self.wheel[w] != transform(self.def_wheel[w]):
                break

    def change(self, pos, rot: 'index of a rotor in wheel list'):
        '''changes a value 'pos' from a rotor into a corresponding one'''
        for w in range(len(self.wheel[rot])):
            if self.wheel[rot][w][0] == pos:
                return self.wheel[rot][w][1]
            elif self.wheel[rot][w][1] == pos:
                return self.wheel[rot][w][0]
        else:
            raise ValueError("Invalid rotor or 'key'")

    def RENCODE(self, text):
        '''encodes a text like the enigma rotor did'''
        for i in range(len(text)):
            for w in range(len(self.wheel)):
                text[i] = self.change(text[i], w)
            for w in range(len(self.wheel) - 2, -1, -1):
                text[i] = self.change(text[i], w)
            self.revolve()
        return text


def ENCODE(text: list, rot):
    '''encodes a text in form of a number list using board and rotor'''
    for w in range(len(text)):
        text[w] = read(text[w], board)
    rot.RENCODE(text)
    for w in range(len(text)):
        text[w] = read(text[w], board)
    return text

def ENIGMA(text: str, rot):
    '''Uses all the elements to encode a 'str' text'''
    text = translate(text)
    text = ENCODE(text, rot)
    text = translate(text)
    return text


# file editing options
def load(file):
    '''reads objects written in a binary file and writes them onto a list'''
    con = {}
    with open(file, 'br') as f:
        while True:
            try:
                key = _pi.load(f)
                val = _pi.load(f)
                con[key] = val
            except EOFError:
                break
    return con

def _save(file, name, lis):
    '''appends an object to a specified binary file'''
    try:
        con = load(file)
    except FileNotFoundError:
        con = {}
    con[name] = lis
    with open(file, 'bw') as f:
        for key, w in con.items():
            _pi.dump(key, f)
            _pi.dump(w, f)

def save_params(file, key, board, *wheels):
    '''saves enigma key values in bunary as: 'key', 'board', 'r1', 'r2', ...'''
    with open(file, 'wb') as f:
        _pi.dump('key', f)
        _pi.dump(key, f)
        _pi.dump('board', f)
        _pi.dump(board, f)
        for w in range(len(wheels)):
            _pi.dump(f'r{w+1}', f)
            _pi.dump(wheels[w], f)



if __name__ == '__main__':
    print(''' ___ __  _ _  __ __ __  __   
| __|  \| | |/ _]  V  |/  \\  
| _|| | ' | | [/\ \_/ | /\ | 
|___|_|\__|_|\__/_| |_|_||_|\n''')
    k = load('def_params')
    boardset(k.pop('board'))
    keyset(k.pop('key'))
    s = [0, 0, 0]
    z = Rotor(k['r1'], k['r2'], k['r3'], k['r4'])
    del k
    while True:
        pr = input('>>> ')
        if pr == 'rot!':
            i = input('Enter rotor positions: ')
            i = i.split()
            for w in range(len(i)):
                z.wheelset(w, int(i[w]))
        elif pr == 'bor!':
            exec(f'i = {input("Enter board as tuple: ")}')
            boardset(i)
        elif pr == 'key!':
            print(key)
        else:
            for w in range(3):
                s[w] = z.wheelpos(w)
            try:
                en = ENIGMA(pr, z)
            except TypeError:
                print('Error: invalid text')
            else:
                print(f'Entry data: r1 = {s[0]}, r2 = {s[1]}, r3 = {s[2]}:')
                print(en)
        print('')

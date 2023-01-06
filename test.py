class sClass():
    phrase = "hello"

    def __enter__(q):
        print('enter')
    
    def __exit__(a, b, c, d):
        print('exit')

s = sClass()

with s:
    print(s.phrase)

w = 'hello'

with w:
    print(w)
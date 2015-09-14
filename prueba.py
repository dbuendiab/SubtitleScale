import locale

def guess_notepad_encoding(filepath, default_ansi_encoding=None):
    with open(filepath, 'rb') as f:
        data = f.read(3)
    if data[:2] in ('\xff\xfe', '\xfe\xff'):
        return 'utf-16'
    if data == u''.encode('utf-8-sig'):
        return 'utf-8-sig'
    # presumably "ANSI"
    return default_ansi_encoding or locale.getpreferredencoding()

if __name__ == "__main__":
    import sys, glob, codecs
    defenc = sys.argv[1]
    for fpath in glob.glob(sys.argv[2]):
        print()
        print((fpath, defenc))
        with open(fpath, 'rb') as f:
            print("raw:", repr(f.read())[:160])
        enc = guess_notepad_encoding(fpath, defenc)
        print("guessed encoding:", enc)
        with codecs.open(fpath, 'r', enc) as f:
            for lino, line in enumerate(f, 1):
                print(lino, repr(line))
                print(lino, repr(line.rstrip('\r\n')))
                if lino == 10:
                    break
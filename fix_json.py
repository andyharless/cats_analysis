import sys

def add_commas(s: str) -> str:
    """
    Turn a string containing an undelimited sequence of JSON objects
    into a string containing a proper JSON list of those objects
    """
    s = s.strip()
    n = len(s)
    sout = '['
    bracecount = 0
    comma = False
    for i, c in enumerate(s):
        sout += c
        if c == '{':
            bracecount += 1
            comma = False
        elif c == '}':
            bracecount -= 1
        if bracecount == 0:
            if i >= n-1:
                sout += ']\n'
            elif i and not comma:
            	sout += ','
            	comma = True
    return sout
    
    
if __name__ == '__main__':

    fn = sys.argv[1]
    if fn[-5:] != '.json':
        fn += '.json'

    with open(fn) as f:
      json_string = f.read()

    print(add_commas(json_string))

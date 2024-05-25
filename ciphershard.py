try:
    import os
    import getpass
    import secrets
    import sys
except ImportError:
    print('Critical Error: Required Modules Not found!\n')
    x = input('Press any key to continue...')
    sys.exit(1)

A = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'o', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')


# Function f(x) converts Alphanumeric characters to numbers of base 36    
def f(x):
  store = []
  for s in x:
    count = 0
    for i in range(36):
        if A[i].lower() == s.lower():
          store.append(i)
          count = 1
          break
    if count == 0:
      store.append(' ')
  return tuple(store)                

    
# Function rf(x) converts base 36 numbers to alphanumeric charactors.
def rf(x):
    store = []
    q = ''
    for s in x:
        try:
            store.append(A[s])
        except(IndexError, TypeError):
            store.append(' ')
    q = ''.join(store)
    return q
    
# Function ikey(x) generates a key.
def ikey(x):
    seed = list(range(36))
    masterkey = []
    for i in range(len(x)):
        masterkey.append(secrets.choice(seed))
    return tuple(masterkey)


# Function en(msg) encrypts a given string and returns ciphertxt and key as a tuple. 
def en(msg):
    ciphertxt = []
    x = f(msg)
    y = ikey(msg)
    for i in range(len(x)):
            if type(x[i]) is int:
                ciphertxt.append(((x[i]+y[i]) % 36))
            else:
                ciphertxt.append(' ')
    ctxt = rf(tuple(ciphertxt))
    shk = rf(y)
    return (ctxt, shk)


# Function de(c,k) decrypts a given encrypted string and returns a plaintxt as output.
def de(c, k):
    ciphertxt = []
    x = f(c)
    y = f(k)
    if len(x) <= len(y):
        for i in range(len(x)):
            if type(x[i]) is int and type(y[i]) is int:
                ciphertxt.append(((x[i]-y[i]) % 36))
            else:
                ciphertxt.append(' ')
    else:
        x = input('Incorrect Input!!!\nPress any key to continue...')
        sys.exit(1)
    return rf(tuple(ciphertxt))

    
# Function sprocess() is for secret splitting interface.
def sprocess():
    table = []
    print('''\n                **********************************************
                                Secret Splitting
                **********************************************''')
    while 1:
        try:
            x = int(input('\nEnter no. of shares you want to split the secret into(atmost 10,atleast 2):'))
            if 1 < x < 11:
                break
        except ValueError:
            print('\nPlease enter a valid integer greater than 1 but less than or equal to 10!\n')
    msg = getpass.getpass('Enter the secret:')
    table += list(en(msg))
    for i in range(2, x):
        tmp = table[-1]
        table.pop()
        table += list(en(tmp))
    for i in range(len(table)):
        print('SHARE', i+1, ':', table[i])


# Function cprocess() is for secret combining interface.
def cprocess():
    table = []
    print('''\n                **********************************************
                                Secret Combining
                **********************************************''')
    while 1:
        try:
            x = int(input('\nEnter no. of shares you want to combine to get the secret(atmost 10,atleast 2):'))
            if 1 < x < 11:
                break
        except ValueError:
                print('\nPlease enter a valid integer greater than 1 but less than or equal to 10!\n')
    for i in range(x):
            table.append(getpass.getpass(str('Enter Share '+str(i+1)+':')))
    for i in range(x-1):
            hook = []
            a, b = table[-2], table[-1]
            table.pop()
            table.pop()
            hook.append(de(a, b))
            table += hook
    print()
    print(''.join(table))
        
# function for main interface.    
def mm():
   print('''\n                **********************************************
                                CIPHER SHARD
                **********************************************''')
   print('\n Choose the desired options below:')
   print('\n1) Split a secret into codes.')
   print('2) Combine codes to recover secret.')
   cmd = input('\nEnter choice:')
   if cmd == '1':
       sprocess()
   elif cmd == '2':
       cprocess()
   else:
      print('\nplease enter 1 or 2 to select options or press ctrl + c to exit!')
      
while True:
    try:
        mm()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)

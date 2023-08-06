import re


## plots and strategy 
def convert(file):
    with open(file) as f:
        lines = f.readlines()
        filename = file.split('.')[0]
    
    for line in lines:
        if re.findall("^plot", line) or re.findall("strategy", line):
            x = line.split(' ')
            x.insert(0, '#')
            lines[lines.index(line)] = ' '.join(x)
            # print(' '.join(x))


    ## if -------------> fix for longer if statements
    for line in lines:
        # print(line)
        if re.findall("^if", line):
            x = line.split(' ')
            # print(x)
            if x[-1] != '\n':
                x[-1] = x[-1].strip('\n')
                x.append(':\n')
            else:
                x[-1] = ':\n'
            lines[lines.index(line)] = ' '.join(x)
            # print(' '.join(x))


    ## comments
    for line in lines:
        if line.startswith('//'):
            # print(line)
            x = line.split(' ')
            x.insert(0, '#')
            lines[lines.index(line)] = ' '.join(x)
            # print(' '.join(x))


    ## alerts ---> # print()?
    for line in lines:
        if re.findall("alert", line):
            # print(line)
            x = line.split('alert')
            x[0] = "print"
            x = ''.join(x)
            lines[lines.index(line)] = x


    ## boolean assignment
    for line in lines:
        bool = re.findall("true|false", line)
        expr = re.findall("==|=", line)
        if bool and not line.startswith('#'):
            # print(line)
            x = line.split(expr[0])
            x = [item.strip('\n') for item in x]
            for i in x:
                if bool[0] in i:
                    x[x.index(i)] = bool[0].capitalize()+'\n'
                    x.insert(x.index(bool[0].capitalize()+'\n'), expr[0])
            lines[lines.index(line)] = ''.join(x)


    ## operators
    for line in lines:
        if re.findall(":=", line):
            # print(line)
            x = line.split(':=')
            # print(x)
            x.insert(-1, '=')
            lines[lines.index(line)] = ' '.join(x)
            # print(' '.join(x))


    ## dynamic variable assignment (a = b>c)
    for line in lines:
        expr = re.findall("[<>]", line)
        if expr:
            string = re.split('=|{0}'.format(expr), line)
            variable = string[0]
            x1 = string[1]
            x2 = string[2].strip('\n')
            x3 = string[2]
            # print(line)
            string = '{0} = lambda {1},{2}: {1} {4} {3}'.format(variable, x1, x2, x3, expr[0])
            # print(string)
            lines[lines.index(line)] = string

    ## write to .py
    with open('{0}.py'.format(filename), 'w') as f:
        for line in lines:
            f.write(line)
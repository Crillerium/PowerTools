import os;
import sys;
if os.path.isfile(sys.argv[1]):
    f = open(sys.argv[1],'r');
    inner = f.read();
    f.close();
    print(inner);
elif sys.argv[1] == 'i':
    lines=[];
    lnum = 1;
    while True:
        try:
            lines.append(input(str(lnum)+'|'));
            lnum+=1;
        except:
            break;
    f = open(sys.argv[2],'w');
    f.write('\n'.join(lines));
    f.close();

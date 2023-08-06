
from switch import switch, bswitch

__all__ = ["test_switch", "test_bswitch", "test_if", "teoric"]

def _decore_name(name):
    n = name.center(40, "=").replace(name, " %s " % name)
    print("<%s>" % n)

def test_switch(day):
    _decore_name("switch")
    with switch(day) as case:
        if case(1):
            print("its monday")
            case.sbreak
        if case(2, sbreak=True):
            print("its thuesday")
        if case.check(lambda value: value == 3):
            print("its whensday")
            case.sbreak
        if case.match(r"4"):
            print("its thursday")
            case.sbreak
        if case(5):
            print("its friday")
        if case(6):
            print("its saturday")
            case.sbreak
        if case(7, 7.0): # you can use more of one cases
            print("its sunday")
        if case.default:
            print("this day no exists")
    with switch(10, comparator=lambda v, cases: \
            any(c > v for c in cases)) as case:
        if case(2):
            print(1)
        if case(12):
            print(2)
    

def test_bswitch(day):
    _decore_name("bswitch")
    
    with bswitch(day) as case:
        if case(1):
            print("its monday")
        if case(2):
            print("its thuesday")
        if case(3):
            print("its whensday")
        if case(4):
            print("its thursday")
        if case(5):
            print("its friday")
        if case(6):
            print("its saturday")
        if case(7):
            print("its sunday")
        if case.default:
            print("this day no exists")
        # if you use a case after a default
        # this raise a error!
        # example:
        #if case(8):
        #    print("el dia 8 no existe")



def test_if(day):
    _decore_name("if elif else")
    
    if day == 1:
        print("its monday")
    elif day == 2:
        print("its thuesday")
    elif day == 3:
        print("its whensday")
    elif day == 4:
        print("its thursday")
    elif day == 5:
        print("its friday")
    elif day == 6:
        print("its saturday")
    elif day == 7:
        print("its sunday")
    else:
        print("this day no exists")
    
    
teoric = """
switch 2:
    case 1:
        print("its monday")
        break
    case 2:
        print("its thuesday")
        break
    case 3:
        print("its whensday")
        break
    case 4:
        print("its thursday")
        break
    case 5:
        print("its friday")
        break
    case 6:
        print("its saturday")
        break
    case 7, 7.0:
        print("its sunday")
        break
    default:
        print("this day no exists")
"""

def main():
    #test_switch(2)
    #test_bswitch(3)
    #test_if(4)
    return

if __name__ == "__main__":
    exit(main())



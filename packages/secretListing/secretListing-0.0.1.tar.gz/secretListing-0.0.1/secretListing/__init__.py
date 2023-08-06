
''' 

'Secret module' was created to ease operations on python lists.




'''



def __secret__(index_pos ,a = list,b = list):
    ''' this function collects list elements of 'b' and inserts them
        into a specified by 'index_pos' to list 'a' and then prints them '''
    a.insert(index_pos, b)
    print(a)


def __pack__(list_name = list):
    ''' this function collect elements of given list and sorts them by
        their value, example: [1,3,6,4] >>> [1,3,4,6] and then prints them '''
    list_name.sort()
    print(list_name)

def __odd__(list_name = list):
    ''' this function check every item in the list and prints whether it is an
        odd number(num) or a normal one '''
    for odd_ones in list_name:
        if odd_ones % 2 != 0:
            print(f'odd num: {odd_ones}')
        if odd_ones % 2 == 0:
            print(print(f'normal num:{odd_ones}'))
        
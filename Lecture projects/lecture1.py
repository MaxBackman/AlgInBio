
#   Problem: search in list
#   Input: A list of n elements
#   Output: True, iff the query element is in the list, otherwise False

#   Worst-case analysis:
#   Up to n iterations => O(n) iterations, 40C units/iteration
#   =>(4+C)O(n) = O(n)

#   Average-case analysis:
#   Requires probability distributions of the input data
#   Often not available


def search(x, data):

    for elem in data:  # how many unit operations? in every iteration: O(1) ("ordo ett" or "ordo one") or C
        if elem == x:  # 1+1 units of time
            return True  # 1 unit of time
    else:
        return False  # 1 unit of time


a = [1,2,3,5]

search(5,a)


# k divides by 2 until termination
# n/2^k <= 1 <=>
# n <= 2^k <=>
# log(n) <= k <=>
# => O(log(n)) iterations

def binsearch(x,data):

    left = 0  # 1 basic operation
    right = len(data)-1  # 3 time units
    found = False  # 1 time unit

    while left <= right and not found:  # 3 and iterates over the while statement
        middle = (left+right)//2  # 3
        if data[middle] == x:  # 1+1+1
            found = True  # 1
        else:
            if x < data[middle]:  # 3
                right = middle-1  # 2 arithmetic and assignment
            else:
                left = middle+1  # 2

    return found  # 1

# Total: C*O(log(n)) = O(log(n))

# Selection sort

def selectionsort(a):

    for i in range(len(a))):

        j = a.index(min(a[i:]))
        # j = argmin(a[i:])  # returns the position

        swap(a,i,j)  # O(1)


def mergesort(a):

    if len(a) < 2:
        return a
    else:
        mid = len(a)//2
        half1 = mergesort(a[:mid])  # T_ms(n/2)
        half2 = mergesort(a[mid:])  # T_ms(n/2)
        return sorted(half1+half2)  # O(n)

# Want to know: time complexity T_ms(n)
# O(1), if n < 2
# 2T_ms(n/2)+C_3*n, otherwise
# look up "Master theorem"
# => T_ms(n) € O(n*log(n))







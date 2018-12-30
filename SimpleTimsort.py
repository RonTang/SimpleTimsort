import time
import random
"""
二分搜索用于插入排序寻找插入位置
"""
def binary_search(the_array, item, start, end):
    if start == end:
        if the_array[start] > item:
            return start
        else:
            return start + 1
    if start > end:
        return start

    mid = round((start + end)/ 2)

    if the_array[mid] < item:
        return binary_search(the_array, item, mid + 1, end)

    elif the_array[mid] > item:
        return binary_search(the_array, item, start, mid - 1)

    else:
        return mid

"""
插入排序用于生成mini run
"""
def insertion_sort(the_array):
   
    l = len(the_array)
    
    for index in range(1, l):
        value = the_array[index]
        pos = binary_search(the_array, value, 0, index - 1)
        the_array[pos+1:index+1] = the_array[pos:index]
        the_array[pos] = value
   
    return the_array
"""
归并，将两个有序的list合并成新的有序list
"""
def merge(left, right):
    
    if not left:
        return right
    if not right:
        return left
    l_len = len(left)
    r_len = len(right)
    result = [None]*(l_len+r_len)
    i, j, k= 0,0,0
    while i < l_len and j< r_len:
        if left[i] <= right[j]:
            result[k] = left[i]
            i+=1
        else:
            result[k] = right[j]
            j+=1
        k+=1
    while i<l_len:
        result[k]=left[i];
        k+=1
        i+=1
    while j<r_len:
        result[k]=right[j]
        k+=1
        j+=1
   
    return result
     
    

def timsort(the_array):
    runs = []
    length = len(the_array)
    new_run = [the_array[0]]
    new_run_reverse = False
    # 将the_array拆分成多了(递增或严格递减)list并将严格递减的list反转后存入runs。
    for i in range(1, length):
       
        if len(new_run) == 1:
            if the_array[i] < the_array[i-1]:
                new_run_reverse = True
            else:
                new_run_reverse = False
            new_run.append(the_array[i])
                
        elif new_run_reverse:
            if the_array[i] < the_array[i-1]:
                new_run.append(the_array[i])
            else:
                new_run.reverse()
                runs.append(new_run)
                #print(new_run)
                new_run=[]
                new_run.append(the_array[i])
        else:
            if the_array[i] >= the_array[i-1]:
                new_run.append(the_array[i])
            else:
                runs.append(new_run)
                #print(new_run)
                new_run=[]
                new_run.append(the_array[i])
       
        if i == length - 1:
            runs.append(new_run)
            #print(new_run)

    mini_run = 32
    sorted_runs=[]
    cur_run=[]
    # 对runs中的每一项list长度不足mini_run用插入排序进行扩充，存入sorted_runs
    for item in runs:
        if len(cur_run) > mini_run:
            sorted_runs.append(insertion_sort(cur_run))
            cur_run = item
        else:
            cur_run.extend(item)
      
    sorted_runs.append(insertion_sort(cur_run))
    
   
    # 依次将run压入栈中，若栈顶run X，Y，Z。
    # 违法了X>Y+Z 或 Y>Z 则Y与较小和合并，并再次放入栈中。
    # 依据这个法则，能够尽量使得大小相同的run合并，以提高性能。
    # Timsort是稳定排序故只有相邻的run才能归并。
    run_stack = []
    sorted_array = []
    
    for run in sorted_runs:
        run_stack.append(run)
        stop = False
        while len(run_stack) >= 3 and not stop:
            
            X = run_stack[len(run_stack)-1]
            Y = run_stack[len(run_stack)-2]
            Z = run_stack[len(run_stack)-3]
            if (not len(X)>len(Y)+len(Z)) or (not len(Y)>len(Z)):
                run_stack.pop()
                run_stack.pop()
                run_stack.pop()
                if len(X) < len(Z):
                    YX = merge(Y,X)
                    run_stack.append(Z)
                    run_stack.append(YX)
                else:
                    ZY = merge(Z,Y)
                    run_stack.append(ZY)
                    run_stack.append(X)
            else:
                stop =True
            
        
        
    #将剩余的run一一归并
    for run in run_stack:
        sorted_array = merge(sorted_array, run)
        

    #print(sorted_array)

data = []
for x in range(0,100):
    data.append(random.randint(0,10000))

start = time.process_time()
timsort(data)
end = time.process_time()
print(end-start)


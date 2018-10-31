def quick(lst):
	if(len(lst) <= 1):
		return lst
	pivot = lst[0]
	less = [i for i in lst[1:] if i<=pivot]
	great =[j for j in lst[1:] if j>pivot]
	return quick(less) + [pivot] + quick(great)

def max_product(lst):
	max_p = 1
	index = 0
	if(len(lst) == 1):
		max_p = lst[0]
	elif(len(lst) == 2):
		max_p = max(lst[0], lst[1])
	elif(len(lst) == 3):
		max_p = max(lst[0]*lst[2], lst[1])
	elif(len(lst) > 3):    	
		forward_1 = lst[0] * max_product(lst[2:])
		forward_2 = lst[1] * max_product(lst[3:])
		max_p = max(forward_1, forward_2)    		
	return max_p

print(max_product([10,3,1,9,2]))
print(max_product([10,3,1,9,2,4,5,1]))
print(max_product([3,4,1]))
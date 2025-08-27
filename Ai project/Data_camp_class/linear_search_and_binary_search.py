# Linear Search => complexity: O(n)

def linear_search(unordered_list, search_value):
    for index in range(len(unordered_list)):
        if unordered_list[index] == search_value:
            return True
        else:
            continue
    return False

unordered_list = [15, 2, 21, 3, 12, 7, 8]
print(linear_search(unordered_list, 8))
print(linear_search(unordered_list, 800))

# Binary Search => complexity: O(log n)

def binary_search(ordered_list, search_value):
    first = 0
    last = len(ordered_list) - 1

    while first <= last:
        middle = (first + last) // 2
        if ordered_list[middle] == search_value:
            return True
        elif search_value < ordered_list[middle]:
            last = middle - 1
        else:
            first = middle + 1
    return False
        
ordered_list = [15, 2, 21, 3, 12, 7, 8]
print(binary_search(ordered_list, 8))
print(binary_search(ordered_list, 800))


def binary_search_recursive(ordered_list, search_value):
  if len(ordered_list) == 0:
    return False
  else:
    middle = len(ordered_list)//2
    if search_value == ordered_list[middle]:
        return True
    elif search_value < ordered_list[middle]:
        return binary_search_recursive(ordered_list[:middle], search_value)
    else:
        return binary_search_recursive(ordered_list[:middle], search_value)

print(binary_search_recursive([1,5,8,9,15,20,70,72], 5))
print(binary_search_recursive([1,5,8,9,15,20,70,72], 50))
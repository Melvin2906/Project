def bubble_sort(my_list):
    length = len(my_list)

    for i in range(length - 1):
        for j in range(length - (i + 1)):
            if my_list[j] > my_list[j + 1]:
                my_list[j], my_list[j + 1] = my_list[j + 1], my_list[j]
    return my_list

my_list = [5, 1, 8, 2, 4, 10]
print(bubble_sort(my_list))

def bubble_sort_2(my_list):
    length = len(my_list)
    is_sorted = False

    while not is_sorted:
        is_sorted = True
        for i in range(length - 1):
            if my_list[i] > my_list[i + 1]:
                my_list[i], my_list[i + 1] = my_list[i + 1], my_list[i]
                is_sorted = False
        length -= 1
    return my_list

my_list = [5, 1, 8, 2, 4, 10]
print(bubble_sort_2(my_list))


# Bubble sort - complexity
   # * Worst case: O(n²)
   # * Best case - not improved version: E(n²)
   # * Best case - improved version: E(n)
   # * Average case: Z(n²)
# Doesn't perform well with highly unsorted large lists
# Perform well:
   # + Large sorted/almost sorted lists
   # + small list
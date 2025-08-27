def selection_sort(my_list):
    length = len(my_list)
    lowest = 0

    for i in range(length - 1):
        lowest = my_list[i]
        index = i
        for j in range(i + 1, length):
            if my_list[j] < lowest:
                index = j
                lowest = my_list[j]
        my_list[i], my_list[index] = my_list[index], my_list[i]
    return my_list

my_list = [5, 1, 8, 2, 4, 10]
print(selection_sort(my_list))

# Selection sort - complexity
   # * Worst case: O(n²)
   # * Best case: E(n²)
   # * Average case: Z(n²)

def insertion_sort(my_list):
    length = len(my_list)

    for i in range(1, length):
        number_to_order = my_list[i]
        j = i - 1
        while j >= 0 and number_to_order < my_list[j]:
            my_list[j + 1] = my_list[j]
            j -= 1
        my_list[j + 1] = number_to_order
    return my_list

my_list = [5, 1, 8, 2, 4, 10]
print(insertion_sort(my_list))

# Insertion sort - complexity
   # * Worst case: O(n²)
   # * Best case: E(n²)
   # * Average case: Z(n²)
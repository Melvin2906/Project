def partition(my_list, first_index, last_index):
    pivot = my_list[first_index]
    left_pointeur = first_index + 1
    right_pointeur = last_index
    while True:
        while my_list[left_pointeur] < pivot and left_pointeur < last_index:
            left_pointeur += 1
        while my_list[right_pointeur] > pivot and right_pointeur >= first_index:
            right_pointeur -= 1
        if left_pointeur >= right_pointeur:
            break
        my_list[left_pointeur], my_list[right_pointeur] = my_list[right_pointeur], my_list[left_pointeur]
    my_list[first_index], my_list[right_pointeur] = my_list[right_pointeur], my_list[first_index]
    return right_pointeur


def quicksort(my_list, first_index, last_index):
    if first_index < last_index:
        partion_index = partition(my_list, first_index, last_index)
        quicksort(my_list, first_index, partion_index)
        quicksort(my_list, partion_index + 1, last_index)


my_list = [5, 1, 8, 2, 4, 10]
quicksort(my_list, 0, len(my_list) - 1)
print(my_list)

# Quick sort - complexity
   # * Worst case: O(n^2)
   # * very efficient
   # * Best case: E(n log n)
   # * Average case: Z(n log n)
   # * Space complexity: O(n log n)
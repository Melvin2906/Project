def merge_sort(my_list):
    if len(my_list) > 1:
        mid = len(my_list) // 2
        left_part = my_list[:mid]
        right_part = my_list[mid:]
        merge_sort(left_part)
        merge_sort(right_part)

        l = r = k = 0
        while l < len(left_part) and r < len(right_part):
            if left_part[l] < right_part[r]:
                my_list[k] = left_part[l]
                l += 1
            else:
                my_list[k] = right_part[r]
                r += 1
            k += 1
        while l < len(left_part):
            my_list[k] = left_part[l]
            l += 1
            k += 1
        while r < len(right_part):
            my_list[k] = right_part[r]
            r += 1
            k += 1


my_list = [5, 1, 8, 2, 4, 10]
merge_sort(my_list)
print(my_list)

# Merge sort - complexity
   # * Worst case: O(n log n)
   # * Best case: E(n log n)
   # * Average case: Z(n log n)
   # * Space complexity: O(n)
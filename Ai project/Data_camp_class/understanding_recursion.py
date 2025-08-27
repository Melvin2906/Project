# Example of recursive function

def factorial(number):
    if number < 0:
        return -1
    elif number == 1 or number == 0:
        return 1
    else:
        return (number * factorial(number - 1))

print(factorial(5))

def fibonnanci(number):
    if number <= 0:
        return number
    else:
        return fibonnanci(number - 1) + fibonnanci(number - 2)

print(fibonnanci(6))

# Another version
cache = [None]*(100)
def fibonacci2(n): 
    if n <= 0:
        return n
    if not cache[n]:
        cache[n] = fibonacci2(n-1) + fibonacci2(n-2)
    
    return cache[n]
    
print(fibonacci2(6))


def hanoi(num_disks, from_rod, to_rod, aux_rod):
    if num_disks >= 0:
        #hanoi(num_disks, from_rod, aux_rod, to_rod)
        print("Moving disk", num_disks, "from rod", from_rod,"to rod",to_rod)
        num_disks -= 1
        hanoi(num_disks, aux_rod, to_rod, from_rod)   

num_disks = 4
source_rod = 'A'
auxiliar_rod = 'B'
target_rod = 'C'
hanoi(num_disks, source_rod, target_rod, auxiliar_rod)
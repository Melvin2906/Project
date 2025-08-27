# Python hash table's are called dictionary

# Empty dictionary
my_empty_dictionary = {}

# Dictionary with items
my_menu = {
    'lasagna': 14.75,
    'moussaka': 21.15,
    'sushi': 16.05
}

# Python dictionary - get
print(my_menu['lasagna']) # => 14.75
# print(my_menu['pasta']) # => error
print(my_menu.get('paella')) # => None

# Python dictionary - items, keys & values
# Get items and print them
print(my_menu.items())

# Get keys and print them
print(my_menu.keys())

# Cet value and print them
print(my_menu.values())

# Python dictionary - insert
my_menu['samosas'] = 13
print(my_menu.items())

# Python dictionary - modify
print(my_menu.get('sushi')) # => 16.05
my_menu['sushi'] = 20
print(my_menu.get('sushi')) # => 20

# Python dictionary - iterate
for key, value in my_menu.items():
    print(f"\nkey: {key}")
    print(f"value: {value}")
print()

for key in my_menu:
    print(key)
print()

for value in my_menu.values():
    print(value)
print()

# Python dictionary - remove
# remove one element (key and value)
del my_menu['sushi']
print(my_menu.items())

# Empty the dictionary
my_menu.clear()
print(my_menu.items())

# or to remove all
del my_menu

# Python dictionary - nested dictionaries
my_menu = {
  'sushi' : {
    'price' : 19.25,
    'best_served' : 'cold'
  },
  'paella' : {
    'price' : 15,
    'best_served' : 'hot'
  },
  'samosa' : {
    'price' : 14,
    'best_served' : 'hot'
  },
  'gazpacho' : {
    'price' : 8,
    'best_served' : 'cold'
  }
}

for dish, values in my_menu.items():
  print(f"{dish.title()} is best served {values['best_served']}.")
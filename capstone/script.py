from trie import Trie
from data import *
from welcome import *
from hashmap import HashMap
from linkedlist import LinkedList


def traverse_linked_list(linked_list):
    """
    Traverses linked list and returns all node values
    """

    results = []

    # edge case: check if linked list is None
    if linked_list is None:
        return []

    current_node = linked_list.get_head_node()
    results.append(current_node.get_value())

    # traverse through linked_list and gather results
    while current_node.get_next_node() is not None:
        next_node = current_node.get_next_node()
        results.append(next_node.get_value())
        current_node = next_node
    return results

def helper_retrieve_results(user_input, map):
    """
    Helper function that returns food type results in a list and deals with
    multi-letter input by the user
    """
    # initialize list of food types to return
    to_return = []
    if len(user_input) > 1:
        first_letter = user_input[:1]
        linked_list = map.retrieve(first_letter)
        results = traverse_linked_list(linked_list)

        # only return results that begin with the characters from user input
        for result in results:
            if result.startswith(user_input):
                to_return.append(result)
    elif len(user_input) == 1:
        linked_list = map.retrieve(user_input)
        to_return = traverse_linked_list(linked_list)
    return to_return


#Printing the Welcome Message
print_welcome()

#Write code to insert food types into a data structure here. The data is in data.py
# gather all first letters for food types
first_letters = [food_type[:1] for food_type in types]

# initialize hash map to map first letters to linked list of food types
letter_food_map = HashMap(len(first_letters))

# map first letter of food types to a linked list of food types
for food_type in types:
    if letter_food_map.retrieve(food_type[:1]) is None:
        letter_food_map.assign(food_type[:1], LinkedList(food_type))
    else:
        old_linked_list = letter_food_map.retrieve(food_type[:1])
        old_linked_list.insert_beginning(food_type)
        letter_food_map.assign(food_type[:1], old_linked_list)

## TEST CASE ##
#print(letter_food_map.retrieve('c').stringify_list())

#Write code to insert restaurant data into a data structure here. The data is in data.py

# will map food type to a linked list of restaurants with given type
type_restaurant_map = HashMap(len(types))

for restaurant in restaurant_data:
    type, name, price, rating, address = restaurant
    to_store = (name, price, rating, address)

    # initialize hash map to store each restaurant's data
    restaurant_data_map = HashMap(1)
    restaurant_data_map.assign(type, to_store)

    # add to linked list of restaurant data maps if it exists; otherwise create it
    if type_restaurant_map.retrieve(type) is None:
        type_restaurant_map.assign(type, LinkedList(to_store))
    else:
        old_linked_list = type_restaurant_map.retrieve(type)
        old_linked_list.insert_beginning(to_store)
        type_restaurant_map.assign(type, old_linked_list)

## TEST CASE ##
#print(type_restaurant_map.retrieve('german').stringify_list())

#Write code for user interaction here
while True:
    # initialize variables
    num_choices = None
    view_flag = None
    continue_flag = None

    user_input = str(input("\nWhat type of food would you like to eat?\nType the beginning of that food type and press enter to see if it's here.\n")).lower()

    # Search user input in food types data structure here
    choices = helper_retrieve_results(user_input, letter_food_map)
    num_choices = len(choices)

    # Restaurant results & user input to see restaurant data
    if num_choices > 1:
        print('\n\nWith those beginning letters, your choices are:\n{}'.format(choices))
        continue
    elif num_choices == 0:
        print('\n\nThere are no restaurants with your beginning letters!\n\n')
    else:
        view_flag = input("\n\nThe only option with those beginning letters is {}. Do you want to look at {} restaurants? Enter 'y' for yes and 'n' for no.\n".format(choices[0], choices[0])).lower()

    if view_flag == 'y':
        restaurant_type = choices[0]
        data = sorted(traverse_linked_list(type_restaurant_map.retrieve(restaurant_type)))
        print('\n\nThe {} Restaurants in SoHo are....\n\n'.format(restaurant_type))
        # display data
        for row in data:
            print('--------------------------\n\n')
            name, price, rating, address = row
            print('Name: {}\n'.format(name))
            print('Price: {}'.format(price))
            print('Rating: {}'.format(rating))
            print('Address: {}'.format(address))
            print('\n\n')

        # does the user want to search for more restaurants?
        continue_flag = input("Do you want to find other restaurants? Enter 'y' for yes and 'n' for no.\n").lower()
    elif view_flag == 'n':
        continue

    # check whether to continue prompt to user
    if continue_flag == 'n':
        break


    #After finding food type write code for retrieving restaurant data here

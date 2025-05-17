# def task_manager(*args):
#     print(f'Today I need to do {args}')

# task_manager('task1', 'task2', 'task3')

# def task_manager(*args):
#     if args:
#         for task in args:
#             print(f'Today I need to do {task}')
#     else:
#             print(f'Please pass a task as argument')

# task_manager('task1', 'task2', 'task3')

def party_planner(*args, **kwargs):
    if args:
        print('You need to buy: ')
        for arg in args:
            print(arg)
    else:
        print('there is no food to buy' )

    if kwargs:
        print('Party details: ')

        for key, value in kwargs.items():
            print(f' {key} : \n {value}')

party_planner('tequilla', 'tacos', place = 'Raanana', time = '19.40')
party_planner('tequilla', 'tacos')
party_planner(place = 'Raanana', time = '19.40')
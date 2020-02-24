import sys
import requests

auth_params = {
    'key': "",  #введите ваш key
    'token': "", #введите ваш token
}

base_url = "https://api.trello.com/1/{}"

board_id = "" #введите ваш id

###response = requests.get(base_url.format('boards/' + board_id), params=auth_params).json()
###print(response)

def create_column(column_name):
    return requests.post(base_url.format('list'), data={'name': column_name, 'idBoard': board_id, **auth_params}).json()

def column_check(column_name):
    column_id = None
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()  
    for column in column_data:  
        if column['name'] == column_name:  
            column_id = column['id']  
            return column_id

def read():
    #Получим данные всех колонок на доске:
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    #Выведем название каждой колонки и всех заданий, которые к ней относятся
    for column in column_data:
            #получим данные всех задач в колонке и перечислим все названия
            task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards',params=auth_params).json()
            print(column['name'] + " -({})".format(len(task_data)))
            if not task_data:
                print('\t' + 'Нет задач!')
                continue
            for task in task_data:
                print('\t' + task['name'] + '\t' + task['id'])

def create(name, column_name):
    column_id = column_check(column_name)
    if column_id is None:
        column_id = create_column(column_name)['id']  
            #Создадим задачу с имененем _name_ в найденной колонке
    requests.post(base_url.format('cards'), data={'name': name, 'idList': column_id, **auth_params})

def move(name, column_name):
    #Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    #Среди всех колонок нужно найти задачу по имени и получить её id
    task_id = None
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name']==name:
                task_id = task['id']
                break
        if task_id:
            break
 
    if column_id is None:  
        column_id = create_column(column_name)['id']  
        # И совершим перемещение:  
        requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column_id, **auth_params})

def get_task_duplicates(task_name):
    #Получаем данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    # Создаём список колонок с дублирующимися именами
    duplicate_tasks = []
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == task_name:
                duplicate_tasks.append(task)
    return duplicate_tasks

if __name__=="__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] =='create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] =='move':
        move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'create_column':
        create_column(sys.argv[2])
import sys
import requests

auth_params = {
    'key': "1af6001ac0e30c7ac17454900c294628",
    'token': "2b9accb0f672b8e7ec393a7bcd19404913116a415c42601a261e149e2850890a",
}

base_url = "https://api.trello.com/1/{}"

board_id = "d7jdsB4j"

def read():
    #Получим данные всех колонок на доске:
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    #Выведем название каждой колонки и всех заданий, которые к ней относятся
    for column in column_data:
            print(column['name'])
            #получим данные всех задач в колонке и перечислим все названия
            task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards',params=auth_params).json()
            if not task_data:
                print('\t' + 'Нет задач!')
                continue
            for task in task_data:
                print('\t' + task['name'])

def create(name, column_name):
    #Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    #Переберем данные обо всех колонках, пока не найдем ту колонку, которая нам нужна
    for column in column_data:
        if column['name'] == column_name:
            #Создадим задачу с имененем _name_ в найденной колонке
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            break

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
    #Переберём данные обо всех колонках, пока не найдем ту, в которую мы будем перемещать задачу
    for column in column_data:
        if column['name'] == column_name:
            #Выполним запрос к API для перемещния задачи в нужную колонку
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value':column['id'], **auth_params})
            break


if __name__=="__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] =='create':
        create(sys.arvg[2], sys.argv[3])
    elif sys.argv[1] =='move':
        move(sys.argv[2], sys.argv[3])
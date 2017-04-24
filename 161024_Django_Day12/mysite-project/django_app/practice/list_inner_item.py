response = {
    'items': [{'id': 'Item1'},{'id': 'Item2'},{'id': 'Item3'},{'id': 'Item4'}]
}
id_list = []
for item in response['items']:
    cur_id = item['id']
    id_list.append(cur_id)

print(id_list)

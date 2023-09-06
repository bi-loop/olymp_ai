import csv

def change(user_id, **user_data):
    # Update the value of a specific user in the database.csv file
    with open('database.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    user_found = False

    for row in rows:
        if row['user_id'] == user_id:
            user_found = True
            for key, value in user_data.items():
                if key == 'password':
                    row['password'] = value
                elif key == 'mail':
                    row['mail'] = value
                elif key == 'verified':
                    row['verified'] = value

    if not user_found:
        new_user = {'user_id': user_id, 'mail': user_data.get('mail', ''), 'password': user_data.get('password', ''),
                    'verified': user_data.get('verified', '')}
        rows.append(new_user)

    with open('database.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['user_id', 'mail', 'password', 'verified'])
        writer.writeheader()
        writer.writerows(rows) #hi

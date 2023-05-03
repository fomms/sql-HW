import psycopg2
from psycopg2.extensions import AsIs


conn = psycopg2.connect(database='test', user='postgres', password='')
cur = conn.cursor()


def delete():
    cur.execute("""
        DROP TABLE clientphone, client;
    """)
    return


def create_db():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS client(
        clientID SERIAL PRIMARY KEY,
        name VARCHAR(60) NOT NULL,
        surname VARCHAR(60) NOT NULL,
        email VARCHAR(60) NOT NULL UNIQUE
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clientphone(
        id SERIAL PRIMARY KEY,
        clientID INTEGER NOT NULL REFERENCES client(clientID) ON DELETE CASCADE,
        phone VARCHAR(16) UNIQUE
        ); 
    """)
    return conn.commit()


def add_client(name, surname, email):
    cur.execute("""
        INSERT INTO client(name, surname, email) VALUES (%s, %s, %s);
        """, (name, surname, email))
    return conn.commit()


def add_phone(client_id, phone):
    cur.execute("""
        INSERT INTO clientphone(clientID, phone) VALUES (%s, %s);
        """, (client_id, phone))
    return conn.commit()


def update_info(new, id, value, table):
    cur.execute("""
        UPDATE %s SET %s = %s WHERE clientID = %s;
        """, (AsIs(table), AsIs(value), new, id))
    return conn.commit()


def delete_phone(phone):
    cur.execute("""
        DELETE FROM clientphone WHERE phone = %s;
        """, (phone,))
    return conn.commit()


def delete_client(client_id):
    cur.execute("""
        DELETE FROM client WHERE clientID = %s;
        """, (client_id,))
    return conn.commit()


def find_client(values_type, values):
    cur.execute("""
            SELECT c.surname, c.email, c.name, cp.phone, c.clientID FROM client c 
            FULL JOIN clientphone cp ON c.clientid = cp.clientid
            WHERE c.%s = %s;
            """, (AsIs(values_type), values))
    info = cur.fetchone()
    if info is None:
        return print('Пользователь не найден')
    if info[3] is None:
        phone = 'Телефон не найден'
    else:
        phone = info[3]
    print(f'Фамилия: {info[0]}\nИмя: {info[2]}\nТелефон: {phone}\nEmail: {info[1]}')
    return


delete()
create_db()
add_client('Ivan', 'Fomin', 'fomms@')
add_client('Nikita', 'Mukhin', 'nik@')
add_client('Segrey', 'Egorov', 'ser@')
add_phone(1, '89034395312')
add_phone(2, '89034356761')
update_info('Igor', '1', 'name', 'client')
delete_phone('89034395312')
delete_client('1')
find_client('clientID', '2')


cur.close()
conn.close()

from mysql.connector import connect

sql = connect(
    host='127.0.0.1', port=3306, user='root', password='admin', database='museum_dates'
)

cursor = sql.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS dates('
               'id INT primary key auto_increment,'
               'title varchar(96), description TEXT, date varchar(96), image BLOB)')
sql.commit()


def get_dates():
    cursor.execute('select * from dates')
    result = cursor.fetchall()
    return result


def add_date(date, title, description):
    cursor.execute('insert into dates(title, description, date)'
                   ' values (%s, %s, %s)', (title, description, date))
    sql.commit()
    cursor.execute('select id from dates')
    result = cursor.fetchall()
    return result[-1][0]


def edit_date(date, title, description, id):
    cursor.execute('update dates set title=%s, description=%s, date=%s where id=%s',
                   (title, description, date, id))
    sql.commit()


def upload_img(img_url, date_id):
    cursor.execute('update dates set image=%s where id=%s', (img_url, date_id))
    sql.commit()


def check_uid(uid):
    cursor.execute('select UID from users where UID=%s', (uid,))
    result = cursor.fetchone()
    if result:
        return 0
    else:
        return 1

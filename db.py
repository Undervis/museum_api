from mysql.connector import connect

sql = connect(
    host='127.0.0.1', port=3306, user='api_user', password='password', database='museum'
)

cursor = sql.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS dates('
               'id INT primary key auto_increment,'
               'title varchar(96), description TEXT,'
               'day varchar(2), month varchar(2), year varchar(4), image BLOB)')
sql.commit()


def get_dates():
    cursor.execute('select * from dates order by year')
    result = cursor.fetchall()
    return result


def get_date(id):
    cursor.execute('select * from dates where id=%s', (id,))
    result = cursor.fetchall()
    return result[0]


def delete_date(id):
    cursor.execute('delete from dates where id=%s', (id,))
    sql.commit()


def add_date(day, month, year, title, description):
    cursor.execute('insert into dates(title, description, day, month, year)'
                   ' values (%s, %s, %s, %s, %s)', (title, description, day, month, year))
    sql.commit()
    cursor.execute('select id from dates')
    result = cursor.fetchall()
    return result[-1][0]


def edit_date(day, month, year, title, description, id):
    cursor.execute('update dates set title=%s, description=%s, day=%s, month=%s, year=%s where id=%s',
                   (title, description, day, month, year, id))
    sql.commit()


def upload_img(img_url, date_id):
    cursor.execute('update dates set image=%s where id=%s', (img_url, date_id))
    sql.commit()

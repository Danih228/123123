def initialize_db():
    conn = sqlite3.connect('internet_store.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS orders
                    (order_id INTEGER PRIMARY KEY,
                    customer_name TEXT,
                    customer_email TEXT,
                    product_id INTEGER,
                    product_name TEXT,
                    quantity INTEGER,
                    total_price REAL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS products
                    (product_id INTEGER PRIMARY KEY,
                    product_name TEXT,
                    price REAL,
                    stock INTEGER
                    )''')

    conn.commit()
    return conn, cursor

conn, cursor = initialize_db()

# Функционал для обработки заказов
def create_order(customer_name, customer_email, product_id, quantity):
    try:
        # Проверка на корректность email и количества
        if not isinstance(customer_email, str) or '@' not in customer_email:
            print('Неверный адрес электронной почты.')
            return
        if not isinstance(quantity, int) or quantity <= 0:
            print('Количество должно быть положительным целым числом.')
            return

        cursor.execute('SELECT * FROM products WHERE product_id = ?', (product_id,))
        product = cursor.fetchone()
        if product and product[3] >= quantity:  # Проверяем, есть ли достаточно товара на складе
            total_price = product[2] * quantity
            cursor.execute('INSERT INTO orders (customer_name, customer_email, product_id, product_name, quantity, total_price) VALUES (?, ?, ?, ?, ?, ?)', (customer_name, customer_email, product_id, product[1], quantity, total_price))
            conn.commit()
            print('Заказ успешно создан!')
        elif product:
            print('Недостаточно товара на складе!')
        else:
            print('Товар не найден!')
    except sqlite3.Error as e:
        print(f'Ошибка базы данных: {e}')

# Функционал для управления товарами
def add_product(product_name, price, stock):
    try:
        cursor.execute('INSERT INTO products (product_name, price, stock) VALUES (?, ?, ?)', (product_name, price, stock))
        conn.commit()
        print('Товар успешно добавлен!')
    except sqlite3.Error as e:
        print(f'Ошибка базы данных: {e}')

def update_product(product_id, price, stock):
    try:
        cursor.execute('UPDATE products SET price = ?, stock = ? WHERE product_id = ?', (price, stock, product_id))
        conn.commit()
        print('Информация о товаре успешно обновлена!')
    except sqlite3.Error as e:
        print(f'Ошибка базы данных: {e}')

# Интеграция с чат-ботами
def chatbot_response(message):
    message = message.lower()
    if 'сделать заказ' in message:
        try:
            product_name, quantity = message.split(":")[1].strip().split(",")
            quantity = int(quantity.strip())
            cursor.execute('SELECT product_id FROM products WHERE product_name = ?', (product_name.strip(),))
            product_id = cursor.fetchone()
            if product_id:
                create_order('Иван Иванов', 'ivan@example.com', product_id[0], quantity)
            else:
                return 'Товар не найден. Проверьте название товара.'
        except:
            return 'Неверный формат запроса. Пожалуйста, введите: "Сделать заказ: Название товара, Количество".'
    elif 'помощь' in message:
        help_customer()
    elif 'акция' in message:
        return 'У нас сейчас проходит акция на все товары! Поторопитесь сделать заказ!'
    else:
        return 'Здравствуйте! Чем могу помочь?'

# Помощь покупателям
def help_customer():
    print('Добро пожаловать в наш интернет магазин! Чтобы сделать заказ, отправьте сообщение в формате "Сделать заказ: Название товара, Количество". Для помощи по другим вопросам, напишите "Помощь"')

# Пример использования функций

# Пример добавления товара
add_product('Товар 1', 10.0, 10)
add_product('Товар 2', 50.0, 5)  №вфвыфывффффффффффффффффффффффффффффффффффффффффффффффффффффффффффффффффффффф
add_product('Товар 3', 20.0, 2)

# Пример создания заказа
# create_order('Иванов И.И.', 'ivanov@example.com', 1, 2)

# Закрытие соединения с базой данных
conn.close()

# Пример взаимодействия с ботом
while True:
    user_input = input("Введите сообщение: ")
    response = chatbot_response(user_input)
    print(response)

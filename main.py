import fdb

con = fdb.connect(dsn = '', user ='', password ='', role='')

# Получить курсор для выполнения SQL-запросов
cursor = con.cursor()

# Получить список таблиц в базе данных
cursor.execute("SELECT rdb$relation_name FROM rdb$relations WHERE rdb$view_blr IS NULL AND (rdb$system_flag IS NULL OR rdb$system_flag = 0)")

for table in cursor.fetchall():
    table_name = table[0]
    print(f"Таблица: {table_name}")

    # Получаем список всех индексов для текущей таблицы
    cursor.execute(f"select rdb$index_name, rdb$unique_flag, rdb$expression_source from rdb$indices where rdb$relation_name = '{table_name}'")

    has_id_or_name_index = False

    for index in cursor.fetchall():
        index_name, is_unique, expression_source = index

        if expression_source is not None:
            print(f"Индекс {index_name} в таблице {table_name}: {expression_source}")
            if "id" in expression_source or "name" in expression_source:
                has_id_or_name_index = True

    if has_id_or_name_index:
        print(f"В таблице {table_name} есть индекс на поле id или name")

    print("---------------")
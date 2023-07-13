import MySQLdb as db

USER_NAME = "root"
USER_PASSWORD = "12345678"
DATABASE_NAME = "week2teamwork"


def trans(value):  # 将字符串类型的值加上单引号，其他类型的值不进行任何修改。
    if isinstance(value, str):
        return "'" + value + "'"
    else:
        return value


def getTableNames() -> list:
    """获取所有表名"""
    conn = db.connect(
        host="localhost",
        port=3306,
        user=USER_NAME,
        password=USER_PASSWORD,
        db=DATABASE_NAME,
    )
    cur = conn.cursor()

    cur.execute("SHOW TABLES;")
    results = cur.fetchall()
    table_list = []
    for result in results:
        table_list.append(result[0])

    cur.close()
    conn.close()

    return table_list


def checkTableExist(tableName: str) -> bool:  # 判断表是否存在
    return tableName in getTableNames()


def getTableDesc(tableName: str) -> list:
    """获取给定表的各字段描述：Field(字段名)、Type(字段类型)、Null(是否可为空)、Key(PRI主键、外键(UNI单值、MUL多值))、Default(默认值)、Extra(附加信息：如自增)"""
    if not checkTableExist(tableName):
        print("未找到{}表".format(tableName))
        return []

    conn = db.connect(
        host="localhost",
        port=3306,
        user=USER_NAME,
        password=USER_PASSWORD,
        db=DATABASE_NAME,
    )
    cur = conn.cursor()

    cur.execute("DESC {};".format(tableName))
    results = cur.fetchall()
    desc_list = []
    for result in results:
        desc = {}
        desc["Field"] = result[0]
        desc["Type"] = result[1]
        desc["Null"] = result[2]
        desc["Key"] = result[3]
        desc["Default"] = result[4]
        desc["Extra"] = result[5]
        desc_list.append(desc)

    cur.close()
    conn.close()

    return desc_list


def getTableFields(tableName: str) -> list:
    """获取给定表的各字段名"""
    if not checkTableExist(tableName):
        print("未找到{}表".format(tableName))
        return []

    conn = db.connect(
        host="localhost",
        port=3306,
        user=USER_NAME,
        password=USER_PASSWORD,
        db=DATABASE_NAME,
    )
    cur = conn.cursor()

    cur.execute("DESC {};".format(tableName))
    results = cur.fetchall()
    field_list = []
    for result in results:
        field_list.append(result[0])

    cur.close()
    conn.close()

    return field_list


def checkFieldExist(tableName: str, field: list) -> bool:  # 判断属性列是否存在在某个表中
    return field in getTableFields(tableName)


def simpleQuery(tableName: str, fields: list, conditions: str = "") -> list:
    """查询给定表符合给定条件的记录的给定字段"""
    if not checkTableExist(tableName):
        print("未找到{}表".format(tableName))
        return []
    if len(fields) == 0:
        print("未指定查询属性")
        return []
    for field in fields:
        if not checkFieldExist(tableName, field):
            print("{}表中未找到{}属性".format(tableName, field))
            return []

    conn = db.connect(
        host="localhost",
        port=3306,
        user=USER_NAME,
        password=USER_PASSWORD,
        db=DATABASE_NAME,
    )
    cur = conn.cursor()

    query = "select " + fields[0]
    for idx in range(1, len(fields)):
        query += "," + fields[idx] + " "
    query += "from " + tableName
    if len(conditions) > 0:
        query += " where {}".format(conditions) + ";"
    cur.execute(query)
    results = cur.fetchall()
    record_list = []
    for result in results:
        record_list.append(dict(zip(fields, result)))

    cur.close()
    conn.close()

    return record_list


def simpleInsert(tableName: str, fields: list, values: list) -> int:
    """向给定表插入给定记录"""
    if not checkTableExist(tableName):
        print("未找到{}表".format(tableName))
        return 0
    if len(fields) == 0:
        print("未指定赋值属性")
        return 0
    if len(fields) != len(values):
        print("赋值属性数与数据数不一致")
        return 0
    for field in fields:
        if not checkFieldExist(tableName, field):
            print("{}表中未找到{}属性".format(tableName, field))
            return 0

    conn = db.connect(
        host="localhost",
        port=3306,
        user=USER_NAME,
        password=USER_PASSWORD,
        db=DATABASE_NAME,
    )
    cur = conn.cursor()

    insertion = "insert into " + tableName + " (" + fields[0]
    for idx in range(1, len(fields)):
        insertion += "," + fields[idx] + " "
    insertion += ") values ({}".format(trans(values[0]))
    for idx in range(1, len(values)):
        insertion += ",{}".format(trans(values[idx]))
    insertion += ");"
    row = cur.execute(insertion)

    cur.close()
    conn.commit()
    conn.close()
    return row


def simpleRemove(tableName: str, conditions: str = "") -> int:
    """从给定表删除符合条件的记录"""
    if not checkTableExist(tableName):
        print("未找到{}表".format(tableName))
        return 0

    conn = db.connect(
        host="localhost",
        port=3306,
        user=USER_NAME,
        password=USER_PASSWORD,
        db=DATABASE_NAME,
    )
    cur = conn.cursor()

    deletion = "delete from " + tableName + " where {}".format(conditions)
    row = cur.execute(deletion)

    cur.close()
    conn.commit()
    conn.close()
    return row


def simpleUpdate(
    tableName: str, fields: list, values: list, conditions: str = ""
) -> int:
    """更新给定表符合条件的对应字段值"""
    if not checkTableExist(tableName):
        print("未找到{}表".format(tableName))
        return 0
    if len(fields) == 0:
        print("未指定修改属性")
        return 0
    if len(fields) != len(values):
        print("修改属性数与数据数不一致")
        return 0
    for field in fields:
        if not checkFieldExist(tableName, field):
            print("{}表中未找到{}属性".format(tableName, field))
            return 0

    conn = db.connect(
        host="localhost",
        port=3306,
        user=USER_NAME,
        password=USER_PASSWORD,
        db=DATABASE_NAME,
    )
    cur = conn.cursor()

    update = "update " + tableName + " set " + fields[0] + "=" + trans(values[0])
    for i in range(1, len(fields)):
        update += "," + fields[i] + "=" + trans(values[i])
    update += " where " + conditions + ";"
    row = cur.execute(update)

    cur.close()
    conn.commit()
    conn.close()
    return row


# complexQuery能生成两张关联表的复杂查询，根据用户选定的两张表tableName1和tableName2、
# 两张表各自要查询的属性列表fields1和fields2、两张表连接属性列表fieldsjoin、给定的查询条件
# conditions返回对应的MySQL查询结果，首先检查数据库中是否存在对应的两张表，而后检查对应的属性
# 是否存在于对应的表中，若数据格式合法，则连接数据库生成对应的查询语句query而后发送到mysql执行
# 并整合查询结果以列表嵌套字典形式返回。在语句生成时，依次加入两表要查询的列名，而后添加两表，
# where后的条件语句由连接字段和给定的查询条件共同生成。
def complexQuery(
    tableName1: str,
    fields1: list,
    tableName2: str,
    fields2: list,
    fieldsjoin: list,
    conditions: str = "",
) -> list:
    """查询给定表符合给定条件的记录的给定字段"""
    if not checkTableExist(tableName1):
        print("未找到{}表".format(tableName1))
        return []
    if not checkTableExist(tableName2):
        print("未找到{}表".format(tableName2))
        return []
    if len(fields1) + len(fields2) == 0:
        print("未指定查询属性")
        return []
    for field in fields1:
        if not checkFieldExist(tableName1, field):
            print("{}表中未找到{}属性".format(tableName1, field))
            return []
    for field in fields2:
        if not checkFieldExist(tableName2, field):
            print("{}表中未找到{}属性".format(tableName2, field))
            return []
    for field in fieldsjoin:
        if not checkFieldExist(tableName1, field):
            print("{}表中未找到{}属性".format(tableName1, field))
            return []
        if not checkFieldExist(tableName2, field):
            print("{}表中未找到{}属性".format(tableName2, field))
            return []

    conn = db.connect(
        host="localhost",
        port=3306,
        user=USER_NAME,
        password=USER_PASSWORD,
        db=DATABASE_NAME,
    )
    cur = conn.cursor()

    query = "select "
    field_list = []
    for idx in range(0, len(fields1)):
        fields1[idx] = tableName1 + "." + fields1[idx]
        field_list.append(fields1[idx])
    for idx in range(0, len(fields2)):
        fields2[idx] = tableName2 + "." + fields2[idx]
        field_list.append(fields2[idx])
    query += ",".join(field_list) + " from " + tableName1 + "," + tableName2
    if (len(fieldsjoin) > 0) | (len(conditions) > 0):
        query += " where "
        condition_list = [" (" + conditions + ") "]
        for field in fieldsjoin:
            condition_list.append(
                " " + tableName1 + "." + field + "=" + tableName2 + "." + field + " "
            )
        query += " and ".join(condition_list)
    query += " ;"
    cur.execute(query)
    results = cur.fetchall()
    record_list = []
    for result in results:
        record_list.append(dict(zip(fields1 + fields2, result)))

    cur.close()
    conn.close()

    return record_list


def customSQL(sqlcommand: str):
    """用户自定义复杂查询"""
    conn = db.connect(
        host="localhost",
        port=3306,
        user="root",
        password="12345678",
        db="week2teamwork",
    )
    cur = conn.cursor()
    row = cur.execute(sqlcommand)
    results = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    formatted_results = []
    for row in results:
        result_dict = dict(zip(column_names, row))
        formatted_results.append(result_dict)
    conn.commit()
    cur.close()
    conn.close()

    return formatted_results


if __name__ == "__main__":
    print(getTableFields("rack"))
    # print('str {}'.format('str'))
    # print(simpleRemove('rack',"Rid='Rack004'"))
    # print(simpleUpdate("rack", ["容量"], ["20U"], "Rid='Rack001'"))
    # print(getTableDesc("application"))
    print(
        complexQuery(
            "user", ["Uid", "年龄"], "useof", ["Aid"], ["Uid"], "user.Uid='User001'"
        )
    )
    # print(customSQL("select 年龄 from user;"))
# 这里给出了一些测试案例，经测试均成功返回结果，但请注意这里需要正确连接数据库（密码输对，且mysql中有目标数据库）

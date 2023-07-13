from django.shortcuts import render, redirect
import MySQLdb as db
from django.contrib import messages


USER_NAME = "root"
USER_PASSWORD = "12345678"
DATABASE_NAME = "week2teamwork"


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
        charset="utf8mb4",
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


def getTableNames() -> list:
    """获取所有表名"""
    conn = db.connect(
        host="localhost",
        port=3306,
        user=USER_NAME,
        password=USER_PASSWORD,
        db=DATABASE_NAME,
        charset="utf8mb4",
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


def checkFieldExist(tableName: str, field: list) -> bool:
    return field in getTableFields(tableName)


def checkTableExist(tableName: str) -> bool:
    return tableName in getTableNames()


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
        charset="utf8mb4",
    )
    cur = conn.cursor()

    query = "select " + fields[0]
    for idx in range(1, len(fields)):
        query += "," + fields[idx] + " "
    query += " from " + tableName
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
        charset="utf8mb4",
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
                " "
                + tableName1
                + "."
                + fieldsjoin
                + "="
                + tableName2
                + "."
                + fieldsjoin
                + " "
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
        db=DATABASE_NAME,
        charset="utf8mb4",
    )
    cur = conn.cursor()

    row = cur.execute(sqlcommand)
    results = cur.fetchall()

    # 获取列名
    column_names = [desc[0] for desc in cur.description]

    # 将结果转为字典列表
    formatted_results = []
    for row in results:
        result_dict = dict(zip(column_names, row))
        formatted_results.append(result_dict)

    cur.close()
    conn.commit()
    conn.close()
    return formatted_results


def index(request):
    return render(request, "DataCenterManager\\index.html")


def result1(request):
    results = simpleQuery(
        "databaseserver", ["DBSid", "IP地址", "DBMS类型", "版本", "处理器类型", "内存容量"], ""
    )
    values = []
    for result in results:
        values.append(list(result.values()))
    return render(
        request,
        "DataCenterManager\\result.html",
        {"keys": results[0].keys(), "values": values},
    )


def result2(request):
    results = simpleQuery("useof", ["Uid"], "Aid = 'App005'")
    values = []
    for result in results:
        values.append(list(result.values()))
    return render(
        request,
        "DataCenterManager\\result.html",
        {"keys": results[0].keys(), "values": values},
    )


def result3(request):
    results = simpleQuery("loadbalancer", ["LBid", "负载分发算法"], "SSL加速 = '是'")
    values = []
    for result in results:
        values.append(list(result.values()))
    return render(
        request,
        "DataCenterManager\\result.html",
        {"keys": results[0].keys(), "values": values},
    )


def userSelection(request):
    users = [f"User{i:03}" for i in range(1, 21)]  # Generate User001 to User020
    return render(request, "DataCenterManager/user_selection.html", {"users": users})


def recommend(request):
    user = request.POST.get("user", "")  # Retrieve the selected user from the request
    results = customSQL(
        f"""
        SELECT Aid, 版本, 名称, 简述
        FROM application
        WHERE Aid IN (
            SELECT DISTINCT Aid
            FROM belong
            WHERE Cid IN (
                SELECT Cid
                FROM user
                NATURAL JOIN useof
                NATURAL JOIN belong
                NATURAL JOIN category
                WHERE Uid='{user}'
            )
            AND Aid NOT IN (
                SELECT DISTINCT Aid
                FROM useof
                WHERE Uid='{user}'
            )
        )
        ORDER BY Aid ASC
        """
    )
    values = [list(result.values()) for result in results]
    if not results:
        # 如果 results 为空，重定向到 user-selector 并设置消息
        messages.add_message(request, messages.WARNING, "无推荐！")
        return redirect("user_selection")

    return render(
        request,
        "DataCenterManager/result.html",
        {"keys": results[0].keys(), "values": values},
    )

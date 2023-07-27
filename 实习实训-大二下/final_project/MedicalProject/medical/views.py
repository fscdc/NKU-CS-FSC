from django.shortcuts import render, redirect
from django.http import JsonResponse
from py2neo import Graph, Node, Relationship, NodeMatcher
import json

from medical.query_process.fuzzy_guess import fuzzy_guess
from medical.query_process.que_by_IpSpM import solver_IpSpM
from medical.query_process.que_by_IpSpM_plus import solver_IpSpMPlus
from medical.query_process.que_by_symp_Naive import solver_naive
from medical.query_process.que_by_symp_VecSim import solver_vecsim

# 连接 Neo4j 数据库
graph = Graph("bolt: // localhost:7474", auth=("neo4j", "12345678"))


# 注册
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # 判断用户名是否存在于 User 节点
        if graph.nodes.match("User", username=username).first():
            return JsonResponse({"message": "Username already exists"}, status=400)

        # 创建一个新的 User 节点
        user = Node("User", username=username)
        graph.create(user)

        # 创建一个新的 Password 节点
        password_node = Node("Password", password=password)
        graph.create(password_node)

        # 建立 User 节点和 Password 节点之间的关系
        rel = Relationship(user, "HAS_PASSWORD", password_node)
        graph.create(rel)

        return redirect("../login")  # 注册成功后跳转到登录页面

    return render(request, "medical/register.html")


# 登录
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # 查找带有给定用户名的 User 节点
        user = graph.nodes.match("User", username=username).first()

        if user:
            # 获取与 User 节点关联的 Password 节点
            rel = graph.match((user,), r_type="HAS_PASSWORD").first()
            if rel != None and (rel.end_node["password"] == password):
                user_info = {"username": username}

                request.session["user_info"] = user_info

                return redirect("../homepage")
            else:
                return JsonResponse({"message": "Invalid credentials"}, status=401)
        else:
            return JsonResponse({"message": "Invalid credentials"}, status=401)

    return render(request, "medical/login.html")


def homepage(request):
    # 从会话中获取用户信息
    user_info = request.session.get("user_info", None)

    neo4j_data = search_random()

    # print(json.loads(neo4j_data)["data"])

    return render(
        request,
        "medical/homepage.html",
        {"user_info": user_info, "neo4j_data": neo4j_data},
    )


def instruction(request):
    user_info = request.session.get("user_info", None)

    return render(request, "medical/instruction.html", {"user_info": user_info})


def guess(request):
    user_info = request.session.get("user_info", None)
    if request.method == "POST":
        # 获取用户输入的消息
        data = json.loads(request.body)
        user_message = data.get("message")
        # 获取下拉菜单选项值
        output_number = data.get("output_number")
        # 在这里调用后端模型来获取回答，假设回答为response_message
        response_message = fuzzy_guess.get_guess_list(
            user_message, True, int(output_number)
        )

        # 返回 JSON 格式的回答
        return JsonResponse({"message": response_message})

    return render(request, "medical/guess.html", {"user_info": user_info})


def submicroscope(request, name):
    user_info = request.session.get("user_info", None)

    illness_dict, neo4j_data = search_one(name)

    # 列表转字符串
    治疗方式_str = "、".join(illness_dict["治疗方式"])
    检查项目_str = "、".join(illness_dict["检查项目"])
    并发症_str = "、".join(illness_dict["并发症"])
    症状_str = "、".join(illness_dict["症状"])
    常见药物_str = "、".join(illness_dict["常见药物"])
    推荐药物_str = "、".join(illness_dict["推荐药物"])
    推荐吃_str = "、".join(illness_dict["推荐吃"])
    忌吃_str = "、".join(illness_dict["忌吃"])
    宜吃_str = "、".join(illness_dict["宜吃"])
    就诊科室_str = "、".join(illness_dict["就诊科室"])

    text = (
        f"这是关于{illness_dict['病名']}的一些信息："
        f"它的患病比例{illness_dict['患病比例']}，主要通过{illness_dict['传染方式']}传播。"
        f"特别是{illness_dict['易感人群']}容易受到影响。"
        f"{ '不幸的是' if illness_dict['医保疾病'] == '否' else '幸运的是' }，"
        f"这{'是' if illness_dict['医保疾病'] == '是' else '不是'}医保疾病，"
        f"{ '但' if illness_dict['治愈率'] != '较高' else '而且' }治愈率也有{illness_dict['治愈率']}。"
        f"治疗通常需要{illness_dict['治疗周期']}，费用在{illness_dict['治疗费用']}的范围内。"
        f"治疗方式包括{治疗方式_str}，并且常常需要进行{检查项目_str}检查。"
        f"但要小心，可能会有{并发症_str}等症状。"
        f"在治疗过程中，您可能会遇到一些{症状_str}。"
        f"为了缓解症状，可以使用{常见药物_str}或者推荐的{推荐药物_str}。"
        f"同时，{宜吃_str}也是适合吃的，"
        f"另外，多喝水是推荐的，但要忌吃{忌吃_str}。"
        f"相反，可以吃一些{推荐吃_str}。"
        f"若出现问题，请尽快就诊于{就诊科室_str}。"
    )

    return render(
        request,
        "medical/submicroscope.html",
        {
            "user_info": user_info,
            "name": name,
            "summary": illness_dict["简介"],
            "cause": illness_dict["成因"],
            "prevent": illness_dict["预防措施"],
            "text": text,
            "neo4j_data": neo4j_data,
        },
    )


def microscope(request):
    user_info = request.session.get("user_info", None)
    if request.method == "POST":
        data = json.loads(request.body)
        disease = data.get("message")  # 获取病名
        # 在这里调用后端模型来获取回答，假设回答为response_message
        response_message = str(in_neo4j(disease))
        response_message = [response_message]
        print(response_message)
        # 返回 JSON 格式的回答
        return JsonResponse({"message": response_message})
    return render(
        request,
        "medical/microscope.html",
        {
            "user_info": user_info,
        },
    )


def inquiry(request):
    user_info = request.session.get("user_info", None)
    if request.method == "POST":
        data = json.loads(request.body)
        disease_message = data.get("disease")  # 获取病名
        medicine_message = data.get("drug")  # 获取药品
        symptom_message = data.get("symptom")  # 获取症状
        switch_message = data.get("switch")

        # 在这里调用后端模型来获取回答，假设回答为response_message
        if switch_message == "True":
            response_message = solver_IpSpM.select_by_all_info(
                disease_message, symptom_message, medicine_message
            )
        else:
            response_message = solver_IpSpMPlus.select_by_all_info(
                disease_message, symptom_message, medicine_message
            )
        # 返回 JSON 格式的回答
        response_message = [illness[0] for illness in response_message]
        return JsonResponse({"message": response_message})

    return render(request, "medical/inquiry.html", {"user_info": user_info})


def inquiryplus(request):
    user_info = request.session.get("user_info", None)
    if request.method == "POST":
        data = json.loads(request.body)
        symptom_message = data.get("message")  # 获取症状文本
        method = data.get("method")  # 获取症状
        # 在这里调用后端模型来获取回答，假设回答为response_message

        if method == "True":
            response_message = solver_naive.que_by_symp(symptom_message, 10)
        else:
            response_message = solver_vecsim.que_by_symp(symptom_message, 10)

        response_message = [illness[0] for illness in response_message]
        # 返回 JSON 格式的回答
        return JsonResponse({"message": response_message})

    return render(request, "medical/inquiryplus.html", {"user_info": user_info})


def user(request):
    user_info = request.session.get("user_info", None)
    if request.method == "POST":
        username = user_info["username"]
        password = request.POST.get("password")

        # 查找带有给定用户名的 User 节点
        user = graph.nodes.match("User", username=username).first()

        if user:
            # 获取与 User 节点关联第一个关系
            rel = graph.match((user,), r_type="HAS_PASSWORD").first()
            if rel != None and (rel.end_node["password"] == password):
                return JsonResponse(
                    {"message": "Same password,please retry"}, status=401
                )
            else:
                # 更新已有的密码节点
                rel.end_node["password"] = password
                graph.push(rel.end_node)
                return redirect("../login")
    return render(request, "medical/user.html", {"user_info": user_info})


def illustration(request):
    user_info = request.session.get("user_info", None)
    return render(request, "medical/illustration.html", {"user_info": user_info})


def search_random():
    # 初始化集合以存储唯一的节点和关系数据
    unique_nodes = set()
    unique_links = set()

    # 防止出现空的关系图
    while not (unique_nodes and unique_links):
        # 执行 Cypher 查询并获取结果
        query = "MATCH p = (a) –-> (b) WHERE rand() < 0.0002 RETURN p"
        result = graph.run(query)

        # 处理查询结果
        for record in result:
            p = record["p"]

            # 先检查关系是否包含 "HAS_PASSWORD"，若包含则跳过当前 record
            if any(type(rel).__name__ == "HAS_PASSWORD" for rel in p.relationships):
                # print("跳过")
                continue

            for rel in p.relationships:
                source = rel.start_node
                target = rel.end_node

                # 检查节点名称和标签是否都相同
                if source["name"] == target["name"] and list(source.labels) == list(
                    target.labels
                ):
                    continue

                name = type(rel).__name__
                # 将唯一的关系数据添加到集合
                unique_links.add(
                    (
                        source["name"],
                        list(source.labels)[0],
                        target["name"],
                        list(target.labels)[0],
                        name,
                    )
                )

                # 将唯一的节点数据添加到集合
                unique_nodes.add((source["name"], list(source.labels)[0]))
                unique_nodes.add((target["name"], list(target.labels)[0]))

    # 生成节点数据并添加id字段
    data = [
        {"id": idx, "name": node_name, "category": node_label}
        for idx, (node_name, node_label) in enumerate(unique_nodes)
    ]

    # 生成边数据并根据节点名称和标签查找对应节点的索引，将索引添加为 source 和 target 的值
    links = [
        {
            "id": idx,
            "source": [
                idx
                for idx, node in enumerate(data)
                if node["name"] == source and node["category"] == source_category
            ][0],
            "target": [
                idx
                for idx, node in enumerate(data)
                if node["name"] == target and node["category"] == target_category
            ][0],
            "name": name,
        }
        for idx, (source, source_category, target, target_category, name) in enumerate(
            unique_links
        )
    ]

    # 构造最终的数据字典
    neo4j_data = {"data": data, "links": links}

    # 使用 ensure_ascii=False 来处理中文字符
    neo4j_data = json.dumps(neo4j_data, ensure_ascii=False)
    return neo4j_data


def search_one(value):
    """获取距离名为 value 的疾病 路径为 1 的所有点"""
    # 定义 data 数组存储节点信息
    data = []

    # 定义 links 数组存储关系信息
    links = []

    # 查询节点及其相关的所有关系
    node = graph.run('MATCH p = (n:疾病{name: "' + value + '"}) --> (m) return p').data()

    # 如果节点存在，len(node) 的值为 1；不存在的话，len(node) 的值为 0
    if len(node):
        # 构造字典存放节点信息
        node_dict = {
            "id": "node_0",
            "name": value,
            "category": list(node[0]["p"].nodes[0].labels)[0],
        }
        data.append(node_dict)

        # 查询与该节点有关的节点，步长为 1，并返回这些节点
        nodes = graph.run(
            'MATCH (n:疾病{name:"' + value + '"})-->(m) RETURN m, ID(m) as node_id'
        ).data()

        # 处理节点信息
        for i, n in enumerate(nodes):
            # 取出节点信息中的 name 和 id
            name = n["m"]["name"]
            node_id = "node_" + str(n["node_id"])

            # ! 防止节点重复，非常关键
            if node_id not in [item["id"] for item in data]:
                # 构造字典存放单个节点信息
                node_dict = {
                    "id": node_id,
                    "name": name,
                    "category": list(n["m"].labels)[0],
                }
                # 将单个节点信息存储进 data 数组中
                data.append(node_dict)

        # 查询该节点所涉及的所有 relationship，步长为 1，并返回这些 relationship
        rels = graph.run(
            'MATCH (n:疾病{name:"' + value + '"})-[rel]->(m) return rel, ID(m) as target'
        ).data()

        # 处理 relationship
        for i, r in enumerate(rels):
            print(r["rel"].start_node)
            source_id = "node_0"
            target_id = "node_" + str(r["target"])
            name = str(type(r["rel"]).__name__)
            # 构造字典存放关系信息
            link_dict = {
                "id": f"link_{i}",
                "source": source_id,
                "target": target_id,
                "name": name,
            }
            links.append(link_dict)

        # 构造字典存储 data 和 links
        search_neo4j_data = {"data": data, "links": links}
        # 将 dict 转化为 json 格式
        search_neo4j_data = json.dumps(search_neo4j_data, ensure_ascii=False)
    else:
        raise Exception("查无此疾病")

    """获取疾病信息字典"""
    illness_info = {"病名": value}

    # 疾病属性
    matcher = NodeMatcher(graph)
    illness = matcher.match("疾病", name=value)
    if len(list(illness)) == 0:
        return illness_info
    else:
        illness = illness.first()

    illness_info["简介"] = illness["desc"]
    illness_info["患病比例"] = illness["get_prob"]
    illness_info["成因"] = illness["cause"]
    illness_info["预防措施"] = illness["prevent"]
    illness_info["传染方式"] = illness["get_way"]
    illness_info["易感人群"] = illness["easy_get"]
    illness_info["医保疾病"] = illness["insurance"]
    illness_info["治愈率"] = illness["cured_prob"]
    illness_info["治疗周期"] = illness["cure_time"]
    illness_info["治疗费用"] = illness["cost_money"]

    # 治疗方式
    cure_method_query = (
        "match (n:疾病)-[r:治疗]->(m:治疗方式) where n.name='{}' return m".format(value)
    )
    cure_method_list = []
    for cure_method_item in list(graph.run(cure_method_query)):
        cure_method_node = cure_method_item.get("m")
        cure_method_list.append(cure_method_node["name"])
    illness_info["治疗方式"] = cure_method_list

    # 检查项目
    check_query = "match (n:疾病)-[r:检查项目]->(m:检查) where n.name='{}' return m".format(
        value
    )
    check_list = []
    for check_item in list(graph.run(check_query)):
        check_node = check_item.get("m")
        check_list.append(check_node["name"])
    illness_info["检查项目"] = check_list

    # 并发症
    complication_query = (
        "match (n:疾病)-[r:并发症]->(m:疾病) where n.name='{}' return m".format(value)
    )
    complication_list = []
    for complication_item in list(graph.run(complication_query)):
        complication_node = complication_item.get("m")
        complication_list.append(complication_node["name"])
    illness_info["并发症"] = complication_list

    # 症状
    symptom_query = "match (n:疾病)-[r:病症]->(m:症状) where n.name='{}' return m".format(
        value
    )
    symptom_list = []
    for symptom_item in list(graph.run(symptom_query)):
        symptom_node = symptom_item.get("m")
        symptom_list.append(symptom_node["name"])
    illness_info["症状"] = symptom_list

    # 常见药物&治疗药物
    common_med_query = "match (n:疾病)-[r:常见药物]->(m) where n.name='{}' return m".format(
        value
    )
    common_med_list = []
    for common_med in list(graph.run(common_med_query)):
        common_med_list.append(common_med.get("m")["name"])
    illness_info["常见药物"] = common_med_list

    cure_med_query = "match (n:疾病)-[r:推荐药物]->(m) where n.name='{}' return m".format(
        value
    )
    cure_med_list = []
    for cure_med in list(graph.run(cure_med_query)):
        cure_med_list.append(cure_med.get("m")["name"])
    illness_info["推荐药物"] = cure_med_list

    # 推荐吃
    recommend_food_query = (
        "match (n:疾病)-[r:推荐吃]->(m) where n.name='{}' return m".format(value)
    )
    recommend_food_list = []
    for recommend_food in list(graph.run(recommend_food_query)):
        recommend_food_list.append(recommend_food.get("m")["name"])
    illness_info["推荐吃"] = recommend_food_list

    # 忌吃
    forbid_food_query = "match (n:疾病)-[r:忌吃]->(m) where n.name='{}' return m".format(
        value
    )
    forbid_food_list = []
    for forbid_food in list(graph.run(forbid_food_query)):
        forbid_food_list.append(forbid_food.get("m")["name"])
    illness_info["忌吃"] = forbid_food_list

    # 宜吃
    suitable_food_query = "match (n:疾病)-[r:宜吃]->(m) where n.name='{}' return m".format(
        value
    )
    suitable_food_list = []
    for suitable_food in list(graph.run(suitable_food_query)):
        suitable_food_list.append(suitable_food.get("m")["name"])
    illness_info["宜吃"] = suitable_food_list

    # 科室
    depart_query = "match (n:疾病)-[r:就诊科室]->(m) where n.name='{}' return m".format(value)
    depart_list = []
    for depart in list(graph.run(depart_query)):
        depart_list.append(depart.get("m")["name"])
    illness_info["就诊科室"] = depart_list

    return illness_info, search_neo4j_data


def in_neo4j(str):
    illness = NodeMatcher(graph).match("疾病", name=str)
    if len(list(illness)) == 0:
        return False
    else:
        return True

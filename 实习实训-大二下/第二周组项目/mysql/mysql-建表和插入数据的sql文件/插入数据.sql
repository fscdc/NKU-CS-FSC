INSERT INTO Rack (Rid, 名称, 位置, 容量) VALUES ('Rack001', '机架1', '机房A', '20U');
INSERT INTO Rack (Rid, 名称, 位置, 容量) VALUES ('Rack002', '机架2', '机房B', '10U');
INSERT INTO Rack (Rid, 名称, 位置, 容量) VALUES ('Rack003', '机架3', '机房C', '20U');
INSERT INTO Rack (Rid, 名称, 位置, 容量) VALUES ('Rack004', '机架4', '机房D', '25U');
INSERT INTO Rack (Rid, 名称, 位置, 容量) VALUES ('Rack005', '机架5', '机房E', '15U');


INSERT INTO LoadBalancer (LBid, 名称, IP地址, 端口, 负载分发算法, SSL加速, 会话保持, Rid) VALUES ('LB001', '负载均衡器1', '192.168.0.1', '8080', 'Round Robin', '是', '是', 'Rack001');
INSERT INTO LoadBalancer (LBid, 名称, IP地址, 端口, 负载分发算法, SSL加速, 会话保持, Rid) VALUES ('LB002', '负载均衡器2', '192.168.0.2', '80', 'Least Connections', '是', '否', 'Rack002');
INSERT INTO LoadBalancer (LBid, 名称, IP地址, 端口, 负载分发算法, SSL加速, 会话保持, Rid) VALUES ('LB003', '负载均衡器3', '192.168.0.3', '443', 'IP Hash', '否', '是', 'Rack001');
INSERT INTO LoadBalancer (LBid, 名称, IP地址, 端口, 负载分发算法, SSL加速, 会话保持, Rid) VALUES ('LB004', '负载均衡器4', '192.168.0.4', '8000', 'Least Connections', '是', '否', 'Rack003');
INSERT INTO LoadBalancer (LBid, 名称, IP地址, 端口, 负载分发算法, SSL加速, 会话保持, Rid) VALUES ('LB005', '负载均衡器5', '192.168.0.5', '8080', 'Round Robin', '否', '是', 'Rack002');
INSERT INTO LoadBalancer (LBid, 名称, IP地址, 端口, 负载分发算法, SSL加速, 会话保持, Rid) VALUES ('LB006', '负载均衡器6', '192.168.0.6', '80', 'Least Connections', '是', '否', 'Rack004');
INSERT INTO LoadBalancer (LBid, 名称, IP地址, 端口, 负载分发算法, SSL加速, 会话保持, Rid) VALUES ('LB007', '负载均衡器7', '192.168.0.7', '443', 'IP Hash', '否', '是', 'Rack005');
INSERT INTO LoadBalancer (LBid, 名称, IP地址, 端口, 负载分发算法, SSL加速, 会话保持, Rid) VALUES ('LB008', '负载均衡器8', '192.168.0.8', '8000', 'Least Connections', '是', '否', 'Rack004');

INSERT INTO Server (Sid, 名称, IP地址, 操作系统, 处理器类型, 内存容量, Rid) VALUES ('S001', '服务器1', '192.168.0.2', 'Windows', 'AMD', '16GB', 'Rack005');
INSERT INTO Server (Sid, 名称, IP地址, 操作系统, 处理器类型, 内存容量, Rid) VALUES ('S002', '服务器2', '192.168.0.3', 'Linux', 'AMD', '128GB', 'Rack002');
INSERT INTO Server (Sid, 名称, IP地址, 操作系统, 处理器类型, 内存容量, Rid) VALUES ('S003', '服务器3', '192.168.0.4', 'Windows', 'Intel', '64GB', 'Rack003');
INSERT INTO Server (Sid, 名称, IP地址, 操作系统, 处理器类型, 内存容量, Rid) VALUES ('S004', '服务器4', '192.168.0.5', 'Linux', 'Intel', '128GB', 'Rack001');
INSERT INTO Server (Sid, 名称, IP地址, 操作系统, 处理器类型, 内存容量, Rid) VALUES ('S005', '服务器5', '192.168.0.6', 'Windows', 'Intel', '32GB', 'Rack002');
INSERT INTO Server (Sid, 名称, IP地址, 操作系统, 处理器类型, 内存容量, Rid) VALUES ('S006', '服务器6', '192.168.0.7', 'Linux', 'AMD', '64GB', 'Rack003');
INSERT INTO Server (Sid, 名称, IP地址, 操作系统, 处理器类型, 内存容量, Rid) VALUES ('S007', '服务器7', '192.168.0.8', 'Windows', 'AMD', '128GB', 'Rack001');
INSERT INTO Server (Sid, 名称, IP地址, 操作系统, 处理器类型, 内存容量, Rid) VALUES ('S008', '服务器8', '192.168.0.9', 'Linux', 'AMD', '256GB', 'Rack004');


INSERT INTO VirtualMachine (VMid, 名称, 版本, 访问控制, 认证配置, 容错设置, Sid) VALUES ('VM001', '虚拟机1', '1.0', '允许', '启用', '关闭', 'S001');
INSERT INTO VirtualMachine (VMid, 名称, 版本, 访问控制, 认证配置, 容错设置, Sid) VALUES ('VM002', '虚拟机2', '1.1', '允许', '禁用', '开启', 'S002');
INSERT INTO VirtualMachine (VMid, 名称, 版本, 访问控制, 认证配置, 容错设置, Sid) VALUES ('VM003', '虚拟机3', '2.0', '禁止', '启用', '关闭', 'S003');
INSERT INTO VirtualMachine (VMid, 名称, 版本, 访问控制, 认证配置, 容错设置, Sid) VALUES ('VM004', '虚拟机4', '1.2', '允许', '禁用', '开启', 'S004');
INSERT INTO VirtualMachine (VMid, 名称, 版本, 访问控制, 认证配置, 容错设置, Sid) VALUES ('VM005', '虚拟机5', '2.1', '禁止', '启用', '关闭', 'S005');
INSERT INTO VirtualMachine (VMid, 名称, 版本, 访问控制, 认证配置, 容错设置, Sid) VALUES ('VM006', '虚拟机6', '1.3', '允许', '禁用', '开启', 'S006');
INSERT INTO VirtualMachine (VMid, 名称, 版本, 访问控制, 认证配置, 容错设置, Sid) VALUES ('VM007', '虚拟机7', '2.2', '禁止', '启用', '关闭', 'S007');
INSERT INTO VirtualMachine (VMid, 名称, 版本, 访问控制, 认证配置, 容错设置, Sid) VALUES ('VM008', '虚拟机8', '1.4', '允许', '禁用', '开启', 'S008');
INSERT INTO VirtualMachine (VMid, 名称, 版本, 访问控制, 认证配置, 容错设置, Sid) VALUES ('VM009', '虚拟机9', '2.3', '禁止', '启用', '关闭', 'S004');
INSERT INTO VirtualMachine (VMid, 名称, 版本, 访问控制, 认证配置, 容错设置, Sid) VALUES ('VM010', '虚拟机10', '1.5', '允许', '禁用', '开启', 'S002');



INSERT INTO DatabaseServer (DBSid, 名称, IP地址, DBMS类型, 版本, 处理器类型, 内存容量) VALUES ('DBS001', '数据库服务器1', '192.168.0.3', 'MySQL', '8.0', 'Intel', '32GB');
INSERT INTO DatabaseServer (DBSid, 名称, IP地址, DBMS类型, 版本, 处理器类型, 内存容量) VALUES ('DBS002', '数据库服务器2', '192.168.0.4', 'Oracle', '12c', 'AMD', '64GB');
INSERT INTO DatabaseServer (DBSid, 名称, IP地址, DBMS类型, 版本, 处理器类型, 内存容量) VALUES ('DBS003', '数据库服务器3', '192.168.0.5', 'SQL Server', '2019', 'Intel', '128GB');

INSERT INTO Application (Aid, 名称, 版本, 开发者, 简述, 占用空间大小, DBSid) VALUES ('App001', '应用程序1', '2.0', '开发者A', '这是一个应用程序', '100MB', 'DBS001');
INSERT INTO Application (Aid, 名称, 版本, 开发者, 简述, 占用空间大小, DBSid) VALUES ('App002', '应用程序2', '2.1', '开发者B', '好玩不氪', '150MB', 'DBS002');
INSERT INTO Application (Aid, 名称, 版本, 开发者, 简述, 占用空间大小, DBSid) VALUES ('App003', '应用程序3', '3.0', '开发者C', '这是第三个应用程序', '200MB', 'DBS003');
INSERT INTO Application (Aid, 名称, 版本, 开发者, 简述, 占用空间大小, DBSid) VALUES ('App004', '应用程序4', '1.0', '开发者D', '这是另一个新应用程序', '120MB', 'DBS001');
INSERT INTO Application (Aid, 名称, 版本, 开发者, 简述, 占用空间大小, DBSid) VALUES ('App005', '应用程序5', '2.2', '开发者E', '这是另一个测试应用程序', '180MB', 'DBS002');
INSERT INTO Application (Aid, 名称, 版本, 开发者, 简述, 占用空间大小, DBSid) VALUES ('App006', '应用程序6', '3.1', '开发者F', '不好玩骗氪', '250MB', 'DBS003');
INSERT INTO Application (Aid, 名称, 版本, 开发者, 简述, 占用空间大小, DBSid) VALUES ('App007', '应用程序7', '1.1', '开发者G', '这是一个新的测试应用程序', '140MB', 'DBS001');
INSERT INTO Application (Aid, 名称, 版本, 开发者, 简述, 占用空间大小, DBSid) VALUES ('App008', '应用程序8', '2.3', '开发者H', '这是第八个应用程序', '190MB', 'DBS002');
INSERT INTO Application (Aid, 名称, 版本, 开发者, 简述, 占用空间大小, DBSid) VALUES ('App009', '应用程序9', '3.2', '开发者I', '这是另一个新测试应用程序', '260MB', 'DBS003');
INSERT INTO Application (Aid, 名称, 版本, 开发者, 简述, 占用空间大小, DBSid) VALUES ('App010', '应用程序10', '1.2', '开发者J', '这是第十个应用程序', '130MB', 'DBS001');
INSERT INTO Application (Aid, 名称, 版本, 开发者, 简述, 占用空间大小, DBSid) VALUES ('App011', '应用程序11', '2.4', '开发者K', '这是一个新的测试应用程序', '170MB', 'DBS002');
INSERT INTO Application (Aid, 名称, 版本, 开发者, 简述, 占用空间大小, DBSid) VALUES ('App012', '应用程序12', '3.3', '开发者L', '飞车', '230MB', 'DBS003');



INSERT INTO runon (Aid, VMid) VALUES ('App002', 'VM002');
INSERT INTO runon (Aid, VMid) VALUES ('App003', 'VM006');
INSERT INTO runon (Aid, VMid) VALUES ('App004', 'VM004');
INSERT INTO runon (Aid, VMid) VALUES ('App005', 'VM010');
INSERT INTO runon (Aid, VMid) VALUES ('App006', 'VM006');
INSERT INTO runon (Aid, VMid) VALUES ('App007', 'VM005');
INSERT INTO runon (Aid, VMid) VALUES ('App008', 'VM008');
INSERT INTO runon (Aid, VMid) VALUES ('App009', 'VM009');
INSERT INTO runon (Aid, VMid) VALUES ('App010', 'VM010');
INSERT INTO runon (Aid, VMid) VALUES ('App011', 'VM001');
INSERT INTO runon (Aid, VMid) VALUES ('App012', 'VM002');
INSERT INTO runon (Aid, VMid) VALUES ('App001', 'VM004');
INSERT INTO runon (Aid, VMid) VALUES ('App001', 'VM003');



INSERT INTO Category (Cid, 名称, 说明) VALUES ('C001', '动作', '动作游戏');
INSERT INTO Category (Cid, 名称, 说明) VALUES ('C002', '冒险', '冒险类游戏');
INSERT INTO Category (Cid, 名称, 说明) VALUES ('C003', '策略', '策略游戏，运用头脑');
INSERT INTO Category (Cid, 名称, 说明) VALUES ('C004', '模拟', '模拟类型游戏');
INSERT INTO Category (Cid, 名称, 说明) VALUES ('C005', '恐怖', '胆小勿进');

INSERT INTO Belong (Aid, Cid) VALUES ('App001', 'C001');
INSERT INTO Belong (Aid, Cid) VALUES ('App002', 'C002');
INSERT INTO Belong (Aid, Cid) VALUES ('App003', 'C003');
INSERT INTO Belong (Aid, Cid) VALUES ('App004', 'C004');
INSERT INTO Belong (Aid, Cid) VALUES ('App005', 'C003');
INSERT INTO Belong (Aid, Cid) VALUES ('App006', 'C001');
INSERT INTO Belong (Aid, Cid) VALUES ('App007', 'C002');
INSERT INTO Belong (Aid, Cid) VALUES ('App008', 'C003');
INSERT INTO Belong (Aid, Cid) VALUES ('App009', 'C004');
INSERT INTO Belong (Aid, Cid) VALUES ('App010', 'C004');
INSERT INTO Belong (Aid, Cid) VALUES ('App011', 'C001');
INSERT INTO Belong (Aid, Cid) VALUES ('App012', 'C005');
INSERT INTO Belong (Aid, Cid) VALUES ('App001', 'C003');





INSERT INTO Replicia (复制品DBSid, 被复制DBSid) VALUES ('DBS002', 'DBS001');


INSERT INTO User (Uid, 性别, 年龄, 邮箱) VALUES ('User001', '男', '30', 'user001@example.com');
INSERT INTO User (Uid, 性别, 年龄, 邮箱) VALUES ('User002', '女', '25', 'user002@example.com');
INSERT INTO User (Uid, 性别, 年龄, 邮箱) VALUES ('User003', '男', '40', 'user003@example.com');
INSERT INTO User (Uid, 性别, 年龄, 邮箱) VALUES ('User004', '女', '32', 'user004@example.com');
INSERT INTO User (Uid, 性别, 年龄, 邮箱) VALUES ('User005', '男', '28', 'user005@example.com');
INSERT INTO User (Uid, 性别, 年龄, 邮箱) VALUES ('User006', '女', '45', 'user006@example.com');
INSERT INTO User (Uid, 性别, 年龄, 邮箱) VALUES ('User007', '男', '31', 'user007@example.com');
INSERT INTO User (Uid, 性别, 年龄, 邮箱) VALUES ('User008', '女', '26', 'user008@example.com');
INSERT INTO User (Uid, 性别, 年龄, 邮箱) VALUES ('User009', '男', '35', 'user009@example.com');
INSERT INTO User (Uid, 性别, 年龄, 邮箱) VALUES ('User010', '女', '29', 'user010@example.com');
INSERT INTO User (Uid, 性别, 年龄, 邮箱) VALUES ('User011', '男', '42', 'user011@example.com');
INSERT INTO User (Uid, 性别, 年龄, 邮箱) VALUES ('User012', '女', '27', 'user012@example.com');
INSERT INTO User (Uid, 性别, 年龄, 邮箱) VALUES ('User013', '男', '33', 'user013@example.com');
INSERT INTO User (Uid, 性别, 年龄, 邮箱) VALUES ('User014', '女', '31', 'user014@example.com');
INSERT INTO User (Uid, 性别, 年龄, 邮箱) VALUES ('User015', '男', '37', 'user015@example.com');
INSERT INTO User (Uid, 性别, 年龄, 邮箱) VALUES ('User016', '女', '28', 'user016@example.com');
INSERT INTO User (Uid, 性别, 年龄, 邮箱) VALUES ('User017', '男', '43', 'user017@example.com');
INSERT INTO User (Uid, 性别, 年龄, 邮箱) VALUES ('User018', '女', '30', 'user018@example.com');
INSERT INTO User (Uid, 性别, 年龄, 邮箱) VALUES ('User019', '男', '36', 'user019@example.com');
INSERT INTO User (Uid, 性别, 年龄, 邮箱) VALUES ('User020', '女', '29', 'user020@example.com');


INSERT INTO useof (Uid, Aid) VALUES ('User001', 'App001');
INSERT INTO useof (Uid, Aid) VALUES ('User006', 'App007');
INSERT INTO useof (Uid, Aid) VALUES ('User018', 'App002');
INSERT INTO useof (Uid, Aid) VALUES ('User020', 'App005');
INSERT INTO useof (Uid, Aid) VALUES ('User010', 'App010');
INSERT INTO useof (Uid, Aid) VALUES ('User012', 'App008');
INSERT INTO useof (Uid, Aid) VALUES ('User019', 'App012');
INSERT INTO useof (Uid, Aid) VALUES ('User013', 'App001');
INSERT INTO useof (Uid, Aid) VALUES ('User016', 'App004');
INSERT INTO useof (Uid, Aid) VALUES ('User007', 'App009');
INSERT INTO useof (Uid, Aid) VALUES ('User003', 'App011');
INSERT INTO useof (Uid, Aid) VALUES ('User011', 'App006');
INSERT INTO useof (Uid, Aid) VALUES ('User017', 'App003');
INSERT INTO useof (Uid, Aid) VALUES ('User001', 'App010');
INSERT INTO useof (Uid, Aid) VALUES ('User014', 'App002');
INSERT INTO useof (Uid, Aid) VALUES ('User009', 'App008');
INSERT INTO useof (Uid, Aid) VALUES ('User005', 'App005');
INSERT INTO useof (Uid, Aid) VALUES ('User004', 'App012');
INSERT INTO useof (Uid, Aid) VALUES ('User015', 'App007');
INSERT INTO useof (Uid, Aid) VALUES ('User002', 'App006');
INSERT INTO useof (Uid, Aid) VALUES ('User008', 'App001');
INSERT INTO useof (Uid, Aid) VALUES ('User020', 'App009');
INSERT INTO useof (Uid, Aid) VALUES ('User006', 'App004');
INSERT INTO useof (Uid, Aid) VALUES ('User012', 'App003');
INSERT INTO useof (Uid, Aid) VALUES ('User019', 'App011');
INSERT INTO useof (Uid, Aid) VALUES ('User013', 'App006');



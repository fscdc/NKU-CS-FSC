


DROP TABLE IF EXISTS `department`;
DROP TABLE IF EXISTS `major`;
DROP TABLE IF EXISTS `teacher`;
DROP TABLE IF EXISTS `course`;
DROP TABLE IF EXISTS `student`;
DROP TABLE IF EXISTS `student_course`;
DROP TABLE IF EXISTS `user_admin`;
DROP TABLE IF EXISTS `user_student`;



CREATE TABLE `department` (
  `d_id` int(3) NOT NULL AUTO_INCREMENT,
  `d_name` varchar(15) NOT NULL,
  `d_mng` varchar(10) NOT NULL,
  PRIMARY KEY (`d_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
alter table department auto_increment=1001;


CREATE TABLE `major` (
  `m_id` int(4) NOT NULL AUTO_INCREMENT,
  `d_id` int(3) NOT NULL,
  `m_name` varchar(20) NOT NULL,
  PRIMARY KEY (`m_id`),
  FOREIGN KEY (d_id) REFERENCES department(d_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
alter table major auto_increment=52001;


CREATE TABLE `teacher` (
  `t_id` int(8) NOT NULL AUTO_INCREMENT,
  `d_id` int(3) ,
  `t_name` varchar(15) ,
  `t_sex` char(1) ,
  `t_position` varchar(6) ,
  PRIMARY KEY (`t_id`),
  FOREIGN KEY (d_id) REFERENCES department(d_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
alter table teacher auto_increment=521001;

CREATE TABLE `course` (
  `c_id` int(4) NOT NULL AUTO_INCREMENT,
  `c_name` varchar(15) ,
  `credit` decimal(2,1) ,
  `d_id` int(3) ,
  `t_id` int(8),
  PRIMARY KEY (`c_id`),
  FOREIGN KEY (d_id) REFERENCES department(d_id) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (t_id) REFERENCES teacher(t_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
alter table course auto_increment=1314001;

CREATE TABLE `student` (
  `s_id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(10) ,
  `sex` char(1) ,
  `age` int(2) ,
  `d_id` int(3) ,
  `m_id` int(4) ,
  `email` char(30) ,
  `tel` varchar(11) ,
  PRIMARY KEY (`s_id`),
  FOREIGN KEY (d_id) REFERENCES department(d_id) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (m_id) REFERENCES major(m_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
alter table student auto_increment=2002001;

CREATE TABLE `student_course` (
  `s_id` int(10) NOT NULL,
  `c_id` int(4) NOT NULL,
  `score` int(3) ,
  `status` char(2) ,
  PRIMARY KEY (`s_id`,`c_id`),
  FOREIGN KEY (s_id) REFERENCES student(s_id) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (c_id) REFERENCES course(c_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE `user_admin` (
  `admin_ID` int(5) NOT NULL AUTO_INCREMENT,
  `admin_Name` varchar(15) NOT NULL,
  `admin_pwd` char(32) NOT NULL,
  PRIMARY KEY (`admin_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
alter table user_admin auto_increment=1;

CREATE TABLE `user_student` (
  `s_id` int(10) NOT NULL,
  `s_pwd` char(32) NOT NULL,
  PRIMARY KEY (`s_id`),
  FOREIGN KEY (s_id) REFERENCES student(s_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DELIMITER //
CREATE TRIGGER choose_course_check
BEFORE INSERT ON student_course
FOR EACH ROW
BEGIN
  DECLARE course_count INT;
  
  SELECT COUNT(*) INTO course_count
  FROM student_course
  WHERE s_id = NEW.s_id AND c_id = NEW.c_id;

  IF course_count > 0 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Error: You have already taken this course.';
  END IF;
END;
//
DELIMITER ;


DELIMITER //
CREATE TRIGGER ageandtel_input_check
BEFORE INSERT ON student
FOR EACH ROW
BEGIN
  IF NEW.age<10 OR NEW.age>40 OR NEW.tel not like '1__________' THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Error: illegal input,please exit again.';
  END IF;
END
//
DELIMITER ;

DELIMITER //
CREATE TRIGGER tel_update_check
BEFORE UPDATE ON student
FOR EACH ROW
BEGIN
  IF NEW.tel not like '1__________' THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Error: illegal tel,please exit again.';
  END IF;
END
//
DELIMITER ;

DELIMITER //
-- 成绩录入的更新存储过程，同步更新平均学分绩
CREATE PROCEDURE updatescore(
    IN studentID INT,
    IN courseID INT,
    IN courseGrade INT
)
BEGIN
    DECLARE courseStatus VARCHAR(10);
    -- 检查课程成绩是否合法
    IF courseGrade < 0 OR courseGrade > 100 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Score must be between 0 and 100.';
    ELSE
        -- 合法成绩，根据及格标准更新课程状态
        
        		
        IF courseGrade < 60 THEN
            SET courseStatus = '挂科';
        ELSE
            SET courseStatus = '修完';
        END IF;

        -- 更新学生选课表的课程状态和成绩
        UPDATE student_course
        SET status = courseStatus, score = courseGrade
        WHERE s_id = studentID AND c_id = courseID;
    END IF;
END;
//
DELIMITER ;


CREATE VIEW student_choose_course AS
SELECT c.c_id,c.c_name,c.credit,t.t_name,d.d_name
FROM course c
JOIN teacher t ON c.t_id=t.t_id
JOIN department d ON c.d_id=d.d_id;



DELIMITER //
CREATE PROCEDURE delete_student_cascade(IN studentid INT)
BEGIN
        DECLARE countone INT;
        DECLARE counttwo INT;
        DECLARE countthree INT;

        START TRANSACTION;
        DELETE FROM student_course WHERE s_id = studentid;
        DELETE FROM user_student WHERE s_id = studentid;
        DELETE FROM student WHERE s_id = studentid;
        SET countone = (SELECT COUNT(*) FROM student WHERE s_id = studentid),
               counttwo = (SELECT COUNT(*) FROM student_course WHERE s_id = studentid),
               countthree = (SELECT COUNT(*) FROM user_student WHERE s_id = studentid);
        IF countone+counttwo+countthree =  0 THEN
                COMMIT;
        ELSE
                ROLLBACK;  
        END IF;
END;
//
DELIMITER ;


DELIMITER //
CREATE PROCEDURE updateposition(
    IN teacherID INT,
    IN teacherposition VARCHAR(6)
)
BEGIN

    DECLARE countpass INT;
    DECLARE countfail INT;
    
    SELECT count(*) INTO countfail
    FROM student_course 
    JOIN course ON course.c_id=student_course.c_id
    WHERE course.t_id=teacherID and student_course.status='挂科';
    
    SELECT count(*) INTO countpass
    FROM student_course 
    JOIN course ON course.c_id=student_course.c_id
    WHERE course.t_id=teacherID and student_course.status='修完';

    
    IF countpass < countfail THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: the teacher has no right to get new position.';
    ELSE	
        UPDATE teacher
        SET t_position=teacherposition
        WHERE t_id =teacherID;
    END IF;
END;
//
DELIMITER ;
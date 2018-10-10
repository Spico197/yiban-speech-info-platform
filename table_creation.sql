-- SQLITE3
CREATE TABLE Speech (
    speech_id           INT PRIMARY KEY NOT NULL,   -- 主键 ID
    speech_name         TEXT,   -- 讲座名
    speaker             TEXT,   -- 主讲人
    introduction        TEXT,   -- 主讲内容简介
    start_name          TEXT,   -- 开始时间
    place               TEXT,   -- 讲座地点
    capacity            INT,    -- 讲座地点容量
    chair_remain_number INT     -- 讲座剩余座位数
); 
CREATE TABLE Student (
    stu_number          INT PRIMARY KEY NOT NULL,   -- 学号
    stu_name            TEXT,   -- 姓名
    stu_college         TEXT,   -- 学院
    stu_class           TEXT,   -- 班级
    stu_phone_number    TEXT    -- 电话号码
);
CREATE TABLE Booking (
    order_id            INT PRIMARY KEY NOT NULL,   -- 主键 ID，订单号
    order_speech_id     INT,    -- 讲座号
    order_stu_numeber   INT     -- 学生学号
);

-- INSERT INTO Speech
-- VALUES (1, 爬虫技术, 康师傅, );
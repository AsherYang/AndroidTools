SET SESSION default_storage_engine = "InnoDB";
SET SESSION time_zone = "+8:00";
ALTER DATABASE CHARACTER SET "utf8mb4";

-- adb 命令表
DROP TABLE IF EXISTS adb_cmds;
CREATE TABLE adb_cmds (
    _id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    adb_cmd_name VARCHAR(20),
    adb_cmd VARCHAR(300) NOT NULL UNIQUE,
    adb_cmd_desc VARCHAR(50)
);

DROP TABLE IF EXISTS tips_today;
CREATE TABLE tips_today (
    _id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    tips_type VARCHAR(5),
    tips_desc VARCHAR(100)
);

-- 定时任务表
--DROP TABLE IF EXISTS scheduler_jobs;
--CREATE TABLE scheduler_jobs (
--    _id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
--    job_name VARCHAR(20),
--    job_trigger VARCHAR(50),
--    login_time VARCHAR(30)
--);

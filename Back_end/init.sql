-- 初始化资产管理数据库
CREATE DATABASE IF NOT EXISTS asset_management
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE asset_management;

-- 表结构由 SQLAlchemy 在应用启动时自动创建/迁移。
-- 下面是示例数据，建议先启动一次后端让表生成，再执行 INSERT。
-- INSERT INTO assets
--   (asset_code, category, brand, model, serial_number, specification,
--    purchase_date, supplier, price, warranty_until, location, owner, department, status)
-- VALUES
--   ('IT-2024-0005', '笔记本电脑', '联想', 'ThinkPad T14s', 'PF5XXXXX',
--    'R7-7840U/16GB/512GB',
--    '2024-03-20 00:00:00', '联想官网', 7999.00, '2027-03-20 00:00:00',
--    '库房', NULL, NULL, '闲置');

CREATE SCHEMA stage;

USE stage;

CREATE TABLE `rates` (
  `CURRENCY_NAME` varchar(100) DEFAULT NULL,
  `CURRENCY_UNIT` int DEFAULT NULL,
  `CURRENCY_CODE` char(3) DEFAULT NULL,
  `CURRENCY_RATE` decimal(6,4) DEFAULT NULL,
  `RATE_DATE` date DEFAULT NULL,
  `UPLOAD_TIME` datetime DEFAULT NULL,
  UNIQUE KEY `ix_one_day_value` (`CURRENCY_CODE`,`RATE_DATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- CREATE UNIQUE INDEX  ix_one_day_value ON rates(currency_code, rate_date);
-- SHOW INDEXES FROM rates;
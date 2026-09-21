

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `bot_db`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `api_keys`
--

CREATE TABLE `api_keys` (
  `id` int(11) NOT NULL,
  `service_name` varchar(50) DEFAULT NULL,
  `api_key` varchar(255) DEFAULT NULL,
  `secret_key` varchar(255) DEFAULT NULL,
  `base_url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `api_keys`
--

INSERT INTO `api_keys` (`id`, `service_name`, `api_key`, `secret_key`, `base_url`) VALUES
();

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `bot_settings`
--

CREATE TABLE `bot_settings` (
  `id` int(11) NOT NULL,
  `fb_page_token` text DEFAULT NULL,
  `fb_verify_token` varchar(255) DEFAULT NULL,
  `ig_page_token` text DEFAULT NULL,
  `ig_verify_token` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `bot_settings`
--

INSERT INTO `bot_settings` (`id`, `fb_page_token`, `fb_verify_token`, `ig_page_token`, `ig_verify_token`) VALUES
();

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `customers`
--

CREATE TABLE `customers` (
  `facebook_id` varchar(100) NOT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `customers`
--

INSERT INTO `customers` (`facebook_id`, `full_name`, `phone`, `address`, `updated_at`) VALUES
();

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `expenses`
--

CREATE TABLE `expenses` (
  `id` int(11) NOT NULL,
  `expense_name` varchar(255) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `expense_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `expenses`
--

INSERT INTO `expenses` (`id`, `expense_name`, `amount`, `expense_date`) VALUES
();

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `inventory`
--

CREATE TABLE `inventory` (
  `id` int(11) NOT NULL,
  `barcode` varchar(100) DEFAULT NULL,
  `product_name` varchar(255) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `stock` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `inventory`
--

INSERT INTO `inventory` (`id`, `barcode`, `product_name`, `price`, `stock`) VALUES
();

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `customer_id` varchar(100) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `serial_number` varchar(100) DEFAULT NULL,
  `billing_info` text DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `status` varchar(50) DEFAULT 'Kargo Bekliyor',
  `invoice_no` varchar(100) DEFAULT NULL,
  `tracking_code` varchar(100) DEFAULT NULL,
  `order_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `orders`
--

INSERT INTO `orders` (`id`, `customer_id`, `product_id`, `serial_number`, `billing_info`, `price`, `status`, `invoice_no`, `tracking_code`, `order_date`) VALUES
();

--
-- Tetikleyiciler `orders`
--
DELIMITER $$
CREATE TRIGGER `trg_after_order_insert` AFTER INSERT ON `orders` FOR EACH ROW BEGIN
    UPDATE inventory SET stock = stock - 1 WHERE id = NEW.product_id;
    UPDATE product_serials SET status = 'Satıldı' WHERE serial_no = NEW.serial_number;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `product_serials`
--

CREATE TABLE `product_serials` (
  `serial_no` varchar(100) NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `status` enum('Mevcut','Satıldı','İade Edildi') DEFAULT 'Mevcut'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `product_serials`
--

INSERT INTO `product_serials` (`serial_no`, `product_id`, `status`) VALUES
();

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `returns`
--

CREATE TABLE `returns` (
  `id` int(11) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `return_code` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT 'Kargo Bekleniyor',
  `return_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `returns`
--

INSERT INTO `returns` (`id`, `order_id`, `return_code`, `status`, `return_date`) VALUES
(1, 3, 'IADE-T5830L', 'Kargo Alındı / Depoya Yolda', '2026-06-05 18:00:54');

--
-- Tetikleyiciler `returns`
--
DELIMITER $$
CREATE TRIGGER `trg_after_return_update` AFTER UPDATE ON `returns` FOR EACH ROW BEGIN
    IF NEW.status = 'Kargo Alındı / Depoya Yolda' AND OLD.status != 'Kargo Alındı / Depoya Yolda' THEN
        UPDATE inventory 
        SET stock = stock + 1 
        WHERE id = (SELECT product_id FROM orders WHERE id = NEW.order_id);
        
        UPDATE product_serials 
        SET status = 'Mevcut' 
        WHERE serial_no = (SELECT serial_number FROM orders WHERE id = NEW.order_id);
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password_hash` varchar(255) DEFAULT NULL,
  `role` enum('yonetici','ik','finans','depo','kargo') DEFAULT NULL,
  `salary` decimal(10,2) DEFAULT NULL,
  `bank_iban` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Tablo döküm verisi `users`
--

INSERT INTO `users` (`id`, `full_name`, `email`, `password_hash`, `role`, `salary`, `bank_iban`, `created_at`) VALUES
();

-- --------------------------------------------------------

--
-- Görünüm yapısı durumu `vw_expense_details`
-- (Asıl görünüm için aşağıya bakın)
--
CREATE TABLE `vw_expense_details` (
`id` int(11)
,`expense_name` varchar(255)
,`amount` decimal(10,2)
,`date` varchar(21)
);

-- --------------------------------------------------------

--
-- Görünüm yapısı durumu `vw_inventory_details`
-- (Asıl görünüm için aşağıya bakın)
--
CREATE TABLE `vw_inventory_details` (
`id` int(11)
,`barcode` varchar(100)
,`product_name` varchar(255)
,`price` decimal(10,2)
,`stock` int(11)
);

-- --------------------------------------------------------

--
-- Görünüm yapısı durumu `vw_order_details`
-- (Asıl görünüm için aşağıya bakın)
--
CREATE TABLE `vw_order_details` (
`id` int(11)
,`customer_name` varchar(100)
,`phone` varchar(20)
,`billing_info` text
,`product_name` varchar(255)
,`price` decimal(10,2)
,`payment_status` varchar(8)
,`date` varchar(21)
,`status` varchar(50)
,`tracking_code` varchar(100)
,`invoice_no` varchar(100)
,`serial_number` varchar(100)
);

-- --------------------------------------------------------

--
-- Görünüm yapısı durumu `vw_personnel_details`
-- (Asıl görünüm için aşağıya bakın)
--
CREATE TABLE `vw_personnel_details` (
`id` int(11)
,`full_name` varchar(100)
,`email` varchar(100)
,`role` enum('yonetici','ik','finans','depo','kargo')
,`salary` decimal(10,2)
,`bank_iban` varchar(100)
,`hire_date` varchar(10)
);

-- --------------------------------------------------------

--
-- Görünüm yapısı durumu `vw_return_details`
-- (Asıl görünüm için aşağıya bakın)
--
CREATE TABLE `vw_return_details` (
`return_id` int(11)
,`customer_id` varchar(100)
,`product_name` varchar(255)
,`return_code` varchar(50)
,`status` varchar(50)
,`date` varchar(10)
);

-- --------------------------------------------------------

--
-- Görünüm yapısı `vw_expense_details`
--
DROP TABLE IF EXISTS `vw_expense_details`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_expense_details`  AS SELECT `expenses`.`id` AS `id`, `expenses`.`expense_name` AS `expense_name`, `expenses`.`amount` AS `amount`, date_format(`expenses`.`expense_date`,'%d.%m.%Y %H:%i') AS `date` FROM `expenses` ;

-- --------------------------------------------------------

--
-- Görünüm yapısı `vw_inventory_details`
--
DROP TABLE IF EXISTS `vw_inventory_details`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_inventory_details`  AS SELECT `inventory`.`id` AS `id`, `inventory`.`barcode` AS `barcode`, `inventory`.`product_name` AS `product_name`, `inventory`.`price` AS `price`, `inventory`.`stock` AS `stock` FROM `inventory` ;

-- --------------------------------------------------------

--
-- Görünüm yapısı `vw_order_details`
--
DROP TABLE IF EXISTS `vw_order_details`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_order_details`  AS SELECT `o`.`id` AS `id`, `c`.`full_name` AS `customer_name`, `c`.`phone` AS `phone`, `o`.`billing_info` AS `billing_info`, `i`.`product_name` AS `product_name`, `o`.`price` AS `price`, 'Başarılı' AS `payment_status`, date_format(`o`.`order_date`,'%d.%m.%Y %H:%i') AS `date`, `o`.`status` AS `status`, `o`.`tracking_code` AS `tracking_code`, `o`.`invoice_no` AS `invoice_no`, `o`.`serial_number` AS `serial_number` FROM ((`orders` `o` left join `customers` `c` on(`o`.`customer_id` = `c`.`facebook_id`)) left join `inventory` `i` on(`o`.`product_id` = `i`.`id`)) ;

-- --------------------------------------------------------

--
-- Görünüm yapısı `vw_personnel_details`
--
DROP TABLE IF EXISTS `vw_personnel_details`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_personnel_details`  AS SELECT `users`.`id` AS `id`, `users`.`full_name` AS `full_name`, `users`.`email` AS `email`, `users`.`role` AS `role`, `users`.`salary` AS `salary`, `users`.`bank_iban` AS `bank_iban`, date_format(`users`.`created_at`,'%d.%m.%Y') AS `hire_date` FROM `users` ;

-- --------------------------------------------------------

--
-- Görünüm yapısı `vw_return_details`
--
DROP TABLE IF EXISTS `vw_return_details`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_return_details`  AS SELECT `r`.`id` AS `return_id`, `o`.`customer_id` AS `customer_id`, `i`.`product_name` AS `product_name`, `r`.`return_code` AS `return_code`, `r`.`status` AS `status`, date_format(`r`.`return_date`,'%d.%m.%Y') AS `date` FROM ((`returns` `r` join `orders` `o` on(`r`.`order_id` = `o`.`id`)) join `inventory` `i` on(`o`.`product_id` = `i`.`id`)) ;

--
-- Dökümü yapılmış tablolar için indeksler
--

--
-- Tablo için indeksler `api_keys`
--
ALTER TABLE `api_keys`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `service_name` (`service_name`);

--
-- Tablo için indeksler `bot_settings`
--
ALTER TABLE `bot_settings`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`facebook_id`);

--
-- Tablo için indeksler `expenses`
--
ALTER TABLE `expenses`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `barcode` (`barcode`);

--
-- Tablo için indeksler `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `product_id` (`product_id`),
  ADD KEY `serial_number` (`serial_number`);

--
-- Tablo için indeksler `product_serials`
--
ALTER TABLE `product_serials`
  ADD PRIMARY KEY (`serial_no`),
  ADD KEY `product_id` (`product_id`);

--
-- Tablo için indeksler `returns`
--
ALTER TABLE `returns`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`);

--
-- Tablo için indeksler `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Dökümü yapılmış tablolar için AUTO_INCREMENT değeri
--

--
-- Tablo için AUTO_INCREMENT değeri `api_keys`
--
ALTER TABLE `api_keys`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Tablo için AUTO_INCREMENT değeri `expenses`
--
ALTER TABLE `expenses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Tablo için AUTO_INCREMENT değeri `inventory`
--
ALTER TABLE `inventory`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Tablo için AUTO_INCREMENT değeri `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Tablo için AUTO_INCREMENT değeri `returns`
--
ALTER TABLE `returns`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Tablo için AUTO_INCREMENT değeri `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Dökümü yapılmış tablolar için kısıtlamalar
--

--
-- Tablo kısıtlamaları `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`facebook_id`) ON DELETE SET NULL,
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `inventory` (`id`),
  ADD CONSTRAINT `orders_ibfk_3` FOREIGN KEY (`serial_number`) REFERENCES `product_serials` (`serial_no`) ON DELETE SET NULL;

--
-- Tablo kısıtlamaları `product_serials`
--
ALTER TABLE `product_serials`
  ADD CONSTRAINT `product_serials_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `inventory` (`id`) ON DELETE CASCADE;

--
-- Tablo kısıtlamaları `returns`
--
ALTER TABLE `returns`
  ADD CONSTRAINT `returns_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

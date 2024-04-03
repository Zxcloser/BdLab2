-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Апр 04 2024 г., 00:50
-- Версия сервера: 8.0.30
-- Версия PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `var1_tar2`
--

DELIMITER $$
--
-- Процедуры
--
CREATE DEFINER=`root`@`%` PROCEDURE `addToBasket` (IN `bookID` INT, IN `sessionID` INT, IN `quantity` INT)   begin
    declare availableBooks int;
    declare availableReserve int;
    
    select amount, reserve into availableBooks, availableReserve from Books where id = bookID;
    
    if availableBooks >= quantity then
        insert into Basket(book_id, amount, data, session) values (bookID, quantity, now(), sessionID);
        update Books set amount = amount - quantity where id = bookID;
    elseif availableBooks + availableReserve >= quantity then
        insert into Basket(book_id, amount, data, session) values (bookID, quantity, now(), sessionID);
        update Books set amount = 0, reserve = reserve - (quantity - availableBooks) where id = bookID;
    else
        signal sqlstate '45000' set message_text = 'Not enough books available';
    end if;
end$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Структура таблицы `Basket`
--

CREATE TABLE `Basket` (
  `id` int NOT NULL,
  `book_id` int DEFAULT NULL,
  `amount` int DEFAULT NULL,
  `data` datetime DEFAULT NULL,
  `session` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Basket`
--

INSERT INTO `Basket` (`id`, `book_id`, `amount`, `data`, `session`) VALUES
(1, 2, 1, '2024-04-03 23:24:49', 3),
(4, 1, 3, '2024-04-04 00:04:23', 2),
(7, 1, 3, '2024-04-04 00:05:39', 2),
(8, 3, 3, '2024-04-04 00:06:00', 2),
(10, 1, 1, '2024-04-04 00:48:01', 1);

-- --------------------------------------------------------

--
-- Структура таблицы `Books`
--

CREATE TABLE `Books` (
  `id` int NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `price` decimal(8,2) DEFAULT NULL,
  `amount` int DEFAULT NULL,
  `reserve` int DEFAULT NULL,
  `genre_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Books`
--

INSERT INTO `Books` (`id`, `name`, `price`, `amount`, `reserve`, `genre_id`) VALUES
(1, 'Преступление и наказание', '2222.00', 3, 3, 2),
(2, 'Евгений Онегин', '5600.00', 19, 10, 1),
(3, 'Я помню чудное мгновение...', '4000.00', 31, 5, 3);

-- --------------------------------------------------------

--
-- Структура таблицы `Genres`
--

CREATE TABLE `Genres` (
  `id` int NOT NULL,
  `name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `Genres`
--

INSERT INTO `Genres` (`id`, `name`) VALUES
(1, 'Поэзия'),
(2, 'Драма'),
(3, 'Проза');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `Basket`
--
ALTER TABLE `Basket`
  ADD PRIMARY KEY (`id`),
  ADD KEY `book_id` (`book_id`);

--
-- Индексы таблицы `Books`
--
ALTER TABLE `Books`
  ADD PRIMARY KEY (`id`),
  ADD KEY `genre_id` (`genre_id`);

--
-- Индексы таблицы `Genres`
--
ALTER TABLE `Genres`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `Basket`
--
ALTER TABLE `Basket`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT для таблицы `Books`
--
ALTER TABLE `Books`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `Genres`
--
ALTER TABLE `Genres`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `Basket`
--
ALTER TABLE `Basket`
  ADD CONSTRAINT `basket_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `Books` (`id`);

--
-- Ограничения внешнего ключа таблицы `Books`
--
ALTER TABLE `Books`
  ADD CONSTRAINT `books_ibfk_1` FOREIGN KEY (`genre_id`) REFERENCES `Genres` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

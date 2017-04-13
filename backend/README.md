# hero-backend

## 依赖
apt-get install libjpeg-dev

## 数据库表
```sql
CREATE TABLE `article` (
  `title` varchar(128) NOT NULL,
  `author` varchar(128) NOT NULL,
  `create_time` varchar(19) NOT NULL,
  `content` longtext NOT NULL,
  PRIMARY KEY (`title`),
  KEY `article_create_time_605c3822_uniq` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `picture` (
  `title` varchar(128) NOT NULL,
  `author` varchar(128) NOT NULL,
  `create_time` varchar(19) NOT NULL,
  `paths` longtext NOT NULL,
  PRIMARY KEY (`title`),
  KEY `picture_b16a6265` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `offset` (
  `type` varchar(32) NOT NULL,
  `href` varchar(256) NOT NULL,
  PRIMARY KEY (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

```

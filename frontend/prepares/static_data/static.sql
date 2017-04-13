/*
SQLyog Ultimate v11.42 (64 bit)
MySQL - 5.7.17-0ubuntu0.16.04.1 : Database - hero
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`hero` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `hero`;

/*Table structure for table `article` */

DROP TABLE IF EXISTS `article`;

CREATE TABLE `article` (
  `title` varchar(128) NOT NULL,
  `author` varchar(128) NOT NULL,
  `create_time` varchar(19) NOT NULL,
  `content` longtext NOT NULL,
  PRIMARY KEY (`title`),
  KEY `article_b16a6265` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `offset` */

DROP TABLE IF EXISTS `offset`;

CREATE TABLE `offset` (
  `type` varchar(32) NOT NULL,
  `href` varchar(256) NOT NULL,
  PRIMARY KEY (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `permission` */

DROP TABLE IF EXISTS `permission`;

CREATE TABLE `permission` (
  `name` varchar(128) NOT NULL,
  `description` varchar(128) NOT NULL,
  `url` varchar(128) NOT NULL,
  `superior` varchar(128) NOT NULL,
  `index` varchar(8) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `permission` */

insert  into `permission`(`name`,`description`,`url`,`superior`,`index`) values ('九阴真经','天之道，损有余而补不足','/hero/restrict/article/','注册用户访问','1.0'),('怜花宝鉴','怜花惜月，惊才绝艳','/hero/restrict/video/','注册用户访问','1.2'),('操作日志','操作日志','/hero/log/','系统管理','0.3'),('权限列表','权限列表','/hero/permission/','系统管理','0.2'),('注册用户访问','注册用户访问','','ROOT','1'),('游客访问','游客访问','','ROOT','2'),('玉女心经','乾坤互调，阴阳双合','/hero/restrict/photograph/','注册用户访问','1.1'),('用户列表','用户列表','/hero/user/','系统管理','0.0'),('系统管理','系统管理','','ROOT','0'),('角色列表','角色列表','/hero/role/','系统管理','0.1');

/*Table structure for table `picture` */

DROP TABLE IF EXISTS `picture`;

CREATE TABLE `picture` (
  `title` varchar(128) NOT NULL,
  `author` varchar(128) NOT NULL,
  `create_time` varchar(19) NOT NULL,
  `paths` longtext NOT NULL,
  PRIMARY KEY (`title`),
  KEY `picture_b16a6265` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `role` */

DROP TABLE IF EXISTS `role`;

CREATE TABLE `role` (
  `name` varchar(128) NOT NULL,
  `level` int(11) NOT NULL,
  `description` varchar(128) NOT NULL,
  `permissions` varchar(256) NOT NULL,
  `users` varchar(256) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `role` */

insert  into `role`(`name`,`level`,`description`,`permissions`,`users`) values ('注册用户',6,'注册用户','注册用户访问,九阴真经,玉女心经,怜花宝鉴',''),('系统管理员',0,'系统管理员','系统管理,用户列表,角色列表,权限列表,操作日志,注册用户访问,九阴真经,玉女心经,怜花宝鉴,游客访问','ximeibaoer@163.com');

/*Table structure for table `syslog` */

DROP TABLE IF EXISTS `syslog`;

CREATE TABLE `syslog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` varchar(19) NOT NULL,
  `operation` varchar(128) NOT NULL,
  `user` varchar(128) NOT NULL,
  `addr` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `syslog_07cc694b` (`time`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8;

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `account` varchar(128) NOT NULL,
  `password` varchar(128) NOT NULL,
  `username` varchar(128) NOT NULL,
  `phone` varchar(128) NOT NULL,
  `create_time` varchar(19) NOT NULL,
  `last_time` varchar(19) NOT NULL,
  `status` varchar(32) NOT NULL,
  `role` varchar(256) NOT NULL,
  PRIMARY KEY (`account`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `user` */

insert  into `user`(`account`,`password`,`username`,`phone`,`create_time`,`last_time`,`status`,`role`) values ('admin@163.com','NWE5YjQzOWM4YjUxYmViZjZiNjY1MGFmMmZiYTdmYzc=','admin','110','2017-04-13 02:13:31','2017-04-13 05:52:22','login','系统管理员');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;


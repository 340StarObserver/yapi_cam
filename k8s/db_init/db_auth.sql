-- MySQL dump 10.14  Distrib 5.5.56-MariaDB, for Linux (x86_64)
--
-- Host: master.mysql    Database: db_auth
-- ------------------------------------------------------
-- Server version	5.5.56-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `db_auth`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `db_auth` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;

USE `db_auth`;

--
-- Table structure for table `r_related_strategy`
--

DROP TABLE IF EXISTS `r_related_strategy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `r_related_strategy` (
  `strategyId` bigint(20) unsigned NOT NULL COMMENT '策略编号',
  `userUin` bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '子账号',
  `groupId` bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '用户组ID',
  PRIMARY KEY (`strategyId`,`userUin`,`groupId`),
  KEY `idx_userUin` (`userUin`),
  KEY `idx_groupId` (`groupId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='策略绑定关系表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `r_related_strategy`
--

LOCK TABLES `r_related_strategy` WRITE;
/*!40000 ALTER TABLE `r_related_strategy` DISABLE KEYS */;
INSERT INTO `r_related_strategy` VALUES (6,0,2),(8,909619752,0),(10,0,1),(10,0,2),(10,0,6),(10,909619752,0),(10,909619772,0),(10,909619781,0),(11,909623456,0),(12,909623456,0),(15,909623456,0),(100,909619752,0);
/*!40000 ALTER TABLE `r_related_strategy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `r_user_app`
--

DROP TABLE IF EXISTS `r_user_app`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `r_user_app` (
  `ownerUin` bigint(20) unsigned NOT NULL COMMENT '所属的uin',
  `appId` bigint(20) unsigned NOT NULL COMMENT 'AppId',
  PRIMARY KEY (`ownerUin`),
  UNIQUE KEY `appId` (`appId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `r_user_app`
--

LOCK TABLES `r_user_app` WRITE;
/*!40000 ALTER TABLE `r_user_app` DISABLE KEYS */;
INSERT INTO `r_user_app` VALUES (909619800,1251234420),(909619400,1251568418);
/*!40000 ALTER TABLE `r_user_app` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `r_user_group`
--

DROP TABLE IF EXISTS `r_user_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `r_user_group` (
  `groupId` bigint(20) unsigned NOT NULL COMMENT '用户组ID',
  `userUin` bigint(20) unsigned NOT NULL COMMENT '用户的uin',
  `addTime` datetime NOT NULL,
  PRIMARY KEY (`groupId`,`userUin`),
  KEY `idx_userUin` (`userUin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `r_user_group`
--

LOCK TABLES `r_user_group` WRITE;
/*!40000 ALTER TABLE `r_user_group` DISABLE KEYS */;
INSERT INTO `r_user_group` VALUES (1,909619752,'2018-03-04 14:29:59'),(2,909619781,'2018-03-04 15:12:39'),(6,909619752,'2018-03-04 15:48:17'),(6,909619772,'2018-03-04 16:46:55'),(6,909619781,'2018-03-04 16:46:55'),(8,909623456,'2018-04-22 15:09:03');
/*!40000 ALTER TABLE `r_user_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_group`
--

DROP TABLE IF EXISTS `t_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_group` (
  `groupId` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '用户组ID',
  `ownerUin` bigint(20) unsigned NOT NULL COMMENT '所属的uin',
  `groupName` varchar(255) NOT NULL COMMENT '用户组名',
  `groupRemark` text COMMENT '用户组备注',
  `groupNum` bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '组内用户数',
  `addTime` datetime NOT NULL,
  `modTime` datetime NOT NULL,
  PRIMARY KEY (`groupId`),
  UNIQUE KEY `idx_ownerUin_groupName` (`ownerUin`,`groupName`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_group`
--

LOCK TABLES `t_group` WRITE;
/*!40000 ALTER TABLE `t_group` DISABLE KEYS */;
INSERT INTO `t_group` VALUES (1,909619400,'超级管理员组','组内成员拥有一切权限',1,'2018-02-28 00:00:00','2018-03-01 16:17:43'),(2,909619400,'测试组','关联了测试应具备的若干策略',1,'2018-02-23 00:00:00','2018-02-28 09:45:43'),(5,909619800,'test_group_3','null',0,'2018-03-04 15:10:25','2018-03-04 15:10:25'),(6,909619400,'temp_group_1','temp for test',3,'2018-03-04 15:45:35','2018-03-04 15:45:35'),(7,909619400,'temp_group_2','temp for test',0,'2018-03-04 15:45:44','2018-03-04 15:45:44'),(8,909619400,'group_for_test_swoole','group_for_test_swoole',1,'2018-04-22 15:08:08','2018-04-22 15:08:08');
/*!40000 ALTER TABLE `t_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_secret`
--

DROP TABLE IF EXISTS `t_secret`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_secret` (
  `secretId` char(40) NOT NULL COMMENT '密钥ID',
  `secretKey` char(40) NOT NULL COMMENT '密钥KEY',
  `userUin` bigint(20) unsigned NOT NULL COMMENT '用户的uin',
  `status` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '密钥状态(0-启用中,1-禁用中,2-已删除)',
  `addTime` datetime NOT NULL,
  `modTime` datetime NOT NULL,
  `secretRemark` text COMMENT '密钥备注',
  PRIMARY KEY (`secretId`),
  KEY `idx_userUin` (`userUin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_secret`
--

LOCK TABLES `t_secret` WRITE;
/*!40000 ALTER TABLE `t_secret` DISABLE KEYS */;
INSERT INTO `t_secret` VALUES ('AKID5IodSGVKh4QOXHu8QL8Fl25KWGi2WAj1','5IodSNZKh4QOXHu8QL8Fl25KWGi2WAj1',909619752,2,'2018-02-18 20:36:20','2018-02-18 22:29:37',''),('AKID8KicVF5Ih4ROXHu8QBWEl25KWGi2WAj1','8KidWJUKh4ROXHu8QBWEl25KWGi2WAj1',909619400,0,'2018-02-18 22:32:15','2018-02-18 22:32:15','...'),('AKID9Bm3UO9Kh4QOXHu8QNWFl25KWGi2WAj1','9Bm3UCVEh4QOXHu8QNWFl25KWGi2WAj1',909619752,1,'2018-02-18 20:38:22','2018-02-18 22:30:20',''),('AKIDUIg1TC9Kh4QNXHu8QCQLl25KWGi2WAj1','UIg1UGQEh4QNXHu8QCQLl25KWGi2WAj1',909619752,0,'2018-02-18 20:33:11','2018-02-18 22:46:02','控制台专用'),('AKIDWPh9SBYAh4RNXHu89GRBl25KWGi2WAj1','WPh9SE9Gh4RNXHu89GRBl25KWGi2WAj1',909619752,0,'2018-02-18 22:21:39','2018-02-18 22:21:39','console'),('AKIDZCj57L6Gk5VCXHu89J8Kl25KWGi2WAj1','ZCj57AXAk5VCXHu89J8Kl25KWGi2WAj1',909623456,0,'2018-04-22 15:10:27','2018-04-22 15:10:27','OpenAPIKey');
/*!40000 ALTER TABLE `t_secret` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_strategy`
--

DROP TABLE IF EXISTS `t_strategy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_strategy` (
  `strategyId` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '策略ID',
  `ownerUin` bigint(20) unsigned NOT NULL COMMENT '所属租户的根账号',
  `strategyType` int(11) unsigned NOT NULL COMMENT '策略类型(0-普通,1-根账号预设,2-子账号预设)',
  `strategyName` varchar(255) NOT NULL COMMENT '策略名字',
  `strategyRemark` text COMMENT '策略备注',
  `strategyRule` text NOT NULL COMMENT '策略规则',
  PRIMARY KEY (`strategyId`),
  KEY `ownerUin` (`ownerUin`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8 COMMENT='策略表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_strategy`
--

LOCK TABLES `t_strategy` WRITE;
/*!40000 ALTER TABLE `t_strategy` DISABLE KEYS */;
INSERT INTO `t_strategy` VALUES (1,909619400,1,'超级管理员','拥有一切权限','[{\"action\": [\"*:*\"], \"resource\": [\"*\"], \"effect\": \"allow\", \"condition\": [\"*\"]}]'),(3,909619800,0,'test-policy-03','xxxx','[{\"action\": [\"dfw:CreateSecurityGroup\"], \"resource\": [\"*\"], \"effect\": \"allow\", \"condition\": [\"*\"]}]'),(5,909619400,1,'super permission','with all permission','[{\"action\": [\"*:*\"], \"resource\": [\"*\"], \"effect\": \"allow\", \"condition\": [\"*\"]}]'),(6,909619400,2,'Default Strategy','','[{\"action\": [\"vm:GetVmList\", \"vpc:GetVpcList\", \"cbs:GetCloudDiskList\"], \"resource\": [\"*\"], \"effect\": \"allow\", \"condition\": [\"*\"]}]'),(7,909619400,0,'敏感的账户操作','不允许删用户组已经绑定用户组','[{\"action\": [\"account:DeleteUserGroup\", \"account:BindUserGroup\"], \"resource\": [\"*\"], \"effect\": \"deny\", \"condition\": [\"*\"]}]'),(8,909619400,0,'敏感的密钥操作','不允许创建和修改密钥状态','[{\"action\": [\"secret:OperateSecret\", \"secret:CreateSecret\"], \"resource\": [\"*\"], \"effect\": \"deny\", \"condition\": [\"*\"]}]'),(9,909619400,0,'allow visit redis to get instance list','','[{\"action\": [\"redis:GetInstanceList\"], \"resource\": [\"*\"], \"effect\": \"allow\", \"condition\": [{\"condType\": \"le\", \"condKey\": \"pageSize\", \"condValue\": 20}]}]'),(10,909619400,0,'allow visit redis to get instance list','','[{\"action\": [\"redis:ModifyInstanceConf\"], \"resource\": [\"yapi:redis:region/sz\"], \"effect\": \"allow\", \"condition\": [{\"condType\": \"ge\", \"condKey\": \"maxmemory\", \"condValue\": 128}, {\"condType\": \"le\", \"condKey\": \"maxmemory\", \"condValue\": 8192}]}]'),(11,909619400,0,'test_swoole_01','','[{\"action\": [\"cbs:ListBucketObjects\", \"grant:GetStrategyList\"], \"resource\": [\"*\"], \"effect\": \"deny\", \"condition\": [{\"condType\": \"gt\", \"condKey\": \"pageSize\", \"condValue\": 20}]}, {\"action\": [\"lb:*\"], \"resource\": [\"*\"], \"effect\": \"deny\", \"condition\": [\"*\"]}]'),(12,909619400,0,'test_swoole_02','','[{\"action\": [\"grant:GetStrategyRelated\", \"grant:GetStrategyList\"], \"resource\": [\"*\"], \"effect\": \"allow\", \"condition\": [{\"condType\": \"le\", \"condKey\": \"pageSize\", \"condValue\": 20}]}]'),(13,909619400,0,'test_swoole_03','','[{\"action\": [\"grant:*\"], \"resource\": [\"*\"], \"effect\": \"deny\", \"condition\": [\"*\"]}]'),(14,909619400,0,'test_swoole_04','','[{\"action\": [\"grant:*\"], \"resource\": [\"*\"], \"effect\": \"allow\", \"condition\": [\"*\"]}]'),(15,909619400,0,'允许查看策略关联实体列表','允许查看策略关联实体列表','[{\"action\": [\"grant:GetStrategyRelated\"], \"resource\": [\"*\"], \"effect\": \"allow\", \"condition\": [\"*\"]}]');
/*!40000 ALTER TABLE `t_strategy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_user`
--

DROP TABLE IF EXISTS `t_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_user` (
  `userUin` bigint(20) unsigned NOT NULL COMMENT '自己的uin',
  `ownerUin` bigint(20) unsigned NOT NULL COMMENT '所属的uin',
  `userName` varchar(255) NOT NULL COMMENT '用户名字',
  `userRemark` text COMMENT '用户备注',
  `userPhone` bigint(20) unsigned DEFAULT NULL COMMENT '用户手机',
  `userEmail` varchar(255) DEFAULT NULL COMMENT '用户邮箱',
  `addTime` datetime NOT NULL,
  `modTime` datetime NOT NULL,
  PRIMARY KEY (`userUin`),
  KEY `idx_ownerUin` (`ownerUin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_user`
--

LOCK TABLES `t_user` WRITE;
/*!40000 ALTER TABLE `t_user` DISABLE KEYS */;
INSERT INTO `t_user` VALUES (909619400,909619400,'根源','根账号',NULL,NULL,'2018-02-18 20:00:00','2018-02-18 20:00:00'),(909619752,909619400,'武安君','Permission Denied',13915497202,'478477395@qq.com','2018-02-18 20:20:00','2018-02-18 20:20:00'),(909619772,909619400,'魏斯','魏文侯',13912345678,'478477395@qq.com','2018-03-03 16:18:00','2018-03-03 16:20:00'),(909619781,909619400,'乐毅','昌国君',13900001111,'478477395@qq.com','2018-03-02 16:18:00','2018-03-03 16:20:00'),(909619800,909619800,'华夏','',NULL,NULL,'2018-03-03 16:00:00','2018-03-03 16:00:00'),(909620639,909619800,'赵雍','赵武灵王',13911112222,'478477395@qq.com','2018-03-01 16:18:00','2018-03-02 16:20:00'),(909623456,909619400,'伍子胥','三约伐楚',13915497202,'478477395@qq.com','2018-04-22 15:00:00','2018-04-22 15:00:00');
/*!40000 ALTER TABLE `t_user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-04-28 19:06:11

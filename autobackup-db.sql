-- MySQL dump 10.19  Distrib 10.3.39-MariaDB, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: auto-backup
-- ------------------------------------------------------
-- Server version	11.2.4-MariaDB-ubu2204

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `backup_traces`
--

DROP TABLE IF EXISTS `backup_traces`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `backup_traces` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_backup` int(11) DEFAULT NULL,
  `last_status` varchar(255) DEFAULT NULL,
  `createdAt` datetime NOT NULL DEFAULT current_timestamp(),
  `updatedAt` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `backup_traces_backups_FK` (`id_backup`),
  CONSTRAINT `backup_traces_backups_FK` FOREIGN KEY (`id_backup`) REFERENCES `backups` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backup_traces`
--

LOCK TABLES `backup_traces` WRITE;
/*!40000 ALTER TABLE `backup_traces` DISABLE KEYS */;
/*!40000 ALTER TABLE `backup_traces` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `backups`
--

DROP TABLE IF EXISTS `backups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `backups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backups`
--

LOCK TABLES `backups` WRITE;
/*!40000 ALTER TABLE `backups` DISABLE KEYS */;
/*!40000 ALTER TABLE `backups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `codigos`
--

DROP TABLE IF EXISTS `codigos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `codigos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_backup` int(11) DEFAULT NULL,
  `no_bloque` int(11) DEFAULT NULL,
  `no_linea` int(11) DEFAULT NULL,
  `linea` varchar(255) DEFAULT NULL,
  `run_as_sudo` tinyint(1) DEFAULT NULL,
  `paralelo` tinyint(1) DEFAULT NULL,
  `createdAt` datetime NOT NULL DEFAULT curdate(),
  `updatedAt` datetime NOT NULL DEFAULT curdate(),
  PRIMARY KEY (`id`),
  KEY `codigos_backups_FK_1` (`id_backup`),
  CONSTRAINT `codigos_backups_FK_1` FOREIGN KEY (`id_backup`) REFERENCES `backups` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `codigos`
--

LOCK TABLES `codigos` WRITE;
/*!40000 ALTER TABLE `codigos` DISABLE KEYS */;
/*!40000 ALTER TABLE `codigos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `file_traces`
--

DROP TABLE IF EXISTS `file_traces`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `file_traces` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_backup` int(11) DEFAULT NULL,
  `file` varchar(255) DEFAULT NULL,
  `size` int(11) DEFAULT NULL,
  `createdAt` datetime NOT NULL DEFAULT curtime(),
  `updatedAt` datetime NOT NULL DEFAULT curtime(),
  PRIMARY KEY (`id`),
  KEY `file_traces_backups_FK` (`id_backup`),
  CONSTRAINT `file_traces_backups_FK` FOREIGN KEY (`id_backup`) REFERENCES `backups` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `file_traces`
--

LOCK TABLES `file_traces` WRITE;
/*!40000 ALTER TABLE `file_traces` DISABLE KEYS */;
/*!40000 ALTER TABLE `file_traces` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `metadatas`
--

DROP TABLE IF EXISTS `metadatas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `metadatas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_backup` int(11) DEFAULT NULL,
  `ruta_respaldo` varchar(255) DEFAULT NULL,
  `ip_servidor` varchar(255) DEFAULT NULL,
  `ip_nas` varchar(255) DEFAULT NULL,
  `rash` varchar(255) DEFAULT NULL,
  `user_servidor` varchar(255) DEFAULT NULL,
  `pw_servidor` varchar(255) DEFAULT NULL,
  `port` int(11) DEFAULT NULL,
  `reintentos_maximos` int(11) DEFAULT NULL,
  `createdAt` datetime NOT NULL DEFAULT curdate(),
  `updatedAt` datetime NOT NULL DEFAULT curdate(),
  PRIMARY KEY (`id`),
  KEY `metadatas_backups_FK_1` (`id_backup`),
  CONSTRAINT `metadatas_backups_FK` FOREIGN KEY (`id_backup`) REFERENCES `backups` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metadatas`
--

LOCK TABLES `metadatas` WRITE;
/*!40000 ALTER TABLE `metadatas` DISABLE KEYS */;
/*!40000 ALTER TABLE `metadatas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'auto-backup'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-27  9:53:34

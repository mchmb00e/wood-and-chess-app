-- MySQL dump 10.13  Distrib 8.0.45, for Linux (x86_64)
--
-- Host: localhost    Database: INGSWI_WOODCHESS
-- ------------------------------------------------------
-- Server version	8.0.45-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `CARRO`
--

DROP TABLE IF EXISTS `CARRO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CARRO` (
  `CAR_ID` int NOT NULL AUTO_INCREMENT,
  `CAR_USURUT` int NOT NULL,
  `CAR_PRODID` int NOT NULL,
  `CAR_MAT1` int DEFAULT NULL,
  `CAR_MAT2` int DEFAULT NULL,
  `CAR_MAT3` int DEFAULT NULL,
  `CAR_MAT4` int DEFAULT NULL,
  PRIMARY KEY (`CAR_ID`),
  KEY `fk_car_producto` (`CAR_PRODID`),
  KEY `fk_car_material1` (`CAR_MAT1`),
  KEY `fk_car_material2` (`CAR_MAT2`),
  KEY `fk_car_material3` (`CAR_MAT3`),
  KEY `fk_car_material4` (`CAR_MAT4`),
  KEY `fk_carro_rut` (`CAR_USURUT`),
  CONSTRAINT `fk_car_material1` FOREIGN KEY (`CAR_MAT1`) REFERENCES `MATERIAL` (`MAT_ID`),
  CONSTRAINT `fk_car_material2` FOREIGN KEY (`CAR_MAT2`) REFERENCES `MATERIAL` (`MAT_ID`),
  CONSTRAINT `fk_car_material3` FOREIGN KEY (`CAR_MAT3`) REFERENCES `MATERIAL` (`MAT_ID`),
  CONSTRAINT `fk_car_material4` FOREIGN KEY (`CAR_MAT4`) REFERENCES `MATERIAL` (`MAT_ID`),
  CONSTRAINT `fk_car_producto` FOREIGN KEY (`CAR_PRODID`) REFERENCES `PRODUCTO` (`PROD_ID`),
  CONSTRAINT `fk_carro_rut` FOREIGN KEY (`CAR_USURUT`) REFERENCES `USUARIO` (`USU_RUT`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CARRO`
--

LOCK TABLES `CARRO` WRITE;
/*!40000 ALTER TABLE `CARRO` DISABLE KEYS */;
INSERT INTO `CARRO` VALUES (19,217933218,3,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `CARRO` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `COMENTARIO`
--

DROP TABLE IF EXISTS `COMENTARIO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `COMENTARIO` (
  `COM_ID` int NOT NULL AUTO_INCREMENT,
  `COM_PRODID` int NOT NULL,
  `COM_USURUT` int NOT NULL,
  `COM_CALIF` int NOT NULL,
  `COM_TITULO` varchar(50) NOT NULL,
  `COM_DESC` varchar(255) DEFAULT NULL,
  `COM_FECHA` datetime NOT NULL,
  PRIMARY KEY (`COM_ID`),
  KEY `fk_com_producto` (`COM_PRODID`),
  KEY `fk_com_usuario` (`COM_USURUT`),
  CONSTRAINT `fk_com_producto` FOREIGN KEY (`COM_PRODID`) REFERENCES `PRODUCTO` (`PROD_ID`),
  CONSTRAINT `fk_com_usuario` FOREIGN KEY (`COM_USURUT`) REFERENCES `USUARIO` (`USU_RUT`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `COMENTARIO`
--

LOCK TABLES `COMENTARIO` WRITE;
/*!40000 ALTER TABLE `COMENTARIO` DISABLE KEYS */;
/*!40000 ALTER TABLE `COMENTARIO` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `FOTOGRAFIA`
--

DROP TABLE IF EXISTS `FOTOGRAFIA`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `FOTOGRAFIA` (
  `FOTO_ID` int NOT NULL AUTO_INCREMENT,
  `FOTO_COMID` int NOT NULL,
  `FOTO_RUTA` varchar(255) NOT NULL,
  PRIMARY KEY (`FOTO_ID`),
  KEY `fk_foto_comentario` (`FOTO_COMID`),
  CONSTRAINT `fk_foto_comentario` FOREIGN KEY (`FOTO_COMID`) REFERENCES `COMENTARIO` (`COM_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `FOTOGRAFIA`
--

LOCK TABLES `FOTOGRAFIA` WRITE;
/*!40000 ALTER TABLE `FOTOGRAFIA` DISABLE KEYS */;
/*!40000 ALTER TABLE `FOTOGRAFIA` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `IMAGEN`
--

DROP TABLE IF EXISTS `IMAGEN`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `IMAGEN` (
  `IMA_ID` int NOT NULL AUTO_INCREMENT,
  `IMA_PRODID` int NOT NULL,
  `IMA_RUTA` varchar(50) NOT NULL,
  `IMA_PRINCIPAL` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`IMA_ID`),
  KEY `fk_ima_producto` (`IMA_PRODID`),
  CONSTRAINT `fk_ima_producto` FOREIGN KEY (`IMA_PRODID`) REFERENCES `PRODUCTO` (`PROD_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `IMAGEN`
--

LOCK TABLES `IMAGEN` WRITE;
/*!40000 ALTER TABLE `IMAGEN` DISABLE KEYS */;
INSERT INTO `IMAGEN` VALUES (3,3,'producto/3_1.jpg',1),(8,6,'producto/6_1.png',1),(9,6,'producto/6_2.png',0),(10,6,'producto/6_3.png',0);
/*!40000 ALTER TABLE `IMAGEN` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MATERIAL`
--

DROP TABLE IF EXISTS `MATERIAL`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MATERIAL` (
  `MAT_ID` int NOT NULL AUTO_INCREMENT,
  `MAT_NOMBRE` varchar(50) NOT NULL,
  `MAT_DESC` varchar(255) DEFAULT NULL,
  `MAT_IMAGEN` varchar(50) NOT NULL,
  `MAT_DISP` int NOT NULL DEFAULT '1',
  `MAT_RDIFFUSE` varchar(50) NOT NULL,
  `MAT_RNORMAL` varchar(50) NOT NULL,
  `MAT_RROUGH` varchar(50) NOT NULL,
  PRIMARY KEY (`MAT_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MATERIAL`
--

LOCK TABLES `MATERIAL` WRITE;
/*!40000 ALTER TABLE `MATERIAL` DISABLE KEYS */;
/*!40000 ALTER TABLE `MATERIAL` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PEDIDO`
--

DROP TABLE IF EXISTS `PEDIDO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PEDIDO` (
  `PED_ID` int NOT NULL AUTO_INCREMENT,
  `PED_USURUT` int NOT NULL,
  `PED_ESTADO` varchar(20) NOT NULL,
  `PED_CALLE` varchar(50) DEFAULT NULL,
  `PED_NUMERO` varchar(10) DEFAULT NULL,
  `PED_COMUNA` varchar(50) DEFAULT NULL,
  `PED_REGION` varchar(50) DEFAULT NULL,
  `PED_INDEXTRA` varchar(100) DEFAULT NULL,
  `PED_PTOTAL` int NOT NULL,
  `PED_TOKEN` varchar(255) DEFAULT NULL,
  `PED_FCREADO` datetime NOT NULL,
  `PED_FACTUAL` datetime NOT NULL,
  PRIMARY KEY (`PED_ID`),
  KEY `fk_pedido_usuario` (`PED_USURUT`),
  CONSTRAINT `fk_pedido_usuario` FOREIGN KEY (`PED_USURUT`) REFERENCES `USUARIO` (`USU_RUT`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PEDIDO`
--

LOCK TABLES `PEDIDO` WRITE;
/*!40000 ALTER TABLE `PEDIDO` DISABLE KEYS */;
INSERT INTO `PEDIDO` VALUES (2,224553951,'En preparación','Tebas','1604','Cerro navia','Región Metropolitana','Casa con reja negra, tocar el timbre.',149970,NULL,'2026-02-06 00:00:00','2026-02-06 00:00:00'),(3,217933218,'Enviado',NULL,NULL,NULL,NULL,NULL,539920,'96D79862C9F8D341DD4673CCF33C8494A47EB05J','2026-02-06 00:00:00','2026-02-06 21:31:21'),(4,217933218,'Anulado','Congillo','9999','Cerro navia','Región Metropolitana','Casa cerro navia',59980,'79F1E93901DC791B02AA28F9FFA7AF56B9F1FEAY','2026-02-06 00:00:00','2026-02-06 00:00:00'),(5,212370053,'Entregado',NULL,NULL,NULL,NULL,NULL,179980,'956AAF08CE8378190F10F4139C775D2417902DCE','2026-02-06 00:00:00','2026-02-06 21:57:52');
/*!40000 ALTER TABLE `PEDIDO` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PEDIDO_PRODUCTO`
--

DROP TABLE IF EXISTS `PEDIDO_PRODUCTO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PEDIDO_PRODUCTO` (
  `PEPR_ID` int NOT NULL AUTO_INCREMENT,
  `PEPR_PEDID` int NOT NULL,
  `PEPR_PRODID` int NOT NULL,
  `PEPR_MATPRI` int DEFAULT NULL,
  `PEPR_MATSEC` int DEFAULT NULL,
  `PEPR_MATTER` int DEFAULT NULL,
  `PEPR_MATCUAT` int DEFAULT NULL,
  PRIMARY KEY (`PEPR_ID`),
  KEY `fk_pepr_pedido` (`PEPR_PEDID`),
  KEY `fk_pepr_producto` (`PEPR_PRODID`),
  KEY `fk_pepr_matpri` (`PEPR_MATPRI`),
  KEY `fk_pepr_matsec` (`PEPR_MATSEC`),
  KEY `fk_pepr_matter` (`PEPR_MATTER`),
  KEY `fk_pepr_matcuat` (`PEPR_MATCUAT`),
  CONSTRAINT `fk_pepr_matcuat` FOREIGN KEY (`PEPR_MATCUAT`) REFERENCES `MATERIAL` (`MAT_ID`),
  CONSTRAINT `fk_pepr_matpri` FOREIGN KEY (`PEPR_MATPRI`) REFERENCES `MATERIAL` (`MAT_ID`),
  CONSTRAINT `fk_pepr_matsec` FOREIGN KEY (`PEPR_MATSEC`) REFERENCES `MATERIAL` (`MAT_ID`),
  CONSTRAINT `fk_pepr_matter` FOREIGN KEY (`PEPR_MATTER`) REFERENCES `MATERIAL` (`MAT_ID`),
  CONSTRAINT `fk_pepr_pedido` FOREIGN KEY (`PEPR_PEDID`) REFERENCES `PEDIDO` (`PED_ID`),
  CONSTRAINT `fk_pepr_producto` FOREIGN KEY (`PEPR_PRODID`) REFERENCES `PRODUCTO` (`PROD_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PEDIDO_PRODUCTO`
--

LOCK TABLES `PEDIDO_PRODUCTO` WRITE;
/*!40000 ALTER TABLE `PEDIDO_PRODUCTO` DISABLE KEYS */;
INSERT INTO `PEDIDO_PRODUCTO` VALUES (2,2,3,NULL,NULL,NULL,NULL),(5,3,3,NULL,NULL,NULL,NULL),(6,3,3,NULL,NULL,NULL,NULL),(7,3,3,NULL,NULL,NULL,NULL),(8,3,3,NULL,NULL,NULL,NULL),(9,3,3,NULL,NULL,NULL,NULL),(15,5,3,NULL,NULL,NULL,NULL),(16,5,3,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `PEDIDO_PRODUCTO` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PRODUCTO`
--

DROP TABLE IF EXISTS `PRODUCTO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PRODUCTO` (
  `PROD_ID` int NOT NULL AUTO_INCREMENT,
  `PROD_NOMBRE` varchar(50) NOT NULL,
  `PROD_DESC` varchar(255) DEFAULT NULL,
  `PROD_STOCK` int NOT NULL,
  `PROD_PRECIO` int NOT NULL,
  PRIMARY KEY (`PROD_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PRODUCTO`
--

LOCK TABLES `PRODUCTO` WRITE;
/*!40000 ALTER TABLE `PRODUCTO` DISABLE KEYS */;
INSERT INTO `PRODUCTO` VALUES (3,'Tablero de ajedrez personalizado 40cm',' ',192,89990),(6,'Nuevo pesebre','Nuevo pesebre artesanal muy bonito.',2,50123);
/*!40000 ALTER TABLE `PRODUCTO` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `USUARIO`
--

DROP TABLE IF EXISTS `USUARIO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `USUARIO` (
  `USU_RUT` int NOT NULL,
  `USU_NOMBRE` varchar(50) NOT NULL,
  `USU_APELLIDO` varchar(50) NOT NULL,
  `USU_EMAIL` varchar(50) NOT NULL,
  `USU_CONTRA` varchar(255) NOT NULL,
  `USU_ROL` varchar(3) NOT NULL,
  `USU_TELEF` varchar(9) NOT NULL,
  PRIMARY KEY (`USU_RUT`),
  UNIQUE KEY `USU_EMAIL` (`USU_EMAIL`),
  UNIQUE KEY `USU_TELEF` (`USU_TELEF`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `USUARIO`
--

LOCK TABLES `USUARIO` WRITE;
/*!40000 ALTER TABLE `USUARIO` DISABLE KEYS */;
INSERT INTO `USUARIO` VALUES (212370053,'Vicente','Arenas','vicentearenas33@gmail.com','$2b$12$Kp2IH0EXiYql6Vzpy4BlduRy7LViM7xTxjKRX3gkASyEBISfVgo.K','USR','912341234'),(217933218,'Genesis Belén','Canipan Miranda','genesis.canipan@usach.cl','$2b$12$CWaFMa4kSbTZp2umJ/.HGOfG4F4YHQm9Z/WI3b0R1bkh2biVlqkEu','USR','956034631'),(224553951,'Miguel Ángel','Chamorro Vásquez','miguel.chamorro@usach.cl','$2b$12$/sCjeoEnwuiY.mz0awMMt.XMv6gqWoAxVaZ/uYZ.4t1AuknI0o/Hm','ADM','933372677');
/*!40000 ALTER TABLE `USUARIO` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-11 14:16:27

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE User (
                    User_ID TEXT PRIMARY KEY,
                    name TEXT,
                    position TEXT CHECK (position IN ('manager', 'admin', 'normal')),
                    password TEXT
                    );
INSERT INTO User VALUES('U001','jacky','manager','123');
INSERT INTO User VALUES('U002','ken','admin','456');
INSERT INTO User VALUES('U003','fai','normal','789');
CREATE TABLE Dog (
                    dogID TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    detail TEXT
                    );
INSERT INTO Dog VALUES('D001','idk','good');
INSERT INTO Dog VALUES('D002','ido','good');
INSERT INTO Dog VALUES('D003','idp','good');
CREATE TABLE Video (
                        videoID TEXT PRIMARY KEY,  
                        dogID INTEGER NOT NULL,
                        datetime TEXT NOT NULL,
                        videoSrc TEXT NOT NULL,
                        FOREIGN KEY (dogID) REFERENCES Dog (dogID)                                        
                    );
INSERT INTO Video VALUES('V001','D001','2024-03-23 19:26:19','static/VIDEOS\D001\1 minute funny videos.mp4');
INSERT INTO Video VALUES('V002','D002','2024-03-23 19:27:33','static/VIDEOS\D002\The Wait  - 1 Minute Short Film _ Award Winning.mp4');
INSERT INTO Video VALUES('V003','D003','2024-03-23 19:27:40','static/VIDEOS\D003\1 Minute Video - Doggie.mp4');
INSERT INTO Video VALUES('V004','D003','2024-03-23 19:27:58','static/VIDEOS\D003\The Wait  - 1 Minute Short Film _ Award Winning.mp4');
CREATE TABLE Map (
                            mapID TEXT PRIMARY KEY,
                            dogID INTEGER NOT NULL,
                            datetime TEXT NOT NULL,
                            mapSrc TEXT NOT NULL,
                            FOREIGN KEY (dogID) REFERENCES Dog (dogID)
                        );
INSERT INTO Map VALUES('D001_Nitro_Wallpaper_01_3840x2400','D001','2024-03-23 19:32:25','static/maps\D001\D001_Nitro_Wallpaper_01_3840x2400.jpg');
INSERT INTO Map VALUES('D001_Nitro_Wallpaper_02_3840x2400','D001','2024-03-23 19:32:25','static/maps\D001\D001_Nitro_Wallpaper_02_3840x2400.jpg');
INSERT INTO Map VALUES('D001_Nitro_Wallpaper_03_3840x2400','D001','2024-03-23 19:32:25','static/maps\D001\D001_Nitro_Wallpaper_03_3840x2400.jpg');
INSERT INTO Map VALUES('D001_Nitro_Wallpaper_04_3840x2400','D001','2024-03-23 19:32:25','static/maps\D001\D001_Nitro_Wallpaper_04_3840x2400.jpg');
INSERT INTO Map VALUES('D002_Nitro_Wallpaper_01_3840x2400','D002','2024-03-23 19:32:37','static/maps\D002\D002_Nitro_Wallpaper_01_3840x2400.jpg');
INSERT INTO Map VALUES('D002_Nitro_Wallpaper_02_3840x2400','D002','2024-03-23 19:32:37','static/maps\D002\D002_Nitro_Wallpaper_02_3840x2400.jpg');
INSERT INTO Map VALUES('D002_Nitro_Wallpaper_03_3840x2400','D002','2024-03-23 19:32:37','static/maps\D002\D002_Nitro_Wallpaper_03_3840x2400.jpg');
INSERT INTO Map VALUES('D002_Nitro_Wallpaper_04_3840x2400','D002','2024-03-23 19:32:37','static/maps\D002\D002_Nitro_Wallpaper_04_3840x2400.jpg');
INSERT INTO Map VALUES('D003_Nitro_Wallpaper_01_3840x2400','D003','2024-03-23 19:32:47','static/maps\D003\D003_Nitro_Wallpaper_01_3840x2400.jpg');
INSERT INTO Map VALUES('D003_Nitro_Wallpaper_02_3840x2400','D003','2024-03-23 19:32:47','static/maps\D003\D003_Nitro_Wallpaper_02_3840x2400.jpg');
INSERT INTO Map VALUES('D003_Nitro_Wallpaper_03_3840x2400','D003','2024-03-23 19:32:47','static/maps\D003\D003_Nitro_Wallpaper_03_3840x2400.jpg');
INSERT INTO Map VALUES('D003_Nitro_Wallpaper_04_3840x2400','D003','2024-03-23 19:32:47','static/maps\D003\D003_Nitro_Wallpaper_04_3840x2400.jpg');
CREATE TABLE Permission (
                            UserID TEXT PRIMARY KEY,
                            dogID TEXT NOT NULL,
                            FOREIGN KEY (dogID) REFERENCES Dog (dogID),
                            FOREIGN KEY (UserID) REFERENCES User (User_ID)
                        );
INSERT INTO Permission VALUES('U001','D001');
INSERT INTO Permission VALUES('U002','D003');
INSERT INTO Permission VALUES('U003','D003');
COMMIT;

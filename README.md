# API-Database
API&amp;Database<br />
啲data已經喺曬個database裏面, 當你run database.py嘅時候, 應該要出到下面嗰啲data:<br /><br />
User_ID: U001, name: jacky, position: manager, password: 123<br />
User_ID: U002, name: ken, position: admin, password: 456<br />
User_ID: U003, name: fai, position: normal, password: 789<br />
dogID: D001, name: idk, detail: good<br />
dogID: D002, name: ido, detail: good<br />
dogID: D003, name: idp, detail: good<br />
mapID: D001_Nitro_Wallpaper_01_3840x2400, dogID: D001, datetime: 2024-03-23 19:32:25, mapSrc: static/maps\D001\D001_Nitro_Wallpaper_01_3840x2400.jpg<br />
mapID: D001_Nitro_Wallpaper_02_3840x2400, dogID: D001, datetime: 2024-03-23 19:32:25, mapSrc: static/maps\D001\D001_Nitro_Wallpaper_02_3840x2400.jpg<br />
mapID: D001_Nitro_Wallpaper_03_3840x2400, dogID: D001, datetime: 2024-03-23 19:32:25, mapSrc: static/maps\D001\D001_Nitro_Wallpaper_03_3840x2400.jpg<br />
mapID: D001_Nitro_Wallpaper_04_3840x2400, dogID: D001, datetime: 2024-03-23 19:32:25, mapSrc: static/maps\D001\D001_Nitro_Wallpaper_04_3840x2400.jpg<br />
mapID: D002_Nitro_Wallpaper_01_3840x2400, dogID: D002, datetime: 2024-03-23 19:32:37, mapSrc: static/maps\D002\D002_Nitro_Wallpaper_01_3840x2400.jpg<br />
mapID: D002_Nitro_Wallpaper_02_3840x2400, dogID: D002, datetime: 2024-03-23 19:32:37, mapSrc: static/maps\D002\D002_Nitro_Wallpaper_02_3840x2400.jpg<br />
mapID: D002_Nitro_Wallpaper_03_3840x2400, dogID: D002, datetime: 2024-03-23 19:32:37, mapSrc: static/maps\D002\D002_Nitro_Wallpaper_03_3840x2400.jpg<br />
mapID: D002_Nitro_Wallpaper_04_3840x2400, dogID: D002, datetime: 2024-03-23 19:32:37, mapSrc: static/maps\D002\D002_Nitro_Wallpaper_04_3840x2400.jpg<br />
mapID: D003_Nitro_Wallpaper_01_3840x2400, dogID: D003, datetime: 2024-03-23 19:32:47, mapSrc: static/maps\D003\D003_Nitro_Wallpaper_01_3840x2400.jpg<br />
mapID: D003_Nitro_Wallpaper_02_3840x2400, dogID: D003, datetime: 2024-03-23 19:32:47, mapSrc: static/maps\D003\D003_Nitro_Wallpaper_02_3840x2400.jpg<br />
mapID: D003_Nitro_Wallpaper_03_3840x2400, dogID: D003, datetime: 2024-03-23 19:32:47, mapSrc: static/maps\D003\D003_Nitro_Wallpaper_03_3840x2400.jpg<br />
mapID: D003_Nitro_Wallpaper_04_3840x2400, dogID: D003, datetime: 2024-03-23 19:32:47, mapSrc: static/maps\D003\D003_Nitro_Wallpaper_04_3840x2400.jpg<br />
Video ID: V001, Dog ID: D001, Datetime: 2024-03-23 19:26:19, Video Src: static/VIDEOS\D001\1 minute funny videos.mp4<br />
Video ID: V002, Dog ID: D002, Datetime: 2024-03-23 19:27:33, Video Src: static/VIDEOS\D002\The Wait  - 1 Minute Short Film _ Award Winning.mp4<br />
Video ID: V003, Dog ID: D003, Datetime: 2024-03-23 19:27:40, Video Src: static/VIDEOS\D003\1 Minute Video - Doggie.mp4<br />
Video ID: V004, Dog ID: D003, Datetime: 2024-03-23 19:27:58, Video Src: static/VIDEOS\D003\The Wait  - 1 Minute Short Film _ Award Winning.mp4<br />
UserID: U001, dogID: D001<br />
UserID: U002, dogID: D003<br />
UserID: U003, dogID: D003<br />
如果出唔到嘅再搵我<br /><br />
map table嘅已經整好曬 可以入到multiple file<br /><br />
啲database foreign key已經set好曬<br /><br />
喺個api入面,我喺三個地方set咗constraint: (create_permission, search_videos, info_dog),要個用戶輸入user id同埋password去check佢個position係咪normal(我入面嘅position setting係manager admin同埋normal, manager同admin咩都做到),如果check到佢係normal嘅話就唔畀佢繼續做落去<br /><br />
要加入嘅api都已經set咗<br /><br />
基本上要有嘅功能都整好咗

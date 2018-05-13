
![][py3x]  ![license]

> Disclaimer: This project is intended to study the Python 3.6, the Scrapy Spider Framework and the MongoDB database, it cannot be used for commercial or other personal intentions. If used improperly, it will be the individuals bear.

* The project is mainly used for crawling t66y.com forum, the largest Chinese BBS in the world. It retrieves title, id, poster image, download torrent url and post's url. Also DOWNLOAD the torrent file!!!
* The project crawls the posts and downloads the torrent file of each post in t66y.com quickly with a simple structure.
* The project can crawl up to **5 millon posts and 10 gigabyte torrent file per day**, depending on your personal network.
* The crawler requests 10 threads at a time. If your network is more performant you can request more threads and crawl a larger amount of posts per day.


## Architecture

* Python 3.6
* Scrapy framework.
* Randomly extracte Cookie and User-Agets from pool.
* Download the torrent of post and store it at local disk.
* Store the result item in MongoDB
* Start_requests start five Request based on froum's topic.
* Support crawling the whole page info.


## Instructions for use

### Pre-boot configuration

* Install MongoDB and start without configuration
* Install Python dependent modules：Scrapy, pymongo, requests
* Modify the configuration in `settings.py` as you wish.

### Start up

* `$cd ~/EpicScrapy1024/Epic1024/`
* `$ python Run.py`


## Run screenshots
![](https://wx4.sinaimg.cn/mw1024/a726c4d3gy1fr9p3tn7pyg20sb0dl1ky.gif)
![15.txt result file](https://mmbiz.qpic.cn/mmbiz_png/jA4Qc7C9IZSP5NvCWOHL0yuZ8w5KyibISsVRic2XxECG7ZTArjGJew2YEdXNicSVTp5dGiaaaEKaMHxxHkSBc8SoFw/0?wx_fmt=png)
![MongoDB status](https://mmbiz.qpic.cn/mmbiz_png/jA4Qc7C9IZSP5NvCWOHL0yuZ8w5KyibISwvFicyK9A1rJffECHmlHzcKaiczowIRqU4dmcy2VKs0ib4QG3hC0w9ia1w/0?wx_fmt=png)
![Downloaded torrent files](https://mmbiz.qpic.cn/mmbiz_png/jA4Qc7C9IZSP5NvCWOHL0yuZ8w5KyibISseQ4lHD6ia9jsVutsY1ib6DT00SGtw0N1ojeNJB0geUnUXwdLtJjNbFg/0?wx_fmt=png)
![Only 20min result, 117MB torrent file](https://mmbiz.qpic.cn/mmbiz_png/jA4Qc7C9IZSP5NvCWOHL0yuZ8w5KyibIS6aq4pfC2O5FMOUKaia8QeNXLdtah4vph0eGtLKz2ABmaj7vyUgYzypg/0?wx_fmt=png)

## Database description

Every data has been stored in different tables in Database based on their block_id. The structure of post_item are same.

#### fibXX table：

    topic_id:               The ID of post.
    topic_title:            Title of post.
    topic_image_url:        Screenshot list of video.
    topic_page_url:         The page url of post.
    block_id:               The ID of Post's block.
    torrent_download_url:   The video's torrent file download url.
    torrent_page_url:       The video's torrent file download page url.

## For Chinese

* 最后来一波福利，关注公众号：***皮克啪的铲屎官***，回复“EpicScrapy1024”，能够找到你需要的东西哦~

![关注并回复 EpicScrapy1024 有惊喜](https://mmbiz.qpic.cn/mmbiz_jpg/jA4Qc7C9IZS5CU8Eicxw9K4kIY8BibzDJX6QiahNQ0wDC2HLheXWp6CpITXBWcxt6E4SRlxHJyrxNO6v6TlKMgeUg/0?wx_fmt=jpeg)




[py3x]: https://img.shields.io/badge/python-3.x-brightgreen.svg
[license]: https://img.shields.io/badge/license-MIT-blue.svg
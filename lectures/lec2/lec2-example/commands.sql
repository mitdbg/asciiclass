
./process.awk > data.csv
./sqlite3

create table http(ip,unixtime,method,url,code,nf);
.separator |
.import data.csv http

.separator \t

select count(*) as count,url from http where url like "%.pdf%" group by url order by count desc limit 50;
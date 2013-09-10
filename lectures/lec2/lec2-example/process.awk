#!/bin/sh

awk 'BEGIN{
    m=split("Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec",d,"|")
    for(o=1;o<=m;o++){
	date[d[o]]=sprintf("%02d",o)
    }
}
{
    gsub(/\[/,"",$4); gsub(":","/",$4); gsub(/\]/,"",$5)
    n=split($4, DATE,"/")
    day=DATE[1]
    mth=DATE[2]
    year=DATE[3]
    hr=DATE[4]
    min=DATE[5]
    sec=DATE[6]
    MKTIME= mktime(year" "date[mth]" "day" "hr" "min" "sec)
    n=split($6,PARTS,"\"")
    print $1"|"MKTIME"|"PARTS[2]"|"$7"|"$9"|"NF

}' access_log-20121229

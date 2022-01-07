SOURCE_URL = "https://sitewebbixi.s3.amazonaws.com/uploads/docs/biximontreal-rentals-2021-10-65c60b.zip"
DATE = 2021-10
RENTALS_FILE = OD_2021_10_5.csv
STATIONS_FILE = stations_10_5.csv
GROUP_BY_INTERVAL = 1 hour

STATIONS_COLUMNS = "pk Int,name String,latitude Float,longitude Float"
STATIONS_QUERY = "\
	SELECT \
		pk as id,\
		name,\
		latitude as lat, \
		longitude as lon \
	FROM stations \
	WHERE \
		(lat BETWEEN -90 AND 90) AND (lon BETWEEN -180 AND 180) AND\
		NOT(lat = -1 AND lon = -1)\
"

RENTALS_COLUMNS = "start_date String,emplacement_pk_start Int,end_date String,emplacement_pk_end Int,duration_sec Int,is_member Boolean"
RENTALS_QUERY = "\
	SELECT \
		emplacement_pk_start as origin,\
		emplacement_pk_end as dest,\
		toStartOfInterval(toDateTime(substring(start_date,1,19)), INTERVAL ${GROUP_BY_INTERVAL}) as time,\
		COUNT(*) as count \
	FROM rentals \
	GROUP BY origin,dest,time \
	ORDER BY time,count DESC \
"


all: prepare-output output/locations.csv output/flows-${DATE}.csv output/flows-${DATE}.parquet \
output/flows-${DATE}.arrow output/flows-${DATE}.feather output/flows-${DATE}.zstd.feather

prepare-output:
	mkdir -p output/

downloads/bixi-rentals-${DATE}.zip:
	mkdir -p downloads/
	curl -o downloads/bixi-rentals-${DATE}.zip ${SOURCE_URL}

downloads/${RENTALS_FILE}: downloads/bixi-rentals-${DATE}.zip
	unzip downloads/bixi-rentals-${DATE}.zip -d downloads/
	touch downloads/${RENTALS_FILE}
	touch downloads/${STATIONS_FILE}

downloads/${STATIONS_FILE}: downloads/${RENTALS_FILE}

output/locations.csv: downloads/${STATIONS_FILE}
#	cp downloads/${STATIONS_FILE} output/locations.csv
	clickhouse local \
	--file=downloads/${STATIONS_FILE} \
	--input-format=CSVWithNames \
	--output-format=CSVWithNames \
	--table=stations \
	--structure=${STATIONS_COLUMNS} \
	--query=${STATIONS_QUERY} \
	> output/locations.csv

output/flows-${DATE}.csv: downloads/${RENTALS_FILE}
	clickhouse local \
	--file=downloads/${RENTALS_FILE} \
	--input-format=CSVWithNames \
	--output-format=CSVWithNames \
	--table=rentals \
	--structure=${RENTALS_COLUMNS} \
	--query=${RENTALS_QUERY} \
	> output/flows-${DATE}.csv

output/flows-${DATE}.parquet: downloads/${RENTALS_FILE}
	clickhouse local \
	--file=downloads/${RENTALS_FILE} \
	--input-format=CSVWithNames \
	--output-format=Parquet \
	--table=rentals \
	--structure=${RENTALS_COLUMNS} \
	--query=${RENTALS_QUERY} \
	> output/flows-${DATE}.parquet

output/flows-${DATE}.arrow: downloads/${RENTALS_FILE}
	clickhouse local \
	--file=downloads/${RENTALS_FILE} \
	--input-format=CSVWithNames \
	--output-format=Arrow \
	--table=rentals \
	--structure=${RENTALS_COLUMNS} \
	--query=${RENTALS_QUERY} \
	> output/flows-${DATE}.arrow


output/flows-${DATE}.feather: output/flows-${DATE}.arrow
	python3 ./arrow-to-feather.py output/flows-${DATE}.arrow output/flows-${DATE}.feather lz4

output/flows-${DATE}.zstd.feather: output/flows-${DATE}.arrow
	python3 ./arrow-to-feather.py output/flows-${DATE}.arrow output/flows-${DATE}.zstd.feather zstd

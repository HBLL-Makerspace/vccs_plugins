echo $1
echo $2
echo $3
echo $4

cd $1
raw2dng $3.$4 -j
mv $3.jpg $2
cd $2
convert $3.jpg $3.jpg -resize 200

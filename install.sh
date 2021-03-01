
outfile=run.sh
tmpfile=$(date +%Y%m%d%H%M%S)
echo '#!'$(which bash) > $outfile
echo 'cd '$(pwd) >> $outfile
echo $(which python3)" bing.py $1 img" >> $outfile
chmod +x $outfile
tasktxt='1 0 * * * '"$(pwd)/$outfile"
tasktxt2='1 0 \* \* \* '"$(pwd)/$outfile"
crontab -l > $tmpfile
sed -i -e "s|$tasktxt2||g" -e '/^$/d' $tmpfile
echo "$tasktxt" >> $tmpfile
crontab $tmpfile
cat $tmpfile
rm -f $tmpfile



outfile=run.sh
tmpfile=$(date +%Y%m%d%H%M%S)
echo '#!'$(which bash) > $outfile
echo 'cd '$(pwd) >> $outfile
echo $(which python3)" bing.py $1 img" >> $outfile
chmod +x $outfile
crontab -l > $tmpfile
echo "1 0 * * * $(pwd)/$outfile" >> $tmpfile
crontab $tmpfile
rm -f $tmpfile


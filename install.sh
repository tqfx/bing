
fileout=run.sh
filetmp=$(date +%Y%m%d%H%M%S)
echo '#!'$(which bash) > $fileout
echo 'cd '$(pwd) >> $fileout
echo $(which python3)" bing.py $1" >> $fileout
chmod +x $fileout

tasktxt='1 0 * * * '"$(pwd)/$fileout"
tasktxt2='1 0 \* \* \* '"$(pwd)/$fileout"
crontab -l > $filetmp 2> /dev/null
sed -i -e "s|$tasktxt2||g" -e '/^$/d' $filetmp
echo "$tasktxt" >> $filetmp
crontab $filetmp
rm -f $filetmp
crontab -l

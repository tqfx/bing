
outfile=run.sh
echo '#!'$(which bash) > $outfile
echo 'cd '$(pwd) >> $outfile
echo $(which python3)" bing.py $1 img" >> $outfile
chmod +x $outfile

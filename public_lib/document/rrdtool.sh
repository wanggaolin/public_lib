# centos 6.x
#报错

#解决
yum -y install pango-devel
rm -f /lib64/librrd.*   #删除原有的rrdtool lib
cd /usr/local/src ; wget https://oss.oetiker.ch/rrdtool/pub/rrdtool-1.5.0.tar.gz
tar -zxf rrdtool-1.5.0.tar.gz ; cd rrdtool-1.5.0
./configure --prefix=/usr/local/rrdtool && make && make install
ln -s  /usr/local/rrdtool/lib/librrd.* /lib64/
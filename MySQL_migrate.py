import os

def search(file_name, key_word):
	f=open(file_name,'r',encoding='utf-8')
	content=f.read()
	f.close()
	li=content.split('\n')
	num=len(li)
	for a in range(num):
		if '#' not in li[a] and key_word in li[a]:
			return a, li[a] 

def goes(dn):
	i,a=search('/etc/mysql/mysql.conf.d/mysqld.cnf', 'datadir')
	sn=a.split('=')[1].replace(' ','')
	if '/' == sn[-1]:
		sn=sn[:-1]
	if '/' == dn[-1]:
		dn=dn[:-1]
	os.system('sudo systemctl stop mysql')

	f=open('/etc/mysql/mysql.conf.d/mysqld.cnf','r', encoding='utf-8')
	con=f.read()
	f.close()

	replace_0=a.split('=')[0]+'='+dn+'/mysql'
	con=con.replace(a,replace_0)
	i,a=search('/etc/mysql/mysql.conf.d/mysqld.cnf', 'log_error')
	replace_1=a.split('=')[0]+'='+dn+'/mysql/error.log'
	con=con.replace(a,replace_1)
	os.system('sudo cp /etc/mysql/mysql.conf.d/mysqld.cnf /etc/mysql/mysql.conf.d/mysqld.cnf.bak') 

	f=open('/etc/mysql/mysql.conf.d/mysqld.cnf','w', encoding='utf-8')
	f.write(con)
	f.close()
	os.system('sudo rsync -va '+sn+'  '+dn)
	os.system('sudo mv '+sn+' '+sn+'.bak')

	f=open('/etc/apparmor.d/tunables/alias','r',encoding='utf-8')
	content=f.read()
	f.close()
	li=content.split('\n')
	num=len(li)
	for a in range(num):
		if '#' not in li[a] and ''!= li[a]:
			li[a]='#'+li[a]

	li.append('alias /var/lib/mysql/ -> '+dn+'/,')
	content=''
	for a in li:
		#f.write(a+'\n')
		content=content+a+'\n'
	os.system('sudo cp /etc/apparmor.d/tunables/alias /etc/apparmor.d/tunables/alias.bak')
	f=open('/etc/apparmor.d/tunables/alias', 'w', encoding='utf-8')
	f.write(content)
	f.close()
	os.system('sudo systemctl restart apparmor')
	os.system('sudo mkdir /var/lib/mysql/mysql -p')
	os.system('sudo systemctl start mysql')

import sys
if __name__=='__main__':
	argv=sys.argv
	#for a in argv:
	#	print(a)
	if 2!=len(argv):
		print('usage:'+argv[0]+' destination')
		exit(0)
	if '/' !=argv[1][0]:
		argv[1]=os.getcwd()+'/'+argv[1]
	#print(argv[1])	
	goes(argv[1])

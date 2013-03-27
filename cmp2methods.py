#-*- coding:gbk -*-
'''
该程序的目的是比较neibhor_distance和res的结果，看最终
sgm is shorter than res,pay attention
'''
import re

def time_cmp(sgm_time,res_time):
    '''
        比较sgm和res中的time的大小，返回他们的差。若sgm大,返回正值；res大返回负值
    '''
    res_time_list = res_time.split(':')
    res = 0
    if len(res_time_list) == 2:
        res = float(res_time_list[0])*60 + float(res_time_list[1])
    if len(res_time_list) == 3:
        res = float(res_time_list[0])*3600 + float(res_time_list[1])*60 \
                   + float(res_time_list[2])
    sgm = float(sgm_time)
    return sgm - res

def format_time(sgm_time):
    '''
        把sgm中以sec表示的时间变成h:m:s的形式，返回字符串
    '''
    ftime = float(sgm_time)
    hour = int(ftime/3600)
    min = int((ftime - hour*3600)/60)
    sec = ftime-hour*3600-min*60
    t = str(hour)+':'+str(min)+':'+str(sec) if hour>0 else str(min)+':'+format(sec,'0.3f')
    return t


res = open('Mc97114.res','r')
sgm = open('mc970114.sgm','r')
neighbor = open('neighbor_distance.txt','r')
compare = open('cmp.txt','w')

res_lines = res.readlines()
line1 = res_lines[0]
res_lines.pop(0)
segnum = re.search('\d+',line1)
segnum = int(segnum.group())
sgm_content = sgm.read()
spk_stime_list = re.findall(r'speaker=(\S+).*startTime=(\S+)',sgm_content)
list_length = len(spk_stime_list)

i = 0
last_begt = 0
last_clusid = 0
old_t = 0

'''
第一步：先写前3列
'''
while i < segnum: 
	res_line = res_lines[i]
	type = re.search(r'type=(\w*)',res_line)
	if type.group(1) == 'non':
		i += 1
		pass
	else:
		result = re.search('begt=(\S*) endt=(\S*).*clusid=(\d*)',res_line)
		begt,endt,clusid = result.group(1,2,3)			#begt是res里的时间
		
		'''写第一列,res中的起始时间'''
		compare.write(format(begt,'12'))   #保证对齐
		
		'''写第二列,res中获得的说话人是否变化的信息'''
		if last_clusid != clusid:
			if i == 1:
				compare.write(format('————','^15'))
			else:
				compare.write(format('r changed','15'))
		else:
			compare.write(format('r unchanged','15'))
			
		last_begt = begt			#保存上一段的开始时间
		last_clusid = clusid
		
		'''写第三列,neighbor的信息。注意要延迟1个,因为distance的第一项是sph1,2之间的距离,即对应于sph2的开始'''
		if i > 1:	#这里是1因为res的第一行是non，所以要跳过一个
			neighbor_line = neighbor.readline()
			distance = neighbor_line.split(' ')[-1]
			if (float(distance) > 480):
				compare.write(format('n changed','15') + '\n')
			else:
				compare.write(format('n unchanged','15') + '\n')
		else:
			compare.write(format('————','^15') + '\n')
		i += 1

res.close()
neighbor.close()
compare.close()
compare = open('cmp.txt','r+')  #用a+不行,指针必须在文件开始
cmp_lines = compare.readlines()
last_stime = spk_stime_list[0][1]
last_spk = spk_stime_list[0][1]
search_start = 0

for list_index in range(1,list_length): #从1开始,因为对第0段也无所谓有无变化
    current_stime = spk_stime_list[list_index][1]    #当前stime
    current_spk = spk_stime_list[list_index][0]        #当前speaker
    for i in range(search_start,len(cmp_lines)):
        begt = cmp_lines[i].split()[0]
        if time_cmp(current_stime,begt) < 0:
            break
    last_begt = cmp_lines[i-1].split()[0]
    search_start = i - 1    #更新搜索起始点
    if time_cmp(current_stime,begt) + time_cmp(current_stime,last_begt) < 0:
        #离last_begt更近,则把sgm的信息加入第i-1行 
        t = format_time(current_stime)
        if last_stime != current_stime:
            cmp_lines[i-1] = cmp_lines[i-1].rstrip('\n')
            cmp_lines[i-1] += 'changed(' + t + ')\n'
        else:
            cmp_lines[i-1] = cmp_lines[i-1].rstrip('\n')
            cmp_lines[i-1] += 'unchanged(' + t + ')\n'
            
    if time_cmp(current_stime,begt) + time_cmp(current_stime,last_begt) > 0:
        #离begt更近,则把sgm的信息加入第i行 
        t = format_time(current_stime)
        if last_stime != current_stime:
            cmp_lines[i] = cmp_lines[i].rstrip('\n')
            cmp_lines[i] += 'changed(' + t + ')\n'
        else:
            cmp_lines[i] = cmp_lines[i].rstrip('\n')
            cmp_lines[i] += 'unchanged(' + t + ')\n'
            
    last_stime = current_stime
    last_spk = current_spk

compare.close()
compare = open('cmp.txt','w')
for j in range(i):
    compare.write(cmp_lines[j])

compare.close()
sgm.close()

if __name__ == '__main__':
    import os 
    for a,b,c in os.walk('C:\ZY\EverythingandNothing\Python\文章&教程'):
        print(c)
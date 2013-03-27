#-*- coding:gbk -*-
'''
�ó����Ŀ���ǱȽ�neibhor_distance��res�Ľ����������
sgm is shorter than res,pay attention
'''
import re

def time_cmp(sgm_time,res_time):
    '''
        �Ƚ�sgm��res�е�time�Ĵ�С���������ǵĲ��sgm��,������ֵ��res�󷵻ظ�ֵ
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
        ��sgm����sec��ʾ��ʱ����h:m:s����ʽ�������ַ���
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
��һ������дǰ3��
'''
while i < segnum: 
	res_line = res_lines[i]
	type = re.search(r'type=(\w*)',res_line)
	if type.group(1) == 'non':
		i += 1
		pass
	else:
		result = re.search('begt=(\S*) endt=(\S*).*clusid=(\d*)',res_line)
		begt,endt,clusid = result.group(1,2,3)			#begt��res���ʱ��
		
		'''д��һ��,res�е���ʼʱ��'''
		compare.write(format(begt,'12'))   #��֤����
		
		'''д�ڶ���,res�л�õ�˵�����Ƿ�仯����Ϣ'''
		if last_clusid != clusid:
			if i == 1:
				compare.write(format('��������','^15'))
			else:
				compare.write(format('r changed','15'))
		else:
			compare.write(format('r unchanged','15'))
			
		last_begt = begt			#������һ�εĿ�ʼʱ��
		last_clusid = clusid
		
		'''д������,neighbor����Ϣ��ע��Ҫ�ӳ�1��,��Ϊdistance�ĵ�һ����sph1,2֮��ľ���,����Ӧ��sph2�Ŀ�ʼ'''
		if i > 1:	#������1��Ϊres�ĵ�һ����non������Ҫ����һ��
			neighbor_line = neighbor.readline()
			distance = neighbor_line.split(' ')[-1]
			if (float(distance) > 480):
				compare.write(format('n changed','15') + '\n')
			else:
				compare.write(format('n unchanged','15') + '\n')
		else:
			compare.write(format('��������','^15') + '\n')
		i += 1

res.close()
neighbor.close()
compare.close()
compare = open('cmp.txt','r+')  #��a+����,ָ��������ļ���ʼ
cmp_lines = compare.readlines()
last_stime = spk_stime_list[0][1]
last_spk = spk_stime_list[0][1]
search_start = 0

for list_index in range(1,list_length): #��1��ʼ,��Ϊ�Ե�0��Ҳ����ν���ޱ仯
    current_stime = spk_stime_list[list_index][1]    #��ǰstime
    current_spk = spk_stime_list[list_index][0]        #��ǰspeaker
    for i in range(search_start,len(cmp_lines)):
        begt = cmp_lines[i].split()[0]
        if time_cmp(current_stime,begt) < 0:
            break
    last_begt = cmp_lines[i-1].split()[0]
    search_start = i - 1    #����������ʼ��
    if time_cmp(current_stime,begt) + time_cmp(current_stime,last_begt) < 0:
        #��last_begt����,���sgm����Ϣ�����i-1�� 
        t = format_time(current_stime)
        if last_stime != current_stime:
            cmp_lines[i-1] = cmp_lines[i-1].rstrip('\n')
            cmp_lines[i-1] += 'changed(' + t + ')\n'
        else:
            cmp_lines[i-1] = cmp_lines[i-1].rstrip('\n')
            cmp_lines[i-1] += 'unchanged(' + t + ')\n'
            
    if time_cmp(current_stime,begt) + time_cmp(current_stime,last_begt) > 0:
        #��begt����,���sgm����Ϣ�����i�� 
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
    for a,b,c in os.walk('C:\ZY\EverythingandNothing\Python\����&�̳�'):
        print(c)
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

for list_index in range(list_length):
    '''
        ��α���sgm�ļ�����Ϊsgm�ֶν��٣����Դ����ȽϷ���
    '''
    current_stime = spk_stime_list[list_index][1]    #��ǰstime
    current_spk = spk_stime_list[list_index][0]        #��ǰspeaker
    while i < segnum: 
        res_line = res_lines[i]
        type = re.search(r'type=(\w*)',res_line)
        if type.group(1) == 'non':
            i += 1
            pass
        else:
            result = re.search('begt=(\S*) endt=(\S*).*clusid=(\d*)',res_line)
            begt,endt,clusid = result.group(1,2,3)            #begt��res���ʱ��
            if time_cmp(current_stime,begt) < 0:
                i -= 1
                begt = last_begt
                break
            elif i > 1:
                compare.write('\n')
            compare.write(str(begt)+'  ')
            compare.write(format(' ','6'))   #��֤����
            '''���res�л�õ�˵�����Ƿ�仯����Ϣ'''
            if last_clusid != clusid:
                if i == 1:
                    compare.write(format('��������','^15'))
                else:
                    compare.write(format('r changed','15'))
            else:
                compare.write(format('r unchanged','15'))
                
            last_begt = begt            #������һ�εĿ�ʼʱ��
            last_clusid = clusid
            '''���neighbor����Ϣ'''
            neighbor_line = neighbor.readline()
            distance = neighbor_line.split(' ')[-1]
            if (float(distance) > 1000):
                compare.write(format('n changed','15'))
            else:
                compare.write(format('n unchanged','15'))
            i += 1
     
    if list_index == 0:
        pass
    else:
        '''
        if time_cmp(last_stime,begt) + time_cmp(current_stime,begt) > 0: 
            #last_stime��begt����
            t = format_time(last_stime)
            if old_t != t: 
                old_t = t   #old_t�����ϴ�д����Ǹ�t,����������ĳЩ����»ᷢ�����ظ�д��
                if last_stime != current_stime:
                    compare.write('changed(' + t + ')')
                else:
                    compare.write('unchanged(' + t + ')')
        else:
            #current_time��begt����
            t = format_time(current_stime)
            if old_t != t: 
                old_t = t   
                if last_stime != current_stime:
                    compare.write('changed(' + t + ')')
                else:
                    compare.write('unchanged(' + t + ')')
        '''
        t = format_time(last_stime)
        if old_t != t: 
            old_t = t   #old_t�����ϴ�д����Ǹ�t,����������ĳЩ����»ᷢ�����ظ�д��
            if last_stime != current_stime: 
                compare.write('changed(' + t + ')')
            else:
                compare.write('unchanged(' + t + ')')
    last_stime = current_stime
    last_spk = current_spk
    compare.write('\n')



res.close()
sgm.close()
neighbor.close()
compare.close()

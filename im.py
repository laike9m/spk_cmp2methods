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

for list_index in range(list_length):
    '''
        这次遍历sgm文件，因为sgm分段较少，所以处理会比较方便
    '''
    current_stime = spk_stime_list[list_index][1]    #当前stime
    current_spk = spk_stime_list[list_index][0]        #当前speaker
    while i < segnum: 
        res_line = res_lines[i]
        type = re.search(r'type=(\w*)',res_line)
        if type.group(1) == 'non':
            i += 1
            pass
        else:
            result = re.search('begt=(\S*) endt=(\S*).*clusid=(\d*)',res_line)
            begt,endt,clusid = result.group(1,2,3)            #begt是res里的时间
            if time_cmp(current_stime,begt) < 0:
                i -= 1
                begt = last_begt
                break
            elif i > 1:
                compare.write('\n')
            compare.write(str(begt)+'  ')
            compare.write(format(' ','6'))   #保证对齐
            '''添加res中获得的说话人是否变化的信息'''
            if last_clusid != clusid:
                if i == 1:
                    compare.write(format('————','^15'))
                else:
                    compare.write(format('r changed','15'))
            else:
                compare.write(format('r unchanged','15'))
                
            last_begt = begt            #保存上一段的开始时间
            last_clusid = clusid
            '''添加neighbor的信息'''
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
            #last_stime离begt更近
            t = format_time(last_stime)
            if old_t != t: 
                old_t = t   #old_t保存上次写入的那个t,用来避免在某些情况下会发生的重复写入
                if last_stime != current_stime:
                    compare.write('changed(' + t + ')')
                else:
                    compare.write('unchanged(' + t + ')')
        else:
            #current_time离begt更近
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
            old_t = t   #old_t保存上次写入的那个t,用来避免在某些情况下会发生的重复写入
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

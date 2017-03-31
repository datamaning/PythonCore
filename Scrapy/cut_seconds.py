#!/usr/bin/python
import os
import sys
import shutil
reload(sys)
sys.setdefaultencoding('utf-8')

if len(sys.argv)!=5:
    print "Warning Usage:startsecond endsecond file_dir to_dir\n"
    print "Here is an example for you:"
    print "(I only want sound from 1s to 7s inputfile directory is /home/input/ outputfile directory is /home/outputfile) :\n"
    print "cut_tool.py 1 7 input_dir output_dir" 
    sys.exit()
sound_per_size=32000
start=int(sys.argv[1])
end=int(sys.argv[2])
cut_file_name=sys.argv[3]
end_dir=sys.argv[4]
def size_1_7(filename):
    filedata=open(filename,'rb')
    data_string=filedata.read(44)
    
    first=data_string[40:41]
    second=data_string[41:42]
    third=data_string[42:43]
    four=data_string[43:44]
    if len(first)==0:
        return 0
#data_string=unicode(data_string,'utf-16')
    byte_first=ord(first)
    byte_second=ord(second)*(2**8)
    byte_third=ord(third)*(2**16)
    byte_four=ord(four)*(2**24)

    sum= byte_first+byte_second+byte_third+byte_four
    if sum>=(start*sound_per_size)-100 and sum<=(end*sound_per_size):
        return 1
    return 0

if __name__=='__main__':
    if os.path.exists(end_dir)==False:
        os.mkdir(end_dir)
    end_dir=os.getcwd()+'/'+end_dir+'/'
    absolute=os.getcwd()+'/'+cut_file_name+'/'
    dir_list=os.listdir(cut_file_name)
    
    count =0  
    for dir in dir_list:
        path=absolute+dir+'/'
        end_path=end_dir+dir
        if os.path.exists(end_path):
            pass
            #print "exist"
        else:
            os.mkdir(end_path)
        for root,dirs,files in os.walk(path):
            for file in files:
                start_file=os.path.join(root,file)
                if size_1_7(start_file)==1:
                    shutil.copy(start_file,end_path)

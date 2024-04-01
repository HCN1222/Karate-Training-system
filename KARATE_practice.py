import tkinter,time,threading,serial,pandas
from datetime import *
import pandas as pd
from random import *

ra = Random()
ra.seed(0)

#print(type(r))

average_all = 0      #所有資料的平均
average_10_data = 0  #包含自身共前10筆資料
counter = 0             
current_num = 0         # current valid numbers of data
hit_time = 0            # how many time 
already_count = True   # hit plus or not
data_10 = []  #store 10-11 data
first_negative = True  #假如現在有個data，他是first_negative嗎?
base = datetime.now()  #往後n秒之基準點
quit = False
arduino = serial.Serial()

reaction_value = 0   #(integer)
wait_time = 0       #(integer)how long time will user wait to hit again
start_ran = datetime.now()        #(datetime)what is the current time that use uniform to get wait's value
trigger_head_st = datetime.now() #(datetime)time that can_hit_or_not show "hit" on the screen
whole_move_value =0  #(integer)
valid_start = False     #(boolean)told the program start to sensor final_data<0 case

def hit_update():
    print("go in hit_update")
    global average_all
    global average_10_data
    global counter
    global current_num
    global hit_time
    global already_count
    global data_10
    global first_negative
    global base
    global how_many_time_hit
    global quit
    
    while not quit:
        #print(counter)
        try:
            data_1 = arduino.readline().decode('unicode_escape').strip()  #data_1:string
            counter = counter + 1
            now_time = datetime.now()
        except:
            return 
        print("www:" + f"{counter}" + "qqqq:" + f"{quit}")
        if counter>=30:
            dataset_split = data_1.split(',')   #dataset_split: list
            ax = int(dataset_split[0])
            ay = int(dataset_split[1])   #what we need
            az = int(dataset_split[2])
            gx = int(dataset_split[3])
            gy = int(dataset_split[4])
            gz = int(dataset_split[5])
            y = int(dataset_split[6])
            p = int(dataset_split[7])
            r = int(dataset_split[8])
            data_10.append(ay)
        
            average_all = (average_all*current_num + ay)/(current_num+1)
            if current_num ==9:
                average_10_data = average_all
            elif current_num >=10:
                average_10_data = (average_10_data*10 - data_10[0] + data_10[10])/10
                data_10.pop(0)
            current_num = current_num + 1
            final_data = 0 if current_num < 9  else average_10_data - average_all if abs(average_10_data - average_all)>=10000 else 0 
            #print(final_data)
        
            if(final_data < 0 and first_negative and (datetime.now()-base).total_seconds() >=1.3):
                hit_time = hit_time + 1
                first_negative = False
                already_count = False
                print("get signal")
            if(final_data >=0 and first_negative == False and already_count == False):
                base = datetime.now()
                already_count = True
                first_negative = True
            
        how_many_time_hit.set(f"{hit_time}")

        
def timedelta_update():
    print("go in timedelta_update")
    global average_all
    global average_10_data
    global counter
    global current_num
    global hit_time
    global already_count
    global data_10
    global first_negative
    global base
    global how_many_time_hit
    global quit 
    
    global reaction
    global whole_movement
    
    global reaction_value   #(integer)
    global wait_time        #(integer)how long time will user wait to hit again
    global can_hit_or_not   #(stringvar)show on screen that told user hit
    global start_ran        #(datetime)what is the current time that use uniform to get wait's value
    global trigger_head_st  #(datetime)time that can_hit_or_not show "hit" on the screen
    global whole_move_value #(integer)
    global valid_start      #(boolean)told the program start to sensor final_data<0 case
    
    global ra
    
    print("eee:" + f"{quit}")
    while not quit:
        try:
            data_1 = arduino.readline().decode('unicode_escape').strip()  #data_1:string
            counter = counter + 1
            now_time = datetime.now()
        except:
            print("wwwww")
            return 
        #print("www:" + f"{counter}" + "qqqq:" + f"{quit}")
        
        if counter>=30:
            dataset_split = data_1.split(',')   #dataset_split: list
            ax = int(dataset_split[0])
            ay = int(dataset_split[1])   #what we need
            az = int(dataset_split[2])
            gx = int(dataset_split[3])
            gy = int(dataset_split[4])
            gz = int(dataset_split[5])
            y = int(dataset_split[6])
            p = int(dataset_split[7])
            r = int(dataset_split[8])
            data_10.append(ay)
        
            average_all = (average_all*current_num + ay)/(current_num+1)
            if current_num ==9:
                average_10_data = average_all
            elif current_num >=10:
                average_10_data = (average_10_data*10 - data_10[0] + data_10[10])/10
                data_10.pop(0)
            current_num = current_num + 1
            final_data = 0 if current_num < 9  else average_10_data - average_all if abs(average_10_data - average_all)>=10000 else 0 
            #print(final_data)
            
            
            if(wait_time == 0 and valid_start == False ):
                print(type(ra))
                wait_time = ra.uniform(7,9)
                print( "wwww:" + f"{wait_time}" )
                start_ran = datetime.now()
                
            if((datetime.now() - start_ran).total_seconds() >= wait_time and wait_time!=0):
                wait_time = 0
                trigger_head_st = datetime.now()   #時間起始點
                valid_start = True                 #開始接收出拳資訊
                can_hit_or_not.set("hit ■")
                whole_movement.set("0")
                reaction.set("0")
                
            #print(f"{trigger_head_st}",f"{(datetime.now()-trigger_head_st).total_seconds()}" , f"{valid_start}")
            
            if((datetime.now()-trigger_head_st).total_seconds()>=3 and valid_start):
                print("user don't hit")
                reaction.set("why don't you hit,bad")
                whole_movement.set("why don't you hit,bad")
                can_hit_or_not.set("hit ▢")
                valid_start = False
        
            if(final_data < 0 and first_negative and valid_start and(datetime.now()-base).total_seconds() >= 3 ):
                hit_time = hit_time + 1
                reaction_value = (datetime.now()-trigger_head_st).total_seconds()
                first_negative = False
                already_count = False
                valid_start = False
                print("get signal")
                can_hit_or_not.set("hit ▢")
                if (reaction_value-0.1)<0.15:
                    reaction.set(f"測試中別亂動")
                else:
                    reaction.set(f"{(reaction_value-0.1):.4f}")
                
            if(final_data < 0 and first_negative and (datetime.now()-base).total_seconds() < 3): #動作未完成，要更新動作時間
                whole_move_val = (datetime.now()-trigger_head_st).total_seconds()
                whole_movement.set(f"{(whole_move_val+0.1-(reaction_value)):.4f}")
            
                
            if(final_data >=0 and first_negative == False and already_count == False):
                base = datetime.now()
                already_count = True
                first_negative = True
                whole_move_val = (datetime.now()-trigger_head_st).total_seconds()
                whole_movement.set(f"{(whole_move_val+0.1-(reaction_value)):.4f}")
                

def mod1():  #出拳次數測量
    global how_many_time_hit
    global quit
    global average_all
    global average_10_data
    global counter
    global current_num
    global hit_time
    global already_count
    global data_10
    global first_negative
    global base
    global arduino
    def close_handler():
        global root
        global how_many_time_hit
        global quit
        global average_all
        global average_10_data
        global counter
        global current_num
        global hit_time
        global already_count
        global data_10
        global first_negative
        global base
        global arduino
        root.attributes('-disabled',0)
        root_1.destroy()
        how_many_time_hit.set("0")
        average_all = 0      #所有資料的平均
        average_10_data = 0  #包含自身共前10筆資料
        counter = 0             
        current_num = 0         # current valid numbers of data
        hit_time = 0            # how many time 
        already_count = True   # hit plus or not
        data_10 = []  #store 10-11 data
        base = datetime.now()
        first_negative = True  #假如現在有個data，他是first_negative嗎?
        arduino.close()
        quit = True
        print(quit)
        print("close"+f"{quit}")
        print("quit mod1")
        
    print("go in mod1")
    print("before"+f"{quit}")
    quit = False
    print("after"+f"{quit}")
    root_1 = tkinter.Toplevel()
    root.attributes('-disabled',1)
    f_1 = tkinter.Frame(root_1)
    label1 = tkinter.Label(f_1,borderwidth = 4,width = 20,relief="flat",text="出拳次數",font=("思源黑體",60))
    label2 = tkinter.Label(f_1,borderwidth = 4,width = 20,relief="flat",textvariable = how_many_time_hit,font=("思源黑體",60))
    f_1.grid(row=0,column=0)
    label1.grid()
    label2.grid()
    root_1.protocol("WM_DELETE_WINDOW",close_handler)
    arduino = serial.Serial('COM3', 115200, timeout = None)
    th = threading.Thread(target=lambda: hit_update())
    th.start()
    
    root_1.mainloop()
    
    quit = True
    
    
def mod2():
    global how_many_time_hit
    global quit
    global average_all
    global average_10_data
    global counter
    global current_num
    global hit_time
    global already_count
    global data_10
    global first_negative
    global base
    global arduino
    global reaction
    global whole_movement
    
    global reaction_value   #(integer)
    global wait_time        #(integer)how long time will user wait to hit again
    global can_hit_or_not   #(stringvar)show on screen that told user hit
    global start_ran        #(datetime)what is the current time that use uniform to get wait's value
    global trigger_head_st  #(datetime)time that can_hit_or_not show "hit" on the screen
    global whole_move_value #(integer)
    global valid_start      #(boolean)told the program start to sensor final_data<0 case
    
    def close_handler():
        global root
        global how_many_time_hit
        global quit
        global average_all
        global average_10_data
        global counter
        global current_num
        global hit_time
        global already_count
        global data_10
        global first_negative
        global base
        global arduino
        global reaction
        global whole_movement
    
        global reaction_value   #(integer)
        global wait_time        #(integer)how long time will user wait to hit again
        global can_hit_or_not   #(stringvar)show on screen that told user hit
        global start_ran        #(datetime)what is the current time that use uniform to get wait's value
        global trigger_head_st  #(datetime)time that can_hit_or_not show "hit" on the screen
        global whole_move_value #(integer)
        global valid_start      #(boolean)told the program start to sensor final_data<0 case
        root.attributes('-disabled',0)
        root_2.destroy()
        reaction.set("0")
        whole_movement.set("0")
        how_many_time_hit.set("0")
        average_all = 0      #所有資料的平均
        average_10_data = 0  #包含自身共前10筆資料
        counter = 0             
        current_num = 0         # current valid numbers of data
        hit_time = 0            # how many time 
        already_count = True   # hit plus or not
        data_10 = []  #store 10-11 data
        base = datetime.now()
        first_negative = True  #假如現在有個data，他是first_negative嗎?
        
        reaction.set("0")
        whole_movement.set("0")
        can_hit_or_not.set("hit ▢")

        reaction_value = 0
        wait_time = 0
        start_ran = datetime.now()
        trigger_head_st = datetime.now()
        whole_move_value = 0
        valid_start = False
        
        arduino.close()
        quit = True
        print("quit mod2")
        
    print("go into mod2")
    quit = False
    root_2 = tkinter.Toplevel()
    root.attributes('-disabled',1)
    f_2 = tkinter.Frame(root_2)
    label1 = tkinter.Label(f_2,borderwidth = 4,width = 20,relief="flat",text="反應時間",font=("思源黑體",60))
    label2 = tkinter.Label(f_2,borderwidth = 4,width = 20,relief="flat",text="動作時間",font=("思源黑體",60))    
    label3 = tkinter.Label(f_2,borderwidth = 4,width = 20,relief="flat",textvariable=reaction,font=("思源黑體",60))
    label4 = tkinter.Label(f_2,borderwidth = 4,width = 20,relief="flat",textvariable=whole_movement,font=("思源黑體",60))
    label5 = tkinter.Label(f_2,borderwidth = 4,width = 20,relief="flat",textvariable=can_hit_or_not,font=("思源黑體",60))
    f_2.grid()
    label1.grid()
    label3.grid()
    label2.grid()
    label4.grid()
    label5.grid()
    root_2.protocol("WM_DELETE_WINDOW",close_handler)
    
    arduino = serial.Serial('COM3', 115200, timeout = None)
    th = threading.Thread(target=timedelta_update)
    th.start()
    
    root_2.mainloop()   
    
    quit = True
    

root = tkinter.Tk()
f = tkinter.Frame(root)
how_many_time_hit = tkinter.StringVar()
whole_movement = tkinter.StringVar()
reaction = tkinter.StringVar()
can_hit_or_not = tkinter.StringVar()
how_many_time_hit.set("0")
whole_movement.set("0")
reaction.set("0")
can_hit_or_not.set("hit ▢")
label1 = tkinter.Label(f,borderwidth = 4,width = 40,relief="flat",text="final project: karate practice",font=("思源黑體",30))
label2 = tkinter.Label(f,borderwidth = 4,width = 20,relief="flat",text="110060021 曾偉博")
label3 = tkinter.Label(f,borderwidth = 4,width = 20,relief="flat",text="110060035 黃振寧")
label4 = tkinter.Label(f,borderwidth = 4,width = 20,relief="flat",text=" ",font=("思源黑體",10))
label5 = tkinter.Label(f,borderwidth = 4,width = 20,relief="flat",text=" ",font=("思源黑體",10))
label6 = tkinter.Label(f,borderwidth = 4,width = 20,relief="flat",text=" ",font=("思源黑體",10))
label7 = tkinter.Label(f,borderwidth = 4,width = 20,relief="flat",text=" ",font=("思源黑體",10))
button1 = tkinter.Button(f,width=20,text="出拳次數測量",command = mod1,font=("思源黑體",15))
button2 = tkinter.Button(f,width=20,text="反應時間、動作時間測量",command = mod2,font=("思源黑體",15))
button3 = tkinter.Button(f,width=20,text="quit",command = root.destroy,font=("思源黑體",15))

f.grid()
label1.grid(row=0,column=0,columnspan=3,sticky=tkinter.E+tkinter.W)
label2.grid(row=1,column=1)
label3.grid(row=2,column=1)
label4.grid(row=3,column=1,rowspan=4)
label5.grid(row=7,column=1,rowspan=4)
label6.grid(row=11,column=1,rowspan=4)
label7.grid(row=15,column=1,rowspan=4)
button1.grid(row=20,column=0,padx=10, pady=10,sticky=tkinter.E)
button2.grid(row=20,column=1,padx=10, pady=10)
button3.grid(row=20,column=2,padx=10, pady=10,sticky=tkinter.W)

root.mainloop()   #when press button or other event,update again

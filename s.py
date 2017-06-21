#!/usr/bin/python
#new2
#new2
import os;
import commands;


dump_file=open("dump.txt");
stack_file=open("stack.txt");

def find_key(line,key):
    "find sp vale"
    str_key = key + ": ";
    sp = line.split(str_key);
    sp2 = sp[1].split(',');
    return sp2[0];

#g_sp = find_sp('A5FP: 423F17AC, IP: 00000000, SP: 42768688, LR: 42287270, PC: 00000002, PSR: 60000133');
#print g_sp;

for line in dump_file:
    pos = line.find("SP:");
    if pos >=0:
        g_sp = find_key(line, "SP");
        print "SP:", g_sp; 
        g_pc = find_key(line, "PC");
        print "PC", g_pc;

        g_lr = find_key(line, "LR");
        print "LR:", g_lr;
        break;

def find_stack(line, sp):
    "find stack line by line "
    base = line[0:8];
    base_num = int(base, 16);
    sp_num = int(sp, 16);
    #print "base_num:" ,base_num;
    
    if base_num > sp_num:
        return 0;
    
    stack_len = line[22:30];
    stack_len_num = int(stack_len, 16);
    #print stack_len ;
    if (base_num+stack_len_num) >= sp_num:
        #print line;
        return 1;
    return 0;

#find_stack("42726f48 l     O .bss	00013880 _ZL8smsstack", g_sp); 

for line in stack_file:
    ret = find_stack(line, g_sp);
    if ret == 1:
        print "crash stack:", line[31:] ;
        break;
if ret ==0:
    print "does not find stack";


code_file = open("code.S");

def find_func_by_addr(addr):
    for line in code_file:
        pos = line.find('<');
        if pos >= 0:
            length = len(line);
            func_name_temp = line[pos:length-1];
            pos = func_name_temp.find(':');
            if pos > 0 :
                func_name = func_name_temp;
            #print func_name;
            continue;

        value  = line[0:8];
        if addr == value :
            print "find func :", func_name;
            return func_name;

    print "find not func";    
    return '';

find_func_by_addr(g_pc);
find_func_by_addr(g_lr);


code_file.close();   
dump_file.close();
stack_file.close();

#print "exit";









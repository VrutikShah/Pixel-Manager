#!/usr/bin/python3.8
import curses,time,os
import getpass,sys

os.chdir(sys.argv[1])
menu = os.listdir()

file = "It is a File"

def empty_right(stdscr):
    p,w = stdscr.getmaxyx()
    per10screen = w//5
    per = " "*(w//5)
    stdscr.attron(curses.color_pair(3))
    for i in range(1,p):
        stdscr.addstr(i,w//5+1," "*(4*w//5-2))

def print_folder(stdscr,row):
    try:
        h = list(os.listdir(row))
        p,w = stdscr.getmaxyx()
        per10screen = w//5
        empty_right(stdscr)
        for i in range(len(h)):
            stdscr.attron(curses.color_pair(3))
            if len(h[i])<per10screen:
                l = h[i]+" "*(per10screen-len(row))
            else:
                l = h[i][:per10screen]
            x = w//5+1
            y = i+1
            stdscr.addstr(y,x,l)
    except:
        pass


def print_menu(stdscr,listings,n,this):
    global menu
    # stdscr.clear()
    h,w = stdscr.getmaxyx()
    per10screen = w//5
    maxi = 0
    per = " "*(w//5)
    for i in range(1,h-1):
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(i,0,per)
    stdscr.attroff(curses.color_pair(2))
    curses.init_pair(4, curses.COLOR_WHITE, 2)
    curses.init_pair(5, 3,17)
    stdscr.attron(curses.color_pair(5))
    stdscr.addstr(0,0," "*w)
    if listings[0]:
        print_folder(stdscr,menu[0])
    else:
        empty_right(stdscr)
        stdscr.addstr(h//2,w//2-len(file)//2,file,curses.color_pair(3))
    stdscr.attron(curses.color_pair(4))
    stdscr.addstr(h-1,0," "*(w-1))
    stdscr.addstr(h-1,w//2-len(menu[0])//2,menu[0])
    for idx, row in enumerate(menu):
        if (idx==0 and n==0) or this==row:
            stdscr.attron(curses.color_pair(1))
            if len(row)<per10screen:
                i = row+" "*(per10screen-len(row))
            else:
                i = row[:per10screen]
            x = 0
            y = idx+1
            stdscr.addstr(y,x,i)
            stdscr.attroff(curses.color_pair(1))
        else:
            if idx>=h-2:
                break
            stdscr.attron(curses.color_pair(2))
            if len(row)<per10screen:
                i = row+" "*(per10screen-len(row))
            else:
                i = row[:per10screen]
            x = 0
            y = idx+1
            stdscr.addstr(y,x,i)
    stdscr.refresh()

def scrolldown(stdscr,cur_row):
    global menu
    h,w = stdscr.getmaxyx()
    per10screen = w//5
    maxi = 0
    per = " "*(w//5)
    stdscr.attron(curses.color_pair(2))
    for idx in range(cur_row-h+2,cur_row):
        if len(menu[idx])<per10screen:
            i = menu[idx]+" "*(per10screen-len(menu[idx]))
        else:
            i = menu[idx][:per10screen]
        if idx==cur_row-1:
            stdscr.attron(curses.color_pair(1))
            if len(menu[idx])<per10screen:
                i = menu[idx]+" "*(per10screen-len(menu[idx]))
            else:
                i = menu[idx][:per10screen]
            x = 0
            y = idx+1-cur_row+h-2
            stdscr.addstr(y,x,i)
            stdscr.attroff(curses.color_pair(1))
            stdscr.attron(curses.color_pair(4))
            stdscr.addstr(h-1,0," "*(w-1))
            stdscr.addstr(h-1,w//2-len(menu[cur_row-1])//2,menu[cur_row-1])
        else:
            x = 0
            y = idx+1-cur_row+h-2
            stdscr.addstr(y,x,i)
    stdscr.refresh()
    # exit()

def main(stdscr):
    global menu
    curses.curs_set(0)
    h,w = stdscr.getmaxyx()
    listings = []
    for i in menu:
        listings.append(os.path.isdir(i))
    per10screen = w//5
    curses.init_pair(1, curses.COLOR_WHITE, 34)
    curses.init_pair(2, curses.COLOR_WHITE, 18)
    cur_row = 1
    maxi = 0
    for i in menu:
        maxi = max(maxi,len(i))
    l = len(menu)
    curses.init_pair(3, 3, 27)
    stdscr.bkgd(' ', curses.color_pair(3)|curses.A_BOLD)
    path = getpass.getuser()+":"+os.getcwd()+"$"
    print_menu(stdscr,listings,0,"")
    stdscr.addstr(0,w//2-len(path)//2,path,curses.color_pair(5) + curses.A_BOLD)
    while 1:
        key = stdscr.getch()
        if key==curses.KEY_DOWN:
            if cur_row==len(menu):
                continue
            if cur_row>=l or cur_row>h-3:
                if listings[cur_row]:
                    print_folder(stdscr,menu[cur_row])
                else:
                    empty_right(stdscr)
                    stdscr.addstr(h//2,w//2-len(file)//2,file,curses.color_pair(3))
                cur_row+=1
                scrolldown(stdscr,cur_row)
                continue
            if len(menu[cur_row-1])<per10screen:
                x = menu[cur_row-1]+" "*((per10screen-len(menu[cur_row-1])))
            else:
                x = menu[cur_row-1][:per10screen]
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(cur_row,0,x)
            stdscr.attroff(curses.color_pair(2))
            if listings[cur_row]:
                print_folder(stdscr,menu[cur_row])
            else:
                empty_right(stdscr)
                stdscr.addstr(h//2,w//2-len(file)//2,file,curses.color_pair(3))
            cur_row+=1
            if len(menu[cur_row-1])<per10screen:
                x = menu[cur_row-1]+" "*((per10screen-len(menu[cur_row-1])))
            else:
                x = menu[cur_row-1][:per10screen]
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(cur_row,0,x)
            stdscr.attroff(curses.color_pair(1))
            if cur_row<=l:
                stdscr.attron(curses.color_pair(4))
                stdscr.addstr(h-1,0," "*(w-1))
                stdscr.addstr(h-1,w//2-len(menu[cur_row-1])//2,menu[cur_row-1])
        elif key==curses.KEY_UP:
            if cur_row==1:
                    continue
            if cur_row>=h-1:
                cur_row-=1
                if listings[cur_row-1]:
                    print_folder(stdscr,menu[cur_row-1])
                else:
                    empty_right(stdscr)
                    stdscr.addstr(h//2,w//2-len(file)//2,file,curses.color_pair(3))
                scrolldown(stdscr,cur_row)
                continue
            if len(menu[cur_row-1])<per10screen:
                x = menu[cur_row-1]+" "*((per10screen-len(menu[cur_row-1])))
            else:
                x = menu[cur_row-1][:per10screen]
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(cur_row,0,x)
            stdscr.attroff(curses.color_pair(2))
            cur_row-=1
            if listings[cur_row-1]:
                print_folder(stdscr,menu[cur_row-1])
            else:
                empty_right(stdscr)
                stdscr.addstr(h//2,w//2-len(file)//2,file,curses.color_pair(3))
            if len(menu[cur_row-1])<per10screen:
                x = menu[cur_row-1]+" "*((per10screen-len(menu[cur_row-1])))
            else:
                x = menu[cur_row-1][:per10screen]
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(cur_row,0,x)
            stdscr.attroff(curses.color_pair(1))
            stdscr.attron(curses.color_pair(4))
            stdscr.addstr(h-1,0," "*(w-1))
            stdscr.addstr(h-1,w//2-len(menu[cur_row-1])//2,menu[cur_row-1])
        elif key==curses.KEY_LEFT:
            old_menu = path.split("/")[-1][:-1]
            os.chdir("..")
            path = getpass.getuser()+":"+os.getcwd()+"$"
            menu = os.listdir()
            cur_row = menu.index(old_menu)+1
            l = len(menu)
            listings = []
            for i in menu:
                listings.append(os.path.isdir(i))
            print_menu(stdscr,listings,1,old_menu)
            print_folder(stdscr,old_menu)
            if cur_row<=l:
                stdscr.attron(curses.color_pair(4))
                stdscr.addstr(h-1,0," "*(w-1))
                stdscr.addstr(h-1,w//2-len(menu[cur_row-1])//2,menu[cur_row-1])
            stdscr.addstr(0,w//2-len(path)//2,path,curses.color_pair(5))
        elif key==curses.KEY_ENTER or key==10 or key==13 or key==curses.KEY_RIGHT:
            if not os.path.isdir(menu[cur_row-1]):
                continue
            old_row = cur_row
            os.chdir(menu[cur_row-1])
            cur_row=1
            menu = os.listdir()
            if len(menu)==0:
                os.chdir("..")
                cur_row=old_row
                menu = os.listdir()
                continue
            path = getpass.getuser()+":"+os.getcwd()+"$"
            l = len(menu)
            listings = []
            for i in menu:
                listings.append(os.path.isdir(i))
            print_menu(stdscr,listings,0,"")
            stdscr.addstr(0,w//2-len(path)//2,path,curses.color_pair(5))
        stdscr.refresh()
    curses.curs_set(0)
curses.wrapper(main)
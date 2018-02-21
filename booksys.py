#!/usr/bin/python
# -*- coding: UTF-8 -*-
import mysql.connector
import sys, os
import time
import datetime
from tkinter import *
from tkinter.messagebox import *
import tkinter
root = Tk()
root.title("图书管理系统")



#这是一个数据库类，对各种操作进行统一分类
class Libop:
    user = 'root'
    pwd = '1234'
    host = 'localhost'
    db = 'lib'
    #data_file = 'mysql-test.dat'

    def __init__(self):
        #print("连接")
        try:
            self.lib = mysql.connector.connect(user=Libop.user, password=Libop.pwd, host=Libop.host,database=Libop.db)

            self.cursor = self.lib.cursor()
            print("Connect successfully")
        except mysql.connector.Error as err:
            print("WTF! initial wrong")
            print("Error: {}".format(err.msg))
            sys.exit()

    def select(self,str):
        try:
            self.cursor.execute(str)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print("WTF! select wrong")
            print("Error:{}".format(err.msg))
            print(str)
            showinfo("ERROR","Please input the parameter correctly")
    def update(self,str):
        try:
            self.cursor.execute(str)
            self.lib.commit()
            return 1
        except mysql.connector.Error as err:
            print("WTF! update wrong")
            print("Error:{}".format(err.msg))
            return 0
    def delete(self,str):
        try:
            self.cursor.execute(str)
            self.lib.commit()
        except mysql.connector.Error as err:
            print("WTF! delete wrong")
            print("Error:{}".format(err.msg))
    def insert(self,str):
        try:
            self.cursor.execute(str)
            self.lib.commit()
            return 1
        except mysql.connector.Error as err:
            print("WTF! insert wrong")
            print("Error:{}".format(err.msg))
            return 0
LIB = Libop()




str1=str2=''
book_type=name=year=publisher=writer=price1=price2=order=cardid=''
#登录按钮的触发事件

def login():
    str1 = ide.get()
    str2 = pwde.get()
    num = 0
    # print(str1,str2)
    # print (curs)
    curs = LIB.select("select manage_id,pswd from managers where manage_id='{}' and pswd='{}'".format(str1, str2))
    #登录检验
    for data in curs:
        num = num + 1
        #print ( data)

    if (num != 0):
        showinfo('通知', '登录成功')
        #登录成功之后出现的书的ID和人的ID两个label
        label_book_id = Label(root, text='书号:').grid(row=0, column=4, sticky=W)
        label_card_id = Label(root, text='卡号:').grid(row=1, column=4, sticky=W)

        entry_book_id = Entry(root)
        entry_book_id.grid(row=0, column=5, sticky=W)

        entry_card_id = Entry(root)
        entry_card_id.grid(row=1, column=5, sticky=W)

        entry_cardid = Entry(root)
        entry_cardid.grid(row=5, column=0, sticky=W)

        entry_book = Entry(root)
        entry_book.grid(row=7, column=0, sticky=W)

        entry_find = Entry(root)
        entry_find.grid(row= 8,column =0,sticky =W)



        # buttons
        button_insert = Button(root, text='添加or修改图书', command=inbook)
        button_insert.grid(row=6, column=4, sticky=W)
        #借书
        button_return = Button(root, text='借书')
        button_return.bind("<ButtonRelease-1>", lambda z: call_rent(entry_book_id, entry_card_id, str1))
        button_return.grid(row=0, column=6, sticky=E)

        #删除用户
        button_delete = Button(root, text='删除用户')
        button_delete.bind("<ButtonRelease-1>", lambda j: deletecard(entry_cardid))
        button_delete.grid(row=5, column=1, sticky=W)

        #增加用户
        button_add = Button(root, text='添加用户', command=addwindow)
        button_add.grid(row=5, column=3, sticky=W)

        button_delete_book = Button(root, text='删除图书')
        button_delete_book.bind("<ButtonRelease-1>", lambda z: deletebook(entry_book))
        button_delete_book.grid(row=7, column=1, sticky=W)

        button_see=Button(root,text='全部图书')
        button_see.bind("<ButtonRelease-1>", lambda b: seebook())
        button_see.grid(row=6,column=3)

        button_see_login = Button(root, text='全部用户')
        button_see_login.bind("<ButtonRelease-1>", lambda c: seelogin())
        button_see_login.grid(row=7, column=3)

        button_see_record = Button(root, text='借阅总览')
        button_see_record.bind("<ButtonRelease-1>", lambda c: see_record())
        button_see_record.grid(row=7, column=4, sticky= W)

        button_fine_record = Button(root, text='逾期提醒')
        button_fine_record.bind("<ButtonRelease-1>", lambda cd: fine_record())
        button_fine_record.grid(row=5, column=4, sticky=W)

        button_find_login = Button(root, text='用户搜索')
        button_find_login.bind("<ButtonRelease-1>", lambda f: find_login(entry_find))
        button_find_login.grid(row=8, column=1, sticky=W)










        display_card_id = Entry(root)
        display_card_id.grid(row=6, column=0, sticky=W)
        button_display = Button(root, text='用户借书情况查询')
        button_display.bind("<ButtonRelease-1>", lambda y: display_rent(display_card_id))
        button_display.grid(row=6, column=1, sticky=W)

        #还书
        button_rent = Button(root, text='还书')
        button_rent.bind("<ButtonRelease-1>", lambda l: call_return(entry_book_id, entry_card_id))
        button_rent.grid(row=1, column=6, sticky=E)



            #entry_cardid = Entry(root)
    else:
        showerror("登录失败","账号 or 密码不对")
        #entry_cardid.grid(row=5, column=0, sticky=W)
def see_record():
    select = "select  card_id ,bookid from record where still = 1 "
    curs = LIB.select(select)
    top = Toplevel()
    text = Text(top)
    still = 0
    for i in curs:
        # print(i)
        still += 1
    text.insert(INSERT, "借出数量：{}\n".format(still))
    text.insert(INSERT, "卡号\t书号\n")

    # for a in i:
    # print (a)

    for (card_id, bookid) in curs:
        text.insert(INSERT,
                    "{}\t{}\n".format(card_id,bookid ))
    text.pack()

def find_login(entry_find):
    str1 = entry_find.get()
    select = "select name ,pw from lib_card where card_id='{}'".format(str1)
    curs = LIB.select(select)
    top = Toplevel(root)
    text = Text(top)
    num = 0
    text.insert(INSERT, "姓名\t密码\n")
    for i in curs:
        num += 1

    if num > 0:

        for (name, pw) in curs:
            text.insert(INSERT, "{}\t{}\n".format(name, pw))

    text.pack()


def fine_record():
    select= "SELECT  card_id,bookid from record where return_time < CURDATE() and still =1"
    curs = LIB.select(select)
    #print(curs)
    top = Toplevel(root)
    text = Text(top)
    num=0
    text.insert(INSERT, "卡号\t书号\n")
    for i in curs:
        num+=1

    if num >0:




            for (card_id,bookid) in curs:
                text.insert(INSERT, "{}\t{}\n".format(card_id,bookid))

    text.pack()

def alterbook():
    pass



def inbook():
    top = Toplevel(root)

    label_bookid = Label(top, text='书号:').grid(row=0, column=0, sticky=W)
    label_type = Label(top, text='类型:').grid(row=1, column=0, sticky=W)
    label_bookname = Label(top, text='书名:').grid(row=2, column=0, sticky=W)
    label_publisher = Label(top, text='出版社:').grid(row=3, column=0, sticky=W)
    label_year = Label(top, text='出版时间:').grid(row=4, column=0, sticky=W)
    label_writer = Label(top, text='作者:').grid(row=5, column=0, sticky=W)
    label_price = Label(top, text='价格:').grid(row=6, column=0, sticky=W)
    label_total= Label(top, text='总量:').grid(row=7, column=0, sticky=W)
    label_stock = Label(top, text='库存:').grid(row=8, column=0, sticky=W)

    # 上面的是是个label
    entry_bookid = Entry(top)
    entry_bookid.grid(row=0, column=1, sticky=W)

    entry_type = Entry(top)
    entry_type.grid(row=1, column=1, sticky=W)

    entry_bookname = Entry(top)
    entry_bookname.grid(row=2, column=1, sticky=W)

    entry_publilsher = Entry(top)
    entry_publilsher.grid(row=3, column=1, sticky=W)

    entry_year = Entry(top)
    entry_year.grid(row=4, column=1, sticky=W)

    entry_writer = Entry(top)
    entry_writer.grid(row=5, column=1, sticky=W)

    entry_price = Entry(top)
    entry_price.grid(row=6, column=1, sticky=W)

    entry_total= Entry(top)
    entry_total.grid(row=7, column=1, sticky=W)

    entry_stock = Entry(top)
    entry_stock.grid(row=8, column=1, sticky=W)


    button_constructe = Button(top, text='添加')
    button_constructe.bind("<ButtonRelease-1>", lambda v: addbook(entry_bookid,entry_type,entry_bookname,entry_publilsher,entry_year, entry_writer,entry_price,entry_total,entry_stock))
    button_constructe.grid(row=9,column =1)

    button_alterbookmess = Button(top, text='修改')
    button_alterbookmess.bind("<ButtonRelease-1>",lambda h: alterbookmess(entry_bookid, entry_type, entry_bookname, entry_publilsher, entry_year,entry_writer, entry_price, entry_total, entry_stock))
    button_alterbookmess.place(x = 70,y= 208)


def alterbookmess(entry_bookid, entry_type, entry_bookname, entry_publilsher, entry_year,entry_writer, entry_price, entry_total, entry_stock):
    bid = entry_bookid.get()
    btype = entry_type.get()
    bname = entry_bookname.get()
    bpublisher = entry_publilsher.get()
    byear = entry_year.get()
    bwriter = entry_writer.get()
    bprice = entry_price.get()
    btotal = entry_total.get()
    bstock = entry_stock.get()
    #update 表名称 set 列名称=新值 where 更新条件;
    if   (checkbook(bid)):
        showinfo('通知','更新成功')
        if btype !='':
            update = "update book set t='{}' where bookid = '{}' ".format(btype,bid)
            a = LIB.update(update)
        if bname != '':
            update= "update book set name='{}' where bookid = '{}' ".format(bname,bid)
            b= LIB.update(update)
        if bpublisher != '':
            update="update book set publisher='{}' where bookid = '{}' ".format(bpublisher,bid)
            c=LIB.update(update)

        if byear != '':
            update="update book set year='{}' where bookid = '{}' ".format(byear,bid)
            d = LIB.update(update)
        if bwriter != '':
            update ="update book set writer='{}' where bookid = '{}' ".format(bwriter,bid)
            e = LIB.update(update)
        if bprice != '':
            update="update book set price='{}' where bookid = '{}' ".format(bprice,bid)
            f = LIB.update(update)
        if btotal != '':
            update ="update book set total='{}' where bookid = '{}' ".format(btotal,bid)
            g = LIB.update(update)



        if bstock != '':
            update ="update book set stock='{}' where bookid = '{}' ".format(bstock,bid)
            h = LIB.update(update)



    else :
        showwarning("通知","此书不存在，请注意")


def addbook(entry_bookid,entry_type,entry_bookname,entry_publilsher,entry_year, entry_writer,entry_price,entry_total,entry_stock):
    bid = entry_bookid.get()
    btype =entry_type.get()
    bname = entry_bookname.get()
    bpublisher =entry_publilsher.get()
    byear = entry_year.get()
    bwriter = entry_writer.get()
    bprice =entry_price.get()
    btotal = entry_total.get()
    bstock = entry_stock.get()
    #print( bid,btype,bname,bpublisher,byear,bwriter,bprice,btotal,bstock)
    if   (checkbook(bid)):
        showinfo('error', '此书号已经存在，请更换')
        return 0

    if bstock == ''or btotal == '':
        showwarning("错误","库存或剩余不能为0")


    if (int(bstock) > int(btotal)) or (int(bprice) < 0):
        showerror('错误!', '库存或价格低于 0!')

    t = LIB.insert("insert into book values('{}','{}','{}','{}',{},'{}',{},{},{})".format(bid,btype,bname,bpublisher,byear,bwriter,bprice,btotal,bstock))
    #print(t)
    if (t == 0):
        showerror('错误', '书号 {}， 其他部分不能为空'.format(bid))
    else:
        showinfo('通知', '添加成功')



def call_rent(en1, en2, brokerage):
    st1 = en1.get()#书号
    st2 = en2.get()#卡号
    st3 = brokerage#管理员
    #print(st1)
    #print(st2)
    #print(st3)
    #这个函数是进行两个BOOkid和cardID的传递
    rent(st1, st2, st3)
    #挑转到rent函数

def rent(BookID, cardid, st3):
    if  not (checkbook(BookID)):
        showwarning('error', '此书号不存在')
        return 0

   #检查有没有这张卡
    if not (checkcard(cardid)):
        showinfo('error', '没有此账号')
        return 0

    select = "select stock from book where bookid='{}'".format(BookID)
    stocks = LIB.select(select)
    #print(stocks)

    stock2 = stocks[0]
    stock3= int(stock2[0])
    #print(type(stock3))
    #print(stock3 )
    num =0
    if (stock3 > 0):
        update = "update book set stock=stock-1 where bookid='{}'".format(BookID)
        flag = LIB.update(update)
        #print(flag) 更新成功为1

        if flag:
            num+=1

            #insert = "insert into record values('',''{}','{}',CURDATE(),DATE_ADD(CURDATE(),INTERVAL 1 MONTH),'{}',1)".format(
                #cardid, BookID, brokerage)
            #INSERT INTO animals (name) VALUES
                    #('dog'),('cat'),('penguin'),
                    #('lax'),('whale'),('ostrich');


            insert = "insert into record  values(NULL,'{}','{}',CURDATE(),DATE_ADD(CURDATE(),INTERVAL 1 MONTH),'{}',1)".format(cardid, BookID, st3)
            LIB.insert(insert)
            showinfo('ok', '借书成功')
        else:
            showerror('借书失败', "全部借出")
    else:
        select = "select return_time from record where bookid='{}' and return_time >= all(select return_time from record where bookid='{}')".format(
            BookID, BookID)
        date = LIB.select(select)
        # date=curs.fetchall()
        date = str(date)
        showinfo('无书可借',"没有更多的书可借，还书时间是:{}-{}-{}").format(date)



    return 1

def checkcard(cardid):
    select="select card_id from lib_card where card_id='{}'".format(cardid)
    curs=LIB.select(select)
    num =0
    for data in curs:
        num = num + 1
        #print ( data)

    if (num != 0):
        return 1
    else:
        return 0
    
def checkbook(BookId):
    select = "select bookid from book where bookid='{}'".format(BookId)
    curs = LIB.select(select)
    #print(curs)
    num = 0
    for data in curs:
        num = num + 1
        #print(data)
        if (num != 0):
             return 1
        else:
             return 0

def deletecard(card):
    cardid=card.get()
    #print(cardid)
    if not (checkcard(cardid)):
        showerror('error',"无此账号")
        return 0
    select="select record_id from record where card_id='{}' and still=1".format(cardid)
    curs = LIB.select(select)
    #print(curs)
    for record_id in curs:
        showinfo('error',"有书没还，请还再借")
        return 0
    delete="delete from lib_card where card_id='{}'".format(cardid)
    LIB.delete(delete)
    showinfo('ok','成功删除')
    return 1

def addwindow():
    top=Toplevel(root)
    label_card_id=Label(top,text='卡号:').grid(row=0,column=0,sticky=W)
    label_name=Label(top,text='姓名:').grid(row=1,column=0,sticky=W)
    label_unit=Label(top,text='密码:').grid(row=2,column=0,sticky=W)

#上面的是是个label
    entry_card_id=Entry(top)
    entry_card_id.grid(row=0,column=1,sticky=W)

    entry_name=Entry(top)
    entry_name.grid(row=1,column=1,sticky=W)

    entry_pw=Entry(top)
    entry_pw.grid(row=2,column=1,sticky=W)


    #下面的是一个按钮，这个按钮触发addcard函数，将是个参数插入
    button_constructe=Button(top,text='确定')
    button_constructe.bind("<ButtonRelease-1>",lambda q:addcard(entry_card_id,entry_name,entry_pw))
    button_constructe.grid(row=4,column = 1)

def addcard(en1,en2,en3):
    cardid=en1.get()
    name=en2.get()
    pw=en3.get()

    select="select card_id from lib_card where card_id='{}'".format(cardid)
    #if (c_type not in ('T','S','O')):
        #showinfo('error',"NO SUCH TYPE")
        #return 0
    line=LIB.select(select)
    if (len(line)!=0):
        showinfo('失败',"已存在此账号!")
    else:
        insert="insert into lib_card values('{}','{}','{}')".format(cardid,name,pw)
        LIB.insert(insert)
        showinfo('ok','添加成功')
    return 1
def display_rent(display_card_id):
        cardid=display_card_id.get()
        #print(cardid)
        select="select card_id from lib_card where card_id='{}'".format(cardid)
        curs=LIB.select(select)
        #print(curs)
      #order_index=LIB_order.curselection()
        #if len(order_index)!=0 :
         #   order_index=order_index[0]
        #else:
         #   order_index=0;
        #orders=order[order_index]
        num = 0
        for data in curs:
            num = num + 1
            # print ( data)

        if num>0:
            select="select card_id,name from lib_card where card_id='{}'".format(cardid)
            curs=LIB.select(select)
            top=Toplevel(root)
            text=Text(top)
            for (card_id,name) in curs:
                text.insert(INSERT,"账号:{}\n".format(card_id))
                text.insert(INSERT,"姓名:{}\n".format(name))


            select="select bookid,t,name,publisher,year,writer,price from book natural join record where card_id='{}' and still=1 ".format(cardid)
            curs=LIB.select(select)

            text.insert(INSERT,"书号\t类型\t书名\t出版社\t出版时间\t\t作者\t价格\n")
            for (bookid,t,name,publisher,year,writer,price) in curs:
                text.insert(INSERT,"{}\t{}\t{}\t{}\t{}\t\t{}\t{}\n".format(bookid,t,name,publisher,year,writer,price))
            text.pack()
        else:
            showinfo('Error',"无此账号")

def call_return(en1,en2):
    st1=en1.get()
    st2=en2.get()
    back(st1,st2)

def back(BookID,cardid):
    if not(checkcard(cardid)): return 0
    select="select bookid from record where bookid='{}' and card_id='{}' and still=1".format(BookID,cardid)
    curs=LIB.select(select)
    select = "select return_time from record where  bookid={}".format(BookID)
    cur= LIB.select(select)
    #print(cur)
    re_time1=cur[0]
    re_time2=cur[0]
    re_time3 = re_time2[0]
    #print(re_time3)
    now_time = time.strftime('%Y%m%d', time.localtime(time.time()))
    # 时间加减
    #print(now_time)
    time3 = "select DATEDIFF('{}', '{}')".format(now_time, re_time3)
    cur2=LIB.select(time3)
    cur3 = cur2[0]
    #print(type(cur3))
    cur4 =cur3[0] #提取时间元组中的第一个数量，就是int格式的数字，可以用来计算罚款
    #print(cur4)
    #print(type(cur4))
    fine = cur4*0.2
    #print (fine)
    if fine > 0:
        showinfo('通知',"你需要支付超期罚款{}元".format(fine))

        insert = "insert into book_fine VALUES (null,'{}','{}')".format(cardid,fine)
        cur5= LIB.insert(insert)

    if (BookID,) in curs:
        select="select record_id from record where bookid='{}' and card_id='{}' and still=1 ".format(BookID,cardid)
        cur=LIB.select(select)
        #cur=curss.fetchall()
        for record in cur:
            recordid=str(record)
            recordid=recordid[1:]
            recordid=recordid[:-2]
            update="update record set still=0 where record_id='{}'".format(recordid)
            LIB.update(update)
            update="update book set stock=stock+1 where bookid='{}'".format(BookID)
            LIB.update(update)

            #if fine:
                ##showinfo('罚款',"你需要支付{}元罚款",format(fine))


            break
        showinfo('message',"还书成功!")


        return 1
    else:
        showinfo('error',"你没有借这本书!")
        return 1


#label_name=Label(root,text='书名').grid(row=3,sticky=W,column=0)
#label_writer=Label(root,text='作者').grid(row=3,sticky=W,column=1)


entry_name=Entry(root)
entry_name.grid(row=4,column=0,sticky=W)

#entry_writer=Entry(root)
#entry_writer.grid(row=4,column=1,sticky=W)


#order the result
def seelogin():
    select = "select card_id,name,pw from lib_card"
    curs=LIB.select(select)




    #print(curs)
    top = Toplevel(root)

    text = Text(top)
    still = 0
    for i in curs:
        # print(i)
        still += 1
    text.insert(INSERT, "全部用户数量：{}\n".format(still))
    text.insert(INSERT, "卡号\t姓名\t密码\n")

    # for a in i:
    # print (a)

    for (card_id,name,pw) in curs:
        text.insert(INSERT,
                    "{}\t{}\t{}\n".format(card_id,name,pw))
    text.pack()



def booksearch():


    bookname=entry_name.get()
    #print (bookname)
    #writer=entry_writer.get()
    select = "select bookid, name,publisher,year,writer,total,stock from book where  name='{}'".format(bookname)
    curs = LIB.select(select)
    #print(curs)
    searchresult=Toplevel(root)

    searchresult.title('搜索结果 ')
    text=Text(searchresult)
    text.insert(INSERT,"书号\t书名\t出版社\t\t出版时间\t\t作者\t总量\t剩余\n")
    text.pack()

    for (bookid, name,publisher,year,writer,total,stock) in curs:
        text.insert(INSERT,"{}\t{}\t{}\t\t{}\t\t{}\t{}\t{}\n".format(bookid, name,publisher,year,writer,total,stock))
    
def studentlogin():
    str1 = ide.get()
    str2 = pwde.get()
    num = 0
    # print(str1,str2)
    # print (curs)
    curs = LIB.select("select card_id,pw from lib_card where card_id='{}' and pw='{}'".format(str1, str2))
    # 登录检验
    for data in curs:
        num = num + 1
        # print ( data)

    if (num != 0):
        showinfo('通知', '欢迎，登录成功')
        # 登录成功之后出现的书的ID和人的ID两个label
        student_mess = Toplevel(root)
        student_mess.title('个人信息')
        student_mess.geometry('200x100')

        #Button(student_mess, text="借书查询").pack()
        #Button.bind("<ButtonRelease-1>", lambda l: borrow(str1))

        button_confirm = Button(student_mess, text='借书查询')
        button_confirm.bind("<ButtonRelease-1>", lambda x: borrow(str1))
        button_confirm.pack()

        button_alter=Button(student_mess,text= '修改密码')
        button_alter.bind("<ButtonRelease-1>", lambda y: alter(str1))
        button_alter.pack()


    else:
        showerror('错误','你的号码不存在或者密码错误')

def  alter(str1):
    top = Toplevel(root)
    label_card_id = Label(top, text='旧密码:').grid(row=0, column=0, sticky=W)
    label_name = Label(top, text='新密码:').grid(row=1, column=0, sticky=W)


    # 上面的是是个label
    entry_old = Entry(top)
    entry_old.grid(row=0, column=1, sticky=W)

    entry_new = Entry(top)
    entry_new.grid(row=1, column=1, sticky=W)

    button_pw = Button(top, text='确定')
    button_pw.bind("<ButtonRelease-1>", lambda q: alterpw( str1,entry_new))
    button_pw.grid(row=4,column =1)

def alterpw( str1,entry_new):
    str2= entry_new.get()
    update ="update lib_card set pw='{}' where card_id='{}'".format(str2,str1)
    #update students set tel=default where id=5;

    curs=LIB.update(update)
    #print( str1)
    #print (curs)
    if curs :
        showinfo('通知',"成功修改密码")
    else:
        showwarning('通知',"发生错误")






def borrow(str1):
    cardid = str1
    # print(cardid)
    select = "select card_id from record where card_id='{}'".format(cardid)
    curs = LIB.select(select)
    print(curs)
    # order_index=LIB_order.curselection()
    # if len(order_index)!=0 :
    #   order_index=order_index[0]
    # else:
    #   order_index=0;
    # orders=order[order_index]
    num = 0
    for data in curs:
        num = num + 1
        # print ( data)

    if num > 0:
        select = "select card_id,name from lib_card where card_id='{}'".format(cardid)
        curs = LIB.select(select)
        top = Toplevel(root)
        text = Text(top)

        for (card_id, name) in curs:
            text.insert(INSERT, "card_id:{}\n".format(card_id))
            text.insert(INSERT, "name:{}\n".format(name))

        select = "select card_id, bookid , borrowdate, return_time from record  where card_id='{}' and still=1 ".format(cardid)

        curs = LIB.select(select)
        print(curs)

        text.insert(INSERT, "卡号\t书号\t借书时间\t\t还书时间\n")
        for (card_id ,bookid, borrowdate, return_time) in curs:
            text.insert(INSERT,
                        "{}\t{}\t{}\t\t{}\n".format(card_id ,bookid, borrowdate, return_time))
        text.pack()
    else:
        showinfo('Error', "你没有借过书")

def deletebook(Bookid):
    bookid = Bookid.get()
    print(bookid)

    if not (checkbook(bookid)):
        showerror('error', "无此书")
        return 0

    delete = "delete from book where bookid='{}'".format(bookid)
    LIB.delete(delete)
    showinfo('ok', '成功删除')
    return 1

def seebook():
    select ="select * from book "
    curs= LIB.select(select)
    #print (curs)
    top = Toplevel(root)
    text = Text(top)

    still = 0
    for i in curs:
        #print(i)
        still += 1
    text.insert(INSERT,"全部图书数量：{}\n本".format(still))
    text.insert(INSERT, "书号\t类型\t书名\t出版社\t出版时间\t\t作者\t价格\t总量\t剩余\n")


        #for a in i:
            #print (a)

    for (bookid,card_id,name,publisher,year, writer, price,total,stock) in curs:
        text.insert(INSERT,
                    "{}\t{}\t{}\t{}\t{}\t\t{}\t{}\t{}\t{}\n".format(bookid,card_id,name,publisher,year, writer, price,total,stock))
    text.pack()

def loginin():
    str1 = ide.get()
    str2 = pwde.get()
    num = 0
    # print(str1,str2)
    # print (curs)
    curs = LIB.select("select card_id,pw from lib_card where card_id='{}' and pw='{}'".format(str1, str2))
    # 登录检验

    loginin = Toplevel(root)
    loginin.title('注册')
    loginin.geometry('300x300')

    label_card_id = Label(loginin, text='卡号:').grid(row=0, column=0, sticky=W)
    label_pw = Label(loginin, text='密码:').grid(row=1, column=0, sticky=W)
    label_name = Label(loginin, text='姓命:').grid(row=2, column=0, sticky=W)
    label_unit = Label(loginin, text='权限（学生不用输入）:').grid(row=3, column=0, sticky=W)

    # 上面的是是个label
    entry_card_id = Entry(loginin)
    entry_card_id.grid(row=0, column=1, sticky=W)

    entry_pw = Entry(loginin)
    entry_pw.grid(row=1, column=1, sticky=W)

    entry_name = Entry(loginin)
    entry_name.grid(row=2, column=1, sticky=W)

    entry_lim = Entry(loginin)
    entry_lim.grid(row=3, column=1, sticky=W)

    # 下面的是一个按钮，这个按钮触发addcard函数，将是个参数插入
    button_constructe = Button(loginin, text='确定')
    button_constructe.bind("<ButtonRelease-1>", lambda q: addloginin(entry_card_id, entry_pw,entry_name,entry_lim))
    button_constructe.grid(row=4, column=0)

def addloginin(en1, en2, en3,en4):
    cardid = en1.get()
    pw  = en2.get()
    name = en3.get()
    lim = en4.get()

    print(type(lim[0]))



    if lim =='':
        if  checkcard(cardid):
            showinfo('通知',"已有此卡号")
        else:
            insert = "insert into lib_card values('{}','{}','{}')".format(cardid, name,pw)
            LIB.insert(insert)
            showinfo('ok', '添加成功')


    elif int(lim[0]) == 1  :
        print (lim[0])
        select = "select manage_id from managers where manage_id='{}'".format(cardid)

        # if (c_type not in ('T','S','O')):
        # showinfo('error',"NO SUCH TYPE")
        # return 0
        line = LIB.select(select)

        if (len(line) != 0):
            showinfo('失败', "已存在此账号!")
        else:
            insert = "insert into managers values('{}','{}')".format(cardid,pw)
            curs = LIB.insert(insert)


            if curs :
                showinfo('ok', '添加成功')
            else:
                showwarning('通知','添加管理员失败')
    elif lim :
        showwarning('通知','学生不用输入权限代码或者权限代码错误')




label_id= Label(root,text='账号: ')
label_id.grid(row=0,sticky=W)

ide=Entry(root)
ide.grid(row=0,column=1,sticky=W)
label_psw=Label(root,text='密码: ').grid(row=1,sticky=W)

pwde=Entry(root,show='*')
pwde.grid(row=1,column=1,sticky=E)

log_button=Button(root,text='管理员',command=login)
log_button.grid(row=1,column=2)

log_buttonst=Button(root,text='学生',command=studentlogin)
log_buttonst.grid(row=0,column =2,sticky = W)

log_buttonst=Button(root,text='注册',command=loginin)
log_buttonst.grid(row=3,column =2,sticky = W)

button_search=Button(root,text='书名搜索',command=booksearch)
button_search.grid(row=4,column=1,sticky=W)






#regi_button=Button(root,text='管理员注册',command=studentlogin)
#regi_button.place(x=110,y=50)

root.mainloop()
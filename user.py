import mysql.connector
from flask import session
import hashlib
from datetime import datetime


class user_operation:
     
    def myconnection(self):
        db=mysql.connector.connect(host="localhost",user="root" ,password="" ,database="rideon")
       # db=mysql.connector.connect(host="localhost" , user="root" ,password="" ,database="rideon",auth_plugin = 'mysql_native_password')
        return db

    def user_signup_insert(self,name,email,mobile,password):
        con=self.myconnection()
        sq="insert into user(name,email,mobile,password) values(%s,%s,%s,%s)"
        record = [name,email,mobile,password]
        cursor=con.cursor()  
        cursor.execute(sq, record)
        con.commit()
        cursor.close()
        con.close()
        return

    def user_delete(self,email):
        con=self.myconnection()
        sq="delete from user where email=%s"
        record = [email]
        cursor=con.cursor()  
        cursor.execute(sq, record)
        con.commit()
        cursor.close()
        con.close()
        return

    def user_login_verify(self,email,password):
        con=self.myconnection()
        sq="select name,email from user where email=%s and password=%s"
        pas = hashlib.md5(password.encode())
        password = pas.hexdigest()
        record = [email,password]
        cursor=con.cursor()  
        cursor.execute(sq, record)
        row = cursor.fetchall()
        rc = cursor.rowcount
        cursor.close()
        con.close()
        if rc == 0:
           return 0
        else:
           for r in row:
               session['user_name'] = r[0]
               session['user_email'] = r[1]  
           return 1

        
    def user_profile(self):
        con=self.myconnection()
        sq="select name,email,mobile from user where email=%s"
        record = [session['user_email']]
        cursor=con.cursor()  
        cursor.execute(sq, record)
        row = cursor.fetchall()
        return row  

    def user_profile_update(self,name,mobile):
        con=self.myconnection()
        sq="update user set name=%s,mobile=%s where email=%s"
        record = [name,mobile,session['user_email']]
        cursor=con.cursor()  
        cursor.execute(sq, record)
        con.commit()
        cursor.close()
        con.close()
        return 

    def user_bike_search(self,city):
        con=self.myconnection()
        sq="select photo,model_name,reg_no,charge,mfg_date,descp,bike_id,p.provider_id from bike b, provider p where b.provider_id=p.provider_id and p.city=%s"
        record=[city]
        cursor=con.cursor()  
        cursor.execute(sq,record)
        row = cursor.fetchall()
        return row   

    def user_bike_date_insert(self,bike_id,provider_id,start_date,end_date,charges):
        con=self.myconnection()
        sq="insert into rent(user_email,bike_id,provider_id,start_date,end_date,charges) values(%s,%s,%s,%s,%s,%s)"
        start_date = datetime.strptime(start_date,'%Y-%m-%d')
        end_date = datetime.strptime(end_date,'%Y-%m-%d')
        total_day=end_date-start_date
        total_day=total_day.days   #return nunmber of days
        charges = int(charges) * total_day
        record = [session['user_email'],bike_id,provider_id,start_date,end_date,charges]
        cursor=con.cursor()  
        cursor.execute(sq, record)
        con.commit()
        cursor.close()
        con.close()
        return

    def user_rent_view(self):
        con=self.myconnection()
        sq="select rent_id,reg_no,model_name,descp,start_date,end_date,charges,photo from rent r,bike b where r.bike_id=b.bike_id and user_email=%s"
        record=[session['user_email']]
        cursor=con.cursor()  
        cursor.execute(sq,record)
        row = cursor.fetchall()
        return row  


    def user_review(self,bike_id):
        con=self.myconnection()
        sq="select star,name,message from review r, user u where r.user_email=u.email and bike_id=%s"
        
        record = [bike_id]
        cursor=con.cursor()  
        cursor.execute(sq,record)
        row = cursor.fetchall()
        return row  

    def user_review_insert(self,bike_id,star,message):
        con=self.myconnection()
        sq="insert into review(user_email,bike_id,star,message) values(%s,%s,%s,%s)"
        record = [session['user_email'],bike_id,star,message]
        cursor=con.cursor()  
        cursor.execute(sq,record)
        con.commit()
        cursor.close()
        con.close()
        return
        
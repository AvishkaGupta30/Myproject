import mysql.connector
from flask import session
import hashlib
from datetime import datetime

class provider_operation:
     
    def myconnection(self):
        
        db=mysql.connector.connect(host="localhost",user="root" ,password="" ,database="rideon")
      #    db=mysql.connector.connect(host="localhost" , user="root" ,password="root" ,database="rideon",auth_plugin = 'mysql_native_password')
        return db

    def provider_signup_insert(self,name,email,mobile,address,city,password):
        con=self.myconnection()
        sq="insert into provider(name,email,mobile,address,city,password) values(%s,%s,%s,%s,%s,%s)"
        record = [name,email,mobile,address,city,password]
        cursor=con.cursor()  
        cursor.execute(sq, record)
        con.commit()
        cursor.close()
        #--- retrive provider id ----------------
        sq="select provider_id from provider order by provider_id desc limit 1"
        cursor=con.cursor()  
        cursor.execute(sq)
        con.close()
        row = cursor.fetchall()
        return row 

    # def user_delete(self,email):
    #     con=self.myconnection()
    #     sq="delete from user where email=%s"
    #     record = [email]
    #     cursor=con.cursor()  
    #     cursor.execute(sq, record)
    #     con.commit()
    #     cursor.close()
    #     con.close()
    #     return

    def provider_login_verify(self,provider_id,password):
        con=self.myconnection()
        sq="select name,provider_id from provider where provider_id=%s and password=%s"
        pas = hashlib.md5(password.encode())
        password = pas.hexdigest()
        record = [provider_id,password]
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
               session['provider_name'] = r[0]
               session['provider_id'] = r[1]    
           return 1

        
    def provider_profile(self):
        con=self.myconnection()
        sq="select provider_id,name,email,mobile,address from provider where provider_id=%s"
        record = [session['provider_id']] 
        cursor=con.cursor()  
        cursor.execute(sq, record) 
        row = cursor.fetchall() 
        return row 

    def provider_profile_update(self,email,mobile,address):
        con=self.myconnection()
        sq="update provider set email=%s,mobile=%s,address=%s where provider_id=%s"
        record = [email,mobile,address,session['provider_id']]
        cursor=con.cursor()   
        cursor.execute(sq, record)  
        con.commit() 
        cursor.close() 
        con.close() 
        return 

    def provider_bike_insert(self,model_name,reg_no,charge,mfg_date,descp,photo):
        con=self.myconnection()
        sq="insert into bike(provider_id,model_name,reg_no,charge,mfg_date,descp,photo) values(%s,%s,%s,%s,%s,%s,%s)"
        record = [session['provider_id'],model_name,reg_no,charge,mfg_date,descp,photo]
        cursor=con.cursor()  
        cursor.execute(sq, record)
        con.commit()
        cursor.close()
        con.close()
        return


 
    def provider_bike_view(self):
        con=self.myconnection()
        sq="select bike_id,model_name,reg_no,charge,mfg_date,descp,photo from bike where provider_id=%s"
        record = [session['provider_id']]
        cursor=con.cursor()  
        cursor.execute(sq, record)
        row = cursor.fetchall()
        return row  

    def provider_bike_delete(self,bike_id):
        con=self.myconnection()
        sq="delete from bike where bike_id=%s"
        record = [bike_id]
        cursor=con.cursor()  
        cursor.execute(sq, record)
        con.commit()
        cursor.close()
        con.close()
        return 

    def provider_bike_profile(self,bike_id):
        con=self.myconnection()
        sq="select bike_id,model_name,reg_no,charge,mfg_date,descp,photo from bike where bike_id=%s"
        record = [bike_id]
        cursor=con.cursor()  
        cursor.execute(sq, record)
        row = cursor.fetchall()
        return row  

    def provider_bike_profile_update(self,bike_id,model_name,reg_no,charge,mfg_date,descp):
        con=self.myconnection()
        sq="update bike set model_name=%s,reg_no=%s,charge=%s,mfg_date=%s,descp=%s where bike_id=%s"
        record = [model_name,reg_no,charge,mfg_date,descp,bike_id]
        cursor=con.cursor()  
        cursor.execute(sq, record)
        con.commit()
        cursor.close()
        con.close()
        return    

    def provider_bike_rent(self):
        con=self.myconnection()
        sq="select rent_id,bike_id,name,mobile,start_date,end_date,charges from rent r,user u  where r.user_email=u.email and provider_id=%s"
        record=[session['provider_id']]
        cursor=con.cursor()  
        cursor.execute(sq,record)
        row = cursor.fetchall()
        return row  
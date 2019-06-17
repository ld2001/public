#Final Database Project - Luke Ding and Pat Rademacher
#Charles Winstead
#June 4, 2019
#CS 586

import psycopg2 as p
import pandas as pd
import io
from sqlalchemy import create_engine
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy import ForeignKey
from sqlalchemy import TEXT, MetaData, Table, Column, Float
import csv

#initialize engine to connect to class Database

engine = create_engine('postgresql://s19wdb28:q4gB6xah*z@dbclass.cs.pdx.edu:5432/s19wdb28')
conn = engine.connect()

# read in all excel and CSV sheets through Pandas

Stores = pd.read_excel('Datasheet.xlsx', Sheetname=0)
Cars = pd.read_csv('Datasheet.csv')
service_centers = pd.read_csv('service_centers.csv', encoding = 'latin-1')
superchargers = pd.read_csv('superchargers.csv', encoding = 'latin-1')
customers = pd.read_csv('customers.csv', encoding = 'latin-1')
employees = pd.read_csv('employees.csv', encoding = 'latin-1')
purchhistory = pd.read_csv('purchasehistory.csv', encoding = 'latin-1')
storeemp = pd.read_csv('storeemp.csv', encoding = 'latin-1')
serveemp = pd.read_csv('servemp.csv', encoding = 'latin-1')
appointments = pd.read_csv('REALAPPOINTMENTS.csv', encoding = 'latin-1')
waittimes = pd.read_csv('waittimes.csv', encoding = 'latin-1')


#initialize proper list sizes for transferring CSV and Excel sheets to list data types


superchargers_array = [''] * 10
cust = [''] * 5
emp = [''] * 5
ph = [''] * 5
ste = [''] * 2
sve = [''] * 2
app = [''] * 8
wt = [''] * 5
newemp = [''] * 5
for i in range(10):
    superchargers_array[i] = list(superchargers.iloc[:, i])
for i in range(5):
    cust[i] = list(customers.iloc[:, i])
    #cust[i].strip("Ê")
    emp[i] = list(employees.iloc[:199, i])
    #emp[i].strip("Ê")
    ph[i] = list(purchhistory.iloc[:, i])
    wt[i] = list(waittimes.iloc[:, i])
for i in range(2):
    ste[i] = list(storeemp.iloc[:, i])
    sve[i] = list(serveemp.iloc[:, i])
for i in range(8):
    app[i] = list(appointments.iloc[:, i])

#had a strange instance when reading in CSV files from home through PSU's server - had to eliminate following character

cust[1] = [s.replace('Ê', ' ') for s in cust[1]]
cust[4] = [s.replace('Ê', '') for s in cust[4]]
emp[1] = [s.replace('Ê', ' ') for s in emp[1]]
emp[4] = [s.replace('Ê', '') for s in emp[4]]

Store_StoreID = []
Store_Country = []
Store_Name = []
Store_Address = []
Store_Extended = []
Store_Local = []
Store_Phone = []
Store_GoogleReviewRating = []

Store_StoreID.append(Stores.iloc[:, 0])
Store_Country.append(Stores.iloc[:, 1])
Store_Name.append(Stores.iloc[:, 2])
Store_Address.append(Stores.iloc[:, 3])
Store_Extended.append(Stores.iloc[:, 4])
Store_Local.append(Stores.iloc[:, 5])
Store_Phone.append(Stores.iloc[:, 6])
Store_GoogleReviewRating.append(Stores.iloc[:, 7])

Cars_Model = []
Cars_Subtype = []
Cars_Range = []
Cars_Zto60 = []

Cars_Model.append(Cars.iloc[:, 0])
Cars_Subtype.append(Cars.iloc[:, 1])
Cars_Range.append(Cars.iloc[:, 2])
Cars_Zto60.append(Cars.iloc[:, 3])

service_id = []
service_country = []
service_name = []
service_address = []
service_extended = []
service_local = []
service_phone = []
service_google = []

service_id.append(service_centers.iloc[:, 0])
service_country.append(service_centers.iloc[:, 1])
service_name.append(service_centers.iloc[:, 2])
service_address.append(service_centers.iloc[:, 3])
service_extended.append(service_centers.iloc[:, 4])
service_local.append(service_centers.iloc[:, 5])
service_phone.append(service_centers.iloc[:, 6])
service_google.append(service_centers.iloc[:, 7])

#convert lists to Pandas' DataFrame data type

df_stores = pd.DataFrame(data = {'store_id' : Store_StoreID[0], 'country' : Store_Country[0], 'name' : Store_Name[0], 'address' : Store_Address[0], 'extended' : Store_Extended[0], 'local' : Store_Local[0], 'phone' : Store_Phone[0], 'google_review_rating' : Store_GoogleReviewRating[0]})

df_cars = pd.DataFrame(data = {'model' : Cars_Model[0], 'subtype' : Cars_Subtype[0], 'range' : Cars_Range[0], 'zto60' : Cars_Zto60[0]})

df_service = pd.DataFrame(data = {'service_id' : service_id[0], 'country' : service_country[0], 'name': service_name[0], 'address': service_address[0], 'extended': service_extended[0], 'local': service_local[0], 'phone': service_phone[0], 'google_review_rating': service_google[0]})

df_superchargers = pd.DataFrame(data = {'supercharger_id': superchargers_array[0], 'country': superchargers_array[1], 'name': superchargers_array[2], 'address': superchargers_array[3], 'extended': superchargers_array[4], 'local': superchargers_array[5], 'phone': superchargers_array[6], 'google_review_rating': superchargers_array[7], 'stalls': superchargers_array[8], 'charge_rate': superchargers_array[9]})

df_customers = pd.DataFrame(data = {'customer_id': cust[0], 'name': cust[1], 'phone': cust[2], 'country': cust[3], 'email': cust[4]})

df_employees = pd.DataFrame(data ={'employee_id': emp[0], 'name': emp[1], 'role': emp[2], 'phone': emp[3], 'email': emp[4]})

df_ph = pd.DataFrame(data = {'customer_id': ph[0], 'model': ph[1], 'subtype': ph[2], 'date': ph[3], 'vin': ph[4]})

df_ste = pd.DataFrame(data = {'employee_id': ste[0], 'store_id': ste[1]})

df_sve = pd.DataFrame(data = {'service_id': sve[0], 'employee_id': sve[1]})

df_wt = pd.DataFrame(data = {'model': wt[0], 'subtype': wt[1], 'country': wt[2], 'wait_time': wt[3], 'price': wt[4]})

df_app = pd.DataFrame(data = {'appointment_id': app[0], 'model': app[1], 'subtype': app[2], 'service_id': app[3], 'employee_id': app[4], 'customer_id': app[5], 'date': app[6], 'time': app[7]})


#use the Pandas 'to_sql' function which converts DataFrames into proper data type to be process for postgres SQL


df_stores.to_sql(name='stores', con=engine, if_exists = 'replace', index=False, dtype = {"store_id": Integer(), "country": String(), "name" : String(), "address" : String, "extended" : String(), "local" : String(), "phone" : String(), "google_review_rating": Integer()})

df_cars.to_sql(name='cars', con=engine, if_exists = 'replace', index=False, dtype = {"model" : String(), "subtype" : String(), "range" : String(), "zto60" : Float()})

df_service.to_sql(name='service_centers', con=engine, if_exists = 'replace', index=False, dtype = {"service_id": Integer(), "country": String(), "name": String(), "address": String(), "extended": String(), "local": String(), "phone": String(), "google_review_rating": Integer()})

df_superchargers.to_sql(name= 'superchargers', con=engine, if_exists = 'replace', index=False, dtype = {"supercharger_id": Integer(), "country": String(), "name" : String(), "address" : String, "extended" : String(), "local" : String(), "phone" : String(), "google_review_rating": Integer(), "stalls":Integer(), "charge_rate": String()})

df_customers.to_sql(name= 'customers', con=engine, if_exists = 'replace', index=False, dtype = {"customer_id": Integer(), "name": String(), "phone" : String(), "country": String(), "email": String()})

df_employees.to_sql(name= 'employees', con=engine, if_exists = 'replace', index=False, dtype = {"employee_id": Integer(), "name": String(), "role" : String(), "phone": String(), "email": String()})

df_ph.to_sql(name= 'purchase_history', con=engine, if_exists = 'replace', index=False, dtype = {'customer_id': Integer(), 'model': String(), 'subtype': String(), 'date': Date(), 'vin': String()})

df_ste.to_sql(name= 'store_employees', con=engine, if_exists = 'replace', index=False, dtype = {'employee_id': Integer(), 'store_id': Integer()})

df_sve.to_sql(name= 'service_employees', con=engine, if_exists = 'replace', index=False, dtype = {'service_id': Integer(), 'employee_id': Integer()})

df_app.to_sql(name= 'appointments', con=engine, if_exists = 'replace', index=False, dtype = {'appointment_id': Integer(), 'model': String(), 'subtype': String(), 'service_id': Integer(), 'employee_id': Integer(), 'customer_id': Integer(), 'date': String(), 'time': Integer()})

df_wt.to_sql(name = 'wait_time', con=engine, if_exists = 'replace', index=False, dtype = {'model': String(), 'subtype': String(), 'country': String(), 'wait_time': Integer(), 'price': Integer()})


conn.execute('ALTER TABLE stores ADD PRIMARY KEY (store_id);')
conn.execute('ALTER TABLE cars ADD PRIMARY KEY (model, subtype);')
conn.execute('ALTER TABLE customers ADD PRIMARY KEY (customer_id);')
conn.execute('ALTER TABLE employees ADD PRIMARY KEY (employee_id);')
conn.execute('ALTER TABLE purchase_history ADD PRIMARY KEY (vin), ADD CONSTRAINT ph_cust FOREIGN KEY (customer_id) REFERENCES customers(customer_id), ADD CONSTRAINT ph_car FOREIGN KEY(model, subtype) REFERENCES cars(model, subtype);')
conn.execute('ALTER TABLE service_centers ADD PRIMARY KEY (service_id);')
conn.execute('ALTER TABLE wait_time ADD PRIMARY KEY (model, subtype, country), ADD CONSTRAINT wait_car FOREIGN KEY (model, subtype) REFERENCES cars(model, subtype);')
conn.execute('ALTER TABLE service_employees ADD PRIMARY KEY (service_id, employee_id), ADD CONSTRAINT serv_emp FOREIGN KEY(service_id) REFERENCES service_centers(service_id), ADD CONSTRAINT emp_serv FOREIGN KEY (employee_id) REFERENCES employees(employee_id);')
conn.execute('ALTER TABLE store_employees ADD PRIMARY KEY (store_id, employee_id), ADD CONSTRAINT store_employee_id FOREIGN KEY (store_id) REFERENCES stores(store_id), ADD CONSTRAINT employee_store_id FOREIGN KEY (employee_id) REFERENCES employees(employee_id);')
conn.execute('ALTER TABLE superchargers ADD PRIMARY KEY (supercharger_id);')
conn.execute('ALTER TABLE appointments ADD PRIMARY KEY (appointment_id), ADD CONSTRAINT app_empl FOREIGN KEY (employee_id) REFERENCES employees(employee_id), ADD CONSTRAINT app_car FOREIGN KEY(model, subtype) REFERENCES cars(model, subtype), ADD CONSTRAINT app_cust FOREIGN KEY(customer_id) REFERENCES customers(customer_id), ADD CONSTRAINT app_serv FOREIGN KEY (service_id) REFERENCES service_centers(service_id);')

conn.close()

#References

# https://docs.sqlalchemy.org/en/13/core/type_basics.html
# https://robertdavidwest.com/2014/10/12/python-pandas-%E2%86%92-mysql-using-sqlalchemy-a-k-a-sqlalchemy-for-pandas-users-who-dont-know-sql-the-brave-and-the-foolhardy/
# https://docs.sqlalchemy.org/en/13/orm/join_conditions.html
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html

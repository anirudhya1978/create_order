import requests

import mysql.connector 
import json
import random
import logging

#creates an order for a customer with a specific item and prince 
#returns 0 if the customer does not exist, else returns the order id created 
def create_order(cust_id, order_item, order_value):
    cnx = mysql.connector.connect(user='admin', password='Welcome1',
                              host='customerdb.ceklihwabawd.us-east-1.rds.amazonaws.com',
                              database='cust_order_db')
    cursor_outer = cnx.cursor()

#We are going to check if the customer we want to create an order for exits 
    query_outer= ("Select customer_name  from customer_details where cust_id=" + str(cust_id))
    print ("My query String " + query_outer)
    customer_exists = "None"
    cursor_outer.execute(query_outer)
    

    
    for (customer_name) in cursor_outer:
        customer_exists = customer_name
    else:
        customer_exists = "None"

    print ("Customer exists: " + customer_exists)
# If the customer does not existm then return 0    
    if customer_exists!= "None": #thsi is not working properly should == None but can't get it to work
        print("The Customer you entered does not exist, Please create customer first")
        cursor_outer.close()
        cnx.close()
        return 0
#if the customer exists then create order and return order id
    else:
        cursor = cnx.cursor()
        max_order_id = 0
        query = ("Select max(order_id) from order_detail")
        cursor.execute(query)
        for(order_id) in cursor:
            max_order_id = max(order_id)
            print ("Max Order Id" + str(max_order_id))
        
        cursor.close()
        
        add_order= ("insert into order_detail"
                       "(order_id, cust_id, order_item, order_value)"
                       "VALUES(%(order_id)s, %(cust_id)s, %(order_item)s, %(order_value)s)")
        
        order_data = {
            'order_id': max_order_id + 1,
            'cust_id': cust_id,
            'order_item': order_item,
            'order_value': order_value
            }
        cursor = cnx.cursor()
        cursor.execute(add_order,order_data)
        cnx.commit()
        cursor.close()
        cursor_outer.close()
        cnx.close()
        return max_order_id+1

#creates a shipment based on an order number and shipper 
#returns shipment_id created and -- tbd 0 if order does not exist in the system
def create_shipment(order_id, shipper_nm):
    
    max_ship_id = 0 # variable used for manipulating next ship id 
    cnx = mysql.connector.connect(user='admin', password='Welcome1',
                              host='customerdb.ceklihwabawd.us-east-1.rds.amazonaws.com',
                              database='cust_order_db')
    cursor = cnx.cursor()
    cursor_outer = cnx.cursor() # this cursor is just to check if the order exists
    query_outer = ("Select order_item from order_detail where order_id=" + str(order_id))
    cursor_outer.execute(query_outer)
    
    order_exists = "None" # variable to check if order exists
    
    for (order_item) in cursor_outer: # set order exists to 1 if the order exists
        order_exists = order_item
        print("order Item" + str(order_item))
        print ("Order Exists" + str(order_exists))
        
    if order_exists == "None": # if the order does not exist return 0 
        print("This order Id Does not exist")
        return 0
    else:                 # else create shipment and return the ship id that was created 
        rand_tracking_num = random.randint(1,1000)*4 # create a generic tracking number based on randon numbers
        #max_ship_id = 0 moved to a variable more global in nature 
        query = ("Select max(ship_id) from shipment_details")
        cursor.execute(query)
        for(ship_id) in cursor:
            max_ship_id = max(ship_id) +1 
            #print ("Max Order Id" + str(max_order_id))
        
        cursor.close() # close out the cursor
        add_ship= ("insert into shipment_details"
                       "(ship_id, order_id, shipper, tracking_number)"
                       "VALUES(%(ship_id)s, %(order_id)s, %(shipper)s, %(tracking_number)s)")
        
        ship_data = {
            'ship_id': max_ship_id,
            'order_id': order_id,
            'shipper': shipper_nm,
            'tracking_number': rand_tracking_num
            }
        cursor = cnx.cursor() #create a new cursor 
        cursor.execute(add_ship,ship_data)
        cnx.commit()
        cursor.close()
    cursor_outer.close() # close out the outer cursor as well 
    cnx.close()
    return max_ship_id

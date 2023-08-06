import requests
import json
import pandas as pd
import datetime
from IPython.display import clear_output
import time
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from cryptography.fernet import Fernet
import pymysql
import random
import math
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient

"""# SAFFRONSTAYS


```
sql_query(query,cypher_key)
sql_query_destructive(query,cypher_key)
ss_calendar(listing_ids,check_in,check_out)
ss_fb_catalogue()
```


"""

# SQL query on the SS database (ONLY SELECT) - returns a dataframe
def sql_query(query,cypher_key):

  key = bytes(cypher_key,'utf-8')
  cipher_suite = Fernet(key)

  host_enc = b'gAAAAABf-DBdA1f9-y-qVB2wwmHY8yD-gg8UpiREVNSTtPogl0rxl0suptWSib8J8YeoJm7yeJ3wDsmenGilQMttq88rnn0Llg=='
  user_enc = b'gAAAAABf-DB2YcOMC7JvsL-GihLJcImh6DvJpt1hNZFetiCzxMacK4agYHkyl3W1mnRkHNmEnecp4mMPZRfqO6bsLP1qgrpWbA=='
  pass_enc = b'gAAAAABf-DCFqT2kj-ExcdPn2IW0m0-M_3piK2-w1xNpUvH21XDsz3iqixvrT-NxKnpf1wirp0NcYoQEGt4TKpYHJzXcrXy6TA=='
  database_enc = b'gAAAAABfQPr48Sej-V7GarivuF4bsfBgP9rldzD500gl174HK4LZy70VfEob-kbaOBFa8rhuio_PbCFj4Nt3nJzVjKqC83d1NA=='
  
  myServer = cipher_suite.decrypt(host_enc).decode("utf-8")
  myUser = cipher_suite.decrypt(user_enc).decode("utf-8")
  myPwd = cipher_suite.decrypt(pass_enc).decode("utf-8")
  db = cipher_suite.decrypt(database_enc).decode("utf-8")

  myConnection = pymysql.connect(host=myServer,user=myUser,password=myPwd,db=db)

  if query.split(' ')[0] != 'SELECT':
    print("Error. Please only use non destructive (SELECT) queries.")
    return "Please only use non destructive (SELECT) queries."

  response_df = pd.io.sql.read_sql(query, con=myConnection)

  myConnection.close()

  return response_df

class dev:
  def sql_query(query):

    myServer = "15.206.90.86"
    myUser = "adminapi"
    myPwd = "SStays#123"
    db = "ss_admin_db"

    myConnection = pymysql.connect(host=myServer,user=myUser,password=myPwd,db=db,port=3306)

    response_df = pd.io.sql.read_sql(query, con=myConnection)

    myConnection.close()

    return response_df

  def sql_query_destructive(query):

    myServer = "15.206.90.86"
    myUser = "adminapi"
    myPwd = "SStays#123"
    db = "ss_admin_db"

    con = pymysql.connect(host=myServer,user=myUser,password=myPwd,db=db)

    try:
      with con.cursor() as cur:
          cur.execute(query)
          con.commit()

    finally:
      con.close()





class aws: 
  def sql_query(query,cypher_key):

    key = bytes(cypher_key,'utf-8')
    cipher_suite = Fernet(key)

    host_enc = b'gAAAAABf-DBdA1f9-y-qVB2wwmHY8yD-gg8UpiREVNSTtPogl0rxl0suptWSib8J8YeoJm7yeJ3wDsmenGilQMttq88rnn0Llg=='
    user_enc = b'gAAAAABf-DB2YcOMC7JvsL-GihLJcImh6DvJpt1hNZFetiCzxMacK4agYHkyl3W1mnRkHNmEnecp4mMPZRfqO6bsLP1qgrpWbA=='
    pass_enc = b'gAAAAABf-DCFqT2kj-ExcdPn2IW0m0-M_3piK2-w1xNpUvH21XDsz3iqixvrT-NxKnpf1wirp0NcYoQEGt4TKpYHJzXcrXy6TA=='
    database_enc = b'gAAAAABfQPr48Sej-V7GarivuF4bsfBgP9rldzD500gl174HK4LZy70VfEob-kbaOBFa8rhuio_PbCFj4Nt3nJzVjKqC83d1NA=='

    myServer = cipher_suite.decrypt(host_enc).decode("utf-8")
    myUser = cipher_suite.decrypt(user_enc).decode("utf-8")
    myPwd = cipher_suite.decrypt(pass_enc).decode("utf-8")
    db = cipher_suite.decrypt(database_enc).decode("utf-8")

    myConnection = pymysql.connect(host=myServer,user=myUser,password=myPwd,db=db)

    if query.split(' ')[0] != 'SELECT':
      print("Error. Please only use non destructive (SELECT) queries.")
      return "Please only use non destructive (SELECT) queries."

    response_df = pd.io.sql.read_sql(query, con=myConnection)

    myConnection.close()

    return response_df


  # to execute destructive queries 
  def sql_query_destructive(query,cypher_key):

    key = bytes(cypher_key,'utf-8')
    cipher_suite = Fernet(key)

    host_enc = b'gAAAAABf-DBdA1f9-y-qVB2wwmHY8yD-gg8UpiREVNSTtPogl0rxl0suptWSib8J8YeoJm7yeJ3wDsmenGilQMttq88rnn0Llg=='
    user_enc = b'gAAAAABf-DB2YcOMC7JvsL-GihLJcImh6DvJpt1hNZFetiCzxMacK4agYHkyl3W1mnRkHNmEnecp4mMPZRfqO6bsLP1qgrpWbA=='
    pass_enc = b'gAAAAABf-DCFqT2kj-ExcdPn2IW0m0-M_3piK2-w1xNpUvH21XDsz3iqixvrT-NxKnpf1wirp0NcYoQEGt4TKpYHJzXcrXy6TA=='
    database_enc = b'gAAAAABfQPr48Sej-V7GarivuF4bsfBgP9rldzD500gl174HK4LZy70VfEob-kbaOBFa8rhuio_PbCFj4Nt3nJzVjKqC83d1NA=='

    myServer = cipher_suite.decrypt(host_enc).decode("utf-8")
    myUser = cipher_suite.decrypt(user_enc).decode("utf-8")
    myPwd = cipher_suite.decrypt(pass_enc).decode("utf-8")
    db = cipher_suite.decrypt(database_enc).decode("utf-8")

    con = pymysql.connect(host=myServer,user=myUser,password=myPwd,db=db)


    try:
      with con.cursor() as cur:
          cur.execute(query)
          con.commit()

    finally:
      con.close()









# to execute destructive queries 
def sql_query_destructive(query,cypher_key):

  key = bytes(cypher_key,'utf-8')
  cipher_suite = Fernet(key)

  host_enc = b'gAAAAABfQPr4eF5i5aU4vfC4RieOdLr9GjwQPWWmvTWT728cK-qUoPesPZmLKwE4vTkhh3oxCmREfrHN1omRwmxJJuo_CS4cMmRKG8_mLFIBQG1mg2Kx102PixJAdf1l74dhO6VI8ZCR'
  user_enc = b'gAAAAABfQPr4PssChqSwFRHAGwKGCrKRLvnjRqfBkrazUydFvX3RBNAr5zAvKxdGJtaemdjq3uRwk1kgY4tLpIO9CxXj_JdC0w=='
  pass_enc = b'gAAAAABfQPr4iwH0c5pxjI4XfV-uT-pBt9tKfQgFJEfjTcTIjwipeN4tI_bG-TtHoamosKEuFOldevYPi-3usIj1ZDSrb-zsXg=='
  database_enc = b'gAAAAABfQPr48Sej-V7GarivuF4bsfBgP9rldzD500gl174HK4LZy70VfEob-kbaOBFa8rhuio_PbCFj4Nt3nJzVjKqC83d1NA=='

  myServer = cipher_suite.decrypt(host_enc).decode("utf-8")
  myUser = cipher_suite.decrypt(user_enc).decode("utf-8")
  myPwd = cipher_suite.decrypt(pass_enc).decode("utf-8")
  db = cipher_suite.decrypt(database_enc).decode("utf-8")

  con = pymysql.connect(host=myServer,user=myUser,password=myPwd,db=db)


  try:
    with con.cursor() as cur:
        cur.execute(query)
        con.commit()

  finally:
    con.close()

# Get the status for all the dates for a list of homes
def ss_calendar(listing_ids,check_in,check_out):

  parsed_listing_ids = str(listing_ids)[1:-1]
  parsed_listing_ids = parsed_listing_ids.replace("'","").replace(" ","")

  url = "https://www.saffronstays.com/calender_node.php"

  params={
      "listingList": parsed_listing_ids,
      "checkIn":check_in,
      "checkOut":check_out
      
  }
  payload = {}
  headers= {}

  response = requests.get(url, headers=headers, data = payload,params=params)
  response = json.loads(response.text.encode('utf8'))
  return response

# SS Facebook catalogue (a list of currently live listings)
def ss_fb_catalogue():
  url = "https://www.saffronstays.com/items_catalogue.php"

  response = requests.get(url)
  response_data = response.text.encode('utf8')

  csv_endpoint = str(response_data).split('`')[1]
  csv_download_url = "https://www.saffronstays.com/"+csv_endpoint

  ss_data = pd.read_csv(csv_download_url)

  return ss_data



# list of emails and preheader names, update with yours
def sendgrid_email(TEMPLATE_ID,EMAILS,api_key,PAYLOAD={}):
    """ Send a dynamic email to a list of email addresses

    :returns API response code
    :raises Exception e: raises an exception """
    # create Mail object and populate
    message = Mail(
        from_email=('book@saffronstays.com','SaffronStays'),
        to_emails=EMAILS
        )
    # pass custom values for our HTML placeholders
    message.dynamic_template_data = PAYLOAD


    message.template_id = TEMPLATE_ID
    # create our sendgrid client object, pass it our key, then send and return our response objects

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        code, body, headers = response.status_code, response.body, response.headers
        print(f"Response code: {code}")
        print(f"Response headers: {headers}")
        print(f"Response body: {body}")
        print("Dynamic Messages Sent!")
        return str(response.status_code)

    except Exception as e:
        print("Error: {0}".format(e))
        return "Error: {0}".format(e)

"""# Vista
```
# Vista API Wrappers 
# Refining the APIs
# Dataframes
# SQL
```


"""

# Return list of all locations
def vista_locations():
  locations = ["lonavala, maharashtra",
  "goa, goa",
  "alibaug, maharashtra",
  "nainital, uttarakhand",
  "chail, himanchal-pradesh",
  "manali, himachal-pradesh",
  "shimla, himanchal%20pradesh",
  "ooty, tamil%20nadu",
  "coorg, karnataka",
  "dehradun, uttarakhand",
  "jaipur, rajasthan",
  "udaipur, rajasthan",
  "mahabaleshwar, maharashtra",
  "nashik, maharashtra",
  "gangtok, sikkim",
  "gurgaon, haryana",
  "vadodara, gujarat",
  "kashmir, jammu"
  ]

  return locations

# Wrapper on the search API
def vista_search_api(search_type='city',location="lonavala,%20maharashtra",checkin="",checkout="",guests=2,adults=2,childs=0,page_no=1):

  url = "https://searchapi.vistarooms.com/api/search/getresults"

  param={
    }

  payload = {
      
      "city": location,
      "search_type": "city",
      "checkin": checkin,
      "checkout": checkout,
      "total_guests": guests,
      "adults": adults,
      "childs": childs,
      "page": page_no,
      "min_bedrooms": 1,
      "max_bedrooms": 30,
      "amenity": [],
      "facilities": [],
      "price_start": 1000,
      "price_end": 5000000,
      "sort_by_price": ""
        
    }
  headers = {}

  response = requests.post(url, params=param, headers=headers, data=payload)
  search_data = json.loads(response.text.encode('utf8'))

  return search_data

# Wrapper on the listing API
def vista_listing_api(slug='the-boulevard-villa',guests=2,checkin=datetime.date.today()+datetime.timedelta(1), checkout=datetime.date.today()+datetime.timedelta(2),
                         guest=3,adult=3,child=0):
  
  url = "https://v3api.vistarooms.com/api/single-property"

  param={
          'slug': slug,
          'checkin': checkin,
          'checkout': checkout,
          'guest': guest,
          'adult': adult,
          'child': child    
      }

  payload = {}
  headers = {
  }

  response = requests.get(url, params=param, headers=headers, data = payload)
  property_deets = json.loads(response.text.encode('utf8'))
  return property_deets

# Wrapper on the listing extra details API
def vista_listing_other_details_api(id=107):

  url = "https://v3api.vistarooms.com/api/single-property-detail"

  param={
          'id': id,
      }

  payload = {}
  headers = {
  }
  
  response = requests.get(url, params=param, headers=headers, data = payload)
  property_other_deets = json.loads(response.text.encode('utf8'))
  return property_other_deets

# Wrapper on the price calculator
def vista_price_calculator_api(property_id='710', checkin=datetime.date.today()+datetime.timedelta(1), checkout = datetime.date.today()+datetime.timedelta(2), guest = 2, adult = 2, child = 0):

  if type(checkin)==str:
    checkin = datetime.datetime.strptime(checkin,'%Y-%m-%d')
    checkout = datetime.datetime.strptime(checkout,'%Y-%m-%d')


  url = "https://v3api.vistarooms.com/api/price-breakup"
  
  param={
      'property_id': property_id,
      'checkin': checkin,
      'checkout': checkout,
      'guest': guest,
      'adult': adult,
      'child': child,   
      }

  payload = {}
  headers = {
  }

  response = requests.get(url, params=param, headers=headers, data = payload)
  pricing_deets = json.loads(response.text.encode('utf8'))
  return pricing_deets

# Wrapper on the avalability (Blocked dates)

def vista_availability_api(property_id=119):
  url = "https://v3api.vistarooms.com/api/calendar/property/availability"

  params={
      "property_id":property_id
  }
  payload = {}
  headers = {
  }

  response = requests.get(url, headers=headers, data = payload, params=params)
  calendar = json.loads(response.text.encode('utf8'))
  return calendar



# Gives a json response for basic listing data for the list of locations
def vista_search_locations_json(locations=["lonavala,%20maharashtra"],guests=2,get_all=False,wait_time=10):

  # Empty list to append (extend) all the data
  properties = []

  if get_all:
    locations = vista_locations()

  # Outer loop - for each location
  for location in locations:

    page_no = 1

    # Inner Loop - for each page in location ( acc to the Vista Search API )
    while True:

      clear_output(wait=True)
      print(f"Page {page_no} for {location.split('%20')[0]} ")

      # Vista API call (search)
      search_data = vista_search_api(location=location,guests=guests,page_no=page_no)

      # Break when you reach the last page for a location
      if not 'data' in search_data.keys():
        break
      if not search_data['data']['properties']:
        break
        
      properties.extend(search_data['data']['properties'])
      page_no += 1

      time.sleep(wait_time)


  return properties

# Retruns a DATAFRAME for the above functions & **DROPS DUPLICATES (always use this for analysis)
def vista_search_locations(locations=["lonavala,%20maharashtra"],guests=2,get_all=False,wait_time=10):
  villas = vista_search_locations_json(locations=locations, guests=guests,get_all=get_all,wait_time=wait_time)
  villas = pd.DataFrame(villas)
  villas = villas.drop_duplicates('id')

  return villas

# Returns a JSON with the listing details
def vista_listing(slug='the-boulevard-villa',guests=2,checkin=datetime.date.today()+datetime.timedelta(1), checkout=datetime.date.today()+datetime.timedelta(2)):

  print("Fetching ",slug)
  # Vista API call (listing)
  property_deets = vista_listing_api(slug=slug,guests=guests,checkin=checkin, checkout=checkout)
  
  # Get lat and long (diff API call)
  lat_long = vista_listing_other_details_api(property_deets['data']['property_detail']['id'])['data']['location']

  # Get pricing for various durations
  weekday_pricing = vista_price_calculator(property_deets['data']['property_detail']['id'],checkin=next_weekday(),checkout=next_weekday()+datetime.timedelta(1))
  weekend_pricing = vista_price_calculator(property_deets['data']['property_detail']['id'],checkin=next_weekday(5),checkout=next_weekday(5)+datetime.timedelta(1))
  entire_week_pricing = vista_price_calculator(property_deets['data']['property_detail']['id'],checkin=next_weekday(),checkout=next_weekday()+datetime.timedelta(7))
  entire_month_pricing = vista_price_calculator(property_deets['data']['property_detail']['id'],checkin=next_weekday(),checkout=next_weekday()+datetime.timedelta(30))

  # Add the extra fields in response (JSON)
  property_deets['data']['slug'] = slug
  property_deets['data']['lat'] = lat_long['latitude']
  property_deets['data']['lon'] = lat_long['longitude']
  property_deets['data']['checkin_date'] = checkin
  property_deets['data']['checkout_date'] = checkout
  property_deets['data']['weekday_pricing'] = weekday_pricing
  property_deets['data']['weekend_pricing'] = weekend_pricing
  property_deets['data']['entire_week_pricing'] = entire_week_pricing
  property_deets['data']['entire_month_pricing'] = entire_month_pricing
  property_deets['data']['price_per_room'] = property_deets['data']['price']['amount_to_be_paid']/property_deets['data']['property_detail']['number_of_rooms']

  return property_deets['data']

# Calculates the price for a duration (if unavailable, will automatically look for the next available dates) % Recursive function
def vista_price_calculator(property_id, checkin=datetime.date.today()+datetime.timedelta(1), checkout = datetime.date.today()+datetime.timedelta(2), guest = 2, adult = 2, child = 0, depth=0):

  date_diff = (checkout-checkin).days

  # Set the exit condition for the recursion depth ( to avoid an endless recursion -> slowing down the scripts )
  if date_diff < 7:
    depth_lim = 15
    next_hop = 7
  elif date_diff >= 7 and date_diff < 29:
    depth_lim = 7
    next_hop = 7
  else:
    depth_lim = 5
    next_hop = date_diff
    
  if depth==depth_lim:
    return f"Villa Probably Inactive, checked till {checkin}"
  
  if type(checkin)==str:
    checkin = datetime.datetime.strptime(checkin,'%Y-%m-%d')
    checkout = datetime.datetime.strptime(checkout,'%Y-%m-%d')

  # Vista API call (Calculation)
  pricing = vista_price_calculator_api(property_id=property_id, checkin=checkin, checkout=checkout, guest=guest, adult=adult, child=child)

  if 'error' in pricing.keys():

    # Recursion condition (Call self with next dates in case the dates are not available)
    if pricing['error'] == 'Booking Not Available for these dates':

      next_checkin = checkin + datetime.timedelta(next_hop)
      next_chekout = checkout + datetime.timedelta(next_hop)

      next_pricing = vista_price_calculator(property_id,checkin=next_checkin ,checkout=next_chekout,depth=depth+1)
      return next_pricing

    # For other errors (Like invalid listing ID)
    else:
      return pricing['error']
      
    return next_pricing
  else:
    return pricing['data']['price']

# Uses a list of slugs to generate a master DATAFRAME , this contains literally everything, ideal for any analysis on Vista
def vista_master_dataframe(slugs=(['vista-greenwoods-five-villa','maison-calme-villa','vista-greenwoods-four-villa','mehta-mansion','villa-maira'])):
  
  total_slugs = len(slugs)
  temp_progress_counter = 0
  villas_deets = []   

  for slug in slugs:
    villa_deets = vista_listing(slug=slug)
    villas_deets.append(villa_deets)
    villas_df = pd.DataFrame(villas_deets)

    temp_progress_counter += 1
    clear_output(wait=True)
    print("Done ",int((temp_progress_counter/total_slugs)*100),"%")

  prop_detail_df = pd.DataFrame(list(villas_df['property_detail']))
  agent_details_df =  pd.DataFrame(list(villas_df['agent_details']))
  price_df =  pd.DataFrame(list(villas_df['price']))

  literally_all_deets = pd.concat([prop_detail_df,villas_df,price_df,agent_details_df], axis=1)

  literally_all_deets = literally_all_deets.drop(['property_detail','mini_gallery', 'base_url',
       'agent_details', 'house_rule_pdf', 'mini_gallery_text',
       'seo','number_extra_guest', 'additionalcost',
       'days', 'min_occupancy', 'max_occupancy', 'amount_to_be_paid','total_guest',
       'extra_adult', 'extra_child', 'extra_adult_cost', 'extra_child_cost',
       'per_person','price','checkin_date','checkout_date','total_price','agent_short_words'], axis = 1)
  
  literally_all_deets['amenities'] = [[amenity['name'] for amenity in amenities] for amenities in literally_all_deets['amenities']]
  literally_all_deets['weekday_pricing_value'] = [wkdpr if type(wkdpr)==str else wkdpr['amount_to_be_paid'] for wkdpr in literally_all_deets['weekday_pricing']]
  literally_all_deets['weekend_pricing_value'] = [wkdpr if type(wkdpr)==str else wkdpr['amount_to_be_paid'] for wkdpr in literally_all_deets['weekend_pricing']]
  literally_all_deets['entire_week_pricing_value'] = [wkdpr if type(wkdpr)==str else wkdpr['amount_to_be_paid'] for wkdpr in literally_all_deets['entire_week_pricing']]
  literally_all_deets['entire_month_pricing_value'] = [wkdpr if type(wkdpr)==str else wkdpr['amount_to_be_paid'] for wkdpr in literally_all_deets['entire_month_pricing']]
  
  return literally_all_deets

# Takes 2 lists of listings (Old and New) and only responds with the Dataframe of the newly added listings
def added_villas_dataframe(old_slugs,new_slugs):
  added_slugs = list(set(new_slugs).difference(set(old_slugs)))
  added_villas = []

  if added_slugs:
    added_villas = vista_master_dataframe(added_slugs) 

  return added_villas

# Non Desctructive SQL QUERY - Try "SELECT * FROM VISTA_MASTER"
def vista_sql_query(query,cypher_key):
  # Returns a daframe object of the query response

  key = bytes(cypher_key,'utf-8')
  cipher_suite = Fernet(key)

  host_enc = b'gAAAAABfQPr4eF5i5aU4vfC4RieOdLr9GjwQPWWmvTWT728cK-qUoPesPZmLKwE4vTkhh3oxCmREfrHN1omRwmxJJuo_CS4cMmRKG8_mLFIBQG1mg2Kx102PixJAdf1l74dhO6VI8ZCR'
  user_enc = b'gAAAAABfQPr4PssChqSwFRHAGwKGCrKRLvnjRqfBkrazUydFvX3RBNAr5zAvKxdGJtaemdjq3uRwk1kgY4tLpIO9CxXj_JdC0w=='
  pass_enc = b'gAAAAABfQPr4iwH0c5pxjI4XfV-uT-pBt9tKfQgFJEfjTcTIjwipeN4tI_bG-TtHoamosKEuFOldevYPi-3usIj1ZDSrb-zsXg=='
  database_enc = b'gAAAAABfQPr48Sej-V7GarivuF4bsfBgP9rldzD500gl174HK4LZy70VfEob-kbaOBFa8rhuio_PbCFj4Nt3nJzVjKqC83d1NA=='

  myServer = cipher_suite.decrypt(host_enc).decode("utf-8")
  myUser = cipher_suite.decrypt(user_enc).decode("utf-8")
  myPwd = cipher_suite.decrypt(pass_enc).decode("utf-8")
  db = "uat_ss_db"

  myConnection = pymysql.connect(host=myServer,user=myUser,password=myPwd,db=db)

  response_df = pd.io.sql.read_sql(query, con=myConnection)

  myConnection.close()

  return response_df

# DESTRCUTIVE sql query
def vista_sql_destructive(query,cypher_key):

  key = bytes(cypher_key,'utf-8')
  cipher_suite = Fernet(key)

  host_enc = b'gAAAAABfQPr4eF5i5aU4vfC4RieOdLr9GjwQPWWmvTWT728cK-qUoPesPZmLKwE4vTkhh3oxCmREfrHN1omRwmxJJuo_CS4cMmRKG8_mLFIBQG1mg2Kx102PixJAdf1l74dhO6VI8ZCR'
  user_enc = b'gAAAAABfQPr4PssChqSwFRHAGwKGCrKRLvnjRqfBkrazUydFvX3RBNAr5zAvKxdGJtaemdjq3uRwk1kgY4tLpIO9CxXj_JdC0w=='
  pass_enc = b'gAAAAABfQPr4iwH0c5pxjI4XfV-uT-pBt9tKfQgFJEfjTcTIjwipeN4tI_bG-TtHoamosKEuFOldevYPi-3usIj1ZDSrb-zsXg=='
  database_enc = b'gAAAAABfQPr48Sej-V7GarivuF4bsfBgP9rldzD500gl174HK4LZy70VfEob-kbaOBFa8rhuio_PbCFj4Nt3nJzVjKqC83d1NA=='

  myServer = cipher_suite.decrypt(host_enc).decode("utf-8")
  myUser = cipher_suite.decrypt(user_enc).decode("utf-8")
  myPwd = cipher_suite.decrypt(pass_enc).decode("utf-8")
  db = "uat_ss_db"

  con = pymysql.connect(host=myServer,user=myUser,password=myPwd,db=db)


  try:
    with con.cursor() as cur:
        cur.execute(query)
        con.commit()

  finally:
    con.close()

def vista_weekly_update_script(cypher_key,search_api_wait=10):


  key = bytes(cypher_key,'utf-8')
  cipher_suite = Fernet(key)

  host_enc = b'gAAAAABfQPr4eF5i5aU4vfC4RieOdLr9GjwQPWWmvTWT728cK-qUoPesPZmLKwE4vTkhh3oxCmREfrHN1omRwmxJJuo_CS4cMmRKG8_mLFIBQG1mg2Kx102PixJAdf1l74dhO6VI8ZCR'
  user_enc = b'gAAAAABfQPr4PssChqSwFRHAGwKGCrKRLvnjRqfBkrazUydFvX3RBNAr5zAvKxdGJtaemdjq3uRwk1kgY4tLpIO9CxXj_JdC0w=='
  pass_enc = b'gAAAAABfQPr4iwH0c5pxjI4XfV-uT-pBt9tKfQgFJEfjTcTIjwipeN4tI_bG-TtHoamosKEuFOldevYPi-3usIj1ZDSrb-zsXg=='
  database_enc = b'gAAAAABfQPr48Sej-V7GarivuF4bsfBgP9rldzD500gl174HK4LZy70VfEob-kbaOBFa8rhuio_PbCFj4Nt3nJzVjKqC83d1NA=='

  dropcols = ['promotion_discount_amount',
              'promotion_applicable',
              'promotion_type',
              'promotion_discounted_total',
              'promotion_discount_percentage']

  sql_db_url = cipher_suite.decrypt(host_enc).decode("utf-8")
  sql_user = cipher_suite.decrypt(user_enc).decode("utf-8")
  sql_pw = cipher_suite.decrypt(pass_enc).decode("utf-8")
  sql_db = "uat_ss_db"

  # Get the list of all the current villas lited
  vista_search_data = vista_search_locations(get_all=True,wait_time=search_api_wait)


  new_slugs = vista_search_data['slug'].values

  query = "SELECT slug FROM VISTA_MASTER"

  old_slugs = vista_sql_query(query,cypher_key)
  old_slugs = old_slugs['slug'].values

  # Get the list of recently added and removed slugs
  added_slugs = list(set(new_slugs).difference(set(old_slugs)))
  removed_slugs = list(set(old_slugs).difference(set(new_slugs)))



  # Add the new listings to the Database
  vista_newly_added_df = added_villas_dataframe(old_slugs,new_slugs)

  vista_current_columns = vista_sql_query("SELECT * FROM VISTA_MASTER LIMIT 2",cypher_key).columns

  dropcols = set(vista_newly_added_df).difference(set(vista_current_columns))

  try:
    vista_newly_added_df.drop(dropcols,axis=1,inplace=True)
  except:
    pass

    
  if len(vista_newly_added_df) > 0:
      
      vista_newly_added_df['listing_status'] = "LISTED"
      vista_newly_added_df['status_on'] = datetime.datetime.today()
      vista_newly_added_df['created_on'] = datetime.datetime.today()

      # changind all the "Object" data types to str (to avoid some weird error in SQL)
      all_object_types = pd.DataFrame(vista_newly_added_df.dtypes)
      all_object_types = all_object_types[all_object_types[0]=='object'].index

      for column in all_object_types:
        vista_newly_added_df[column] = vista_newly_added_df[column].astype('str')

      #return vista_newly_added_df
      engine = create_engine(f"mysql+pymysql://{sql_user}:{sql_pw}@{sql_db_url}/{sql_db}")

      for i in range(len(vista_newly_added_df)):
        try:
          vista_newly_added_df.iloc[i:i+1].to_sql(name='VISTA_MASTER',if_exists='append',con = engine,index=False)
        except IntegrityError:
          pass  
          
      engine.dispose()

      
  # Update listing Statuses
  vista_update_lsiting_status(cypher_key)



  # A Summary of the updates
  final_success_response = {
      "No of Added Villas" : len(added_slugs),
      "No of Removed Villas" : len(removed_slugs),
      "Added Villas" : added_slugs,
      "Removed Villas" : removed_slugs
  }

  return final_success_response



# Update listing status 
def vista_update_lsiting_status(cypher_key):

  get_ids_query ="SELECT id,listing_status FROM VISTA_MASTER"
  vista_data = vista_sql_query(get_ids_query,cypher_key)

  for id in vista_data[vista_data['listing_status']=='DELISTED']['id']:
    stat = vista_check_if_listed(id)
    print(id,stat)
    if stat:
      print("Updating database...")
      query = "UPDATE VISTA_MASTER SET listing_status='LISTED',status_on='"+str(datetime.datetime.today())+"'WHERE id='"+str(id)+"'"
      vista_sql_destructive(query,cypher_key)

  for id in vista_data[vista_data['listing_status']=='LISTED']['id']:
    stat = vista_check_if_listed(id)
    print(id,stat)
    if not stat:
      print("Updating database...")
      query = "UPDATE VISTA_MASTER SET listing_status='DELISTED',status_on='"+str(datetime.datetime.today())+"'WHERE id='"+str(id)+"'"
      vista_sql_destructive(query,cypher_key)


# Breadth first seach algorithm to get the blocked dates
def vista_blocked_dates(property_id,ci,co):

  # check if the listing is active

  lt_status = vista_check_status(property_id)
  if lt_status in ["INACTIVE","DELISTED"]:
    return {
        "id" : property_id,
        "blocked_dates" : lt_status
    }

  # rg = Range => checkout - checkin (in days)
  rg = (datetime.datetime.strptime(co, "%Y-%m-%d") - datetime.datetime.strptime(ci, "%Y-%m-%d")).days    

  api_calls = 0


  # This list contains all the date ranges to be checked - there will be additions and subtractions to this list
  DTE = [(ci,co,rg)]                  


  # we will add the blocekd dates here 
  blocked = {}                         
  explored = []


  while len(DTE) != 0:

    # To see how many API calls happened (fewer the better)
    api_calls += 1                        

    # Pick one item (date range) from the DTE list -> to see if it is available
    dates = DTE.pop()                     

    print(f"Checking : {dates[0]} for {dates[2]} days")

    explored.append(dates)

    checkin = dates[0]
    checkout = dates[1]
    range = dates[2]

    # Call the vista API to see of this is available
    api_response = vista_price_calculator_api(property_id=property_id,checkin=checkin,checkout=checkout)      


    # If no error -> it is available, start the next iteration of the loop
    if "error" not in api_response.keys():                      
      print("Not Blocked")
      continue

    # if the range is unavailable  do this
    else:   

      print("Blocked")

      # if the range is 1, mark the date as blocked
      if range == 1:                                                                 
        blocked[checkin] = api_response['data']['price']['amount_to_be_paid']
        #blocked.append((checkin,api_response['data']['price']['amount_to_be_paid']))
      
      # if the range is not 1, split the range in half and add both these ranges to the DTE list
      else:                                                                           
        checkin_t = datetime.datetime.strptime(checkin, "%Y-%m-%d")
        checkout_t = datetime.datetime.strptime(checkout, "%Y-%m-%d")

        middle_date = checkin_t + datetime.timedelta(math.ceil(range/2))

        first_half = ( str(checkin_t)[:10] , str(middle_date)[:10] , (middle_date - checkin_t).days )
        second_half = ( str(middle_date)[:10] , str(checkout_t)[:10] , (checkout_t - middle_date).days)

        DTE.extend([first_half,second_half])


  response_obj = {
      "id" : property_id,
      "blocked_dates" : blocked,
      "meta_data": {
          "total_blocked_dates" : len(blocked),
          "api_calls":api_calls,
          "checked from": ci,
          "checked till":co
          #"date_ranges_checked":explored
      }
  }

  return response_obj

# To check if the villa is inactive (Listed but blocked for all dates)
def vista_check_status(property_id="",slug=""):

  if vista_check_if_listed(property_id,slug):
    status = "LISTED"
  else:
    status = "DELISTED"
    return status

  if status == "LISTED":

    min_nights = 1

    for i in [8,16,32,64,128]:

      price = vista_price_calculator_api(property_id , checkin=datetime.date.today()+datetime.timedelta(i), checkout = datetime.date.today()+datetime.timedelta(i + min_nights))


      if "error" not in price.keys():
        return "LISTED"

      if i == 128:
        return "INACTIVE"

      elif price['error'] == 'Booking Not Available for these dates':
        pass

      elif isinstance(price['error'].split(" ")[4],int):
        min_nights = price['error'].split(" ")[4]
        pass

def vista_check_if_listed(property_id="",slug=""):

  if len(slug)>0:
    try:
      listing = vista_listing_api(slug)
      property_id = listing['data']['property_detail']['id']
    except: 
      return False

  price = vista_price_calculator_api(property_id , checkin=datetime.date.today()+datetime.timedelta(5), checkout = datetime.date.today()+datetime.timedelta(7))

  if "error" not in price.keys():
    return True

  elif isinstance(price['error'],str):
    return True

  elif 'property_id' in dict(price['error']).keys():
    return False

  return False

# Update listing status 

def vista_update_lsiting_status_old(cypher_key):

  get_ids_query ="SELECT id,listing_status FROM VISTA_MASTER"
  vista_data = vista_sql_query(get_ids_query,cypher_key)


  for id in vista_data[vista_data['listing_status']=='DELISTED']['id']:
    print(id)
    stat = vista_check_status(id)
    print(id,stat)
    if stat in ["LISTED","INACTIVE"]:
      print("Updating database...")
      query = "UPDATE VISTA_MASTER SET listing_status='"+stat+"',status_on='"+str(datetime.datetime.today())+"'WHERE id='"+str(id)+"'"
      vista_sql_destructive(query,cypher_key)

  for id in vista_data[vista_data['listing_status']=='LISTED']['id']:
    stat = vista_check_status(id)
    print(id,stat)
    if stat in ["DELISTED","INACTIVE"]:
      print("Updating database...")
      query = "UPDATE VISTA_MASTER SET listing_status='"+stat+"',status_on='"+str(datetime.datetime.today())+"'WHERE id='"+str(id)+"'"
      vista_sql_destructive(query,cypher_key)

  for id in vista_data[vista_data['listing_status']=='INACTIVE']['id']:
    stat = vista_check_status(id)
    print(id,stat)
    if stat in ["DELISTED","LISTED"]:
      print("Updating database...")
      query = "UPDATE VISTA_MASTER SET listing_status='"+stat+"',status_on='"+str(datetime.datetime.today())+"'WHERE id='"+str(id)+"'"
      vista_sql_destructive(query,cypher_key)


def vista_update_lsiting_status(cypher_key):
    
  for i,r in vista_data.iterrows():

    try:
      old_status = r['listing_status']

      cal = vista_availability_api(r['id'])
    
      if "error" in cal.keys():
        current_status = "DELISTED"

      else:

        cal = pd.DataFrame(cal['data'])
        cal['date'] = cal['date'].astype('datetime64')

        if len(cal[cal['date']< datetime.datetime.today() + datetime.timedelta(90)])/88 > 1:
          current_status = "INACTIVE"


        else:
          current_status = "LISTED"

      if old_status != current_status:
        print(f"Updating database for {r['id']} - {current_status}...")
        query = f"UPDATE VISTA_MASTER SET listing_status='{current_status}',status_on='{str(datetime.datetime.today())}' WHERE id='{r['id']}'"
        #print(query)
        vista_sql_destructive(query,cypher_key)
      else:
        print(r['id'], "Unchanged")
      
    except:
      pass

"""# Lohono


```
# Lohono API wrappers
# Refining the APIs
# Master DataFrame
```


"""

# List of all lohono locations 
def lohono_locations():
  locations = ['india-alibaug','india-goa']
  return locations

# lohono Search API wrapper
def lohono_search_api(location_slug="india-goa",page=1):
  url = "https://www.lohono.com/api/property"

  params = {
      'location_slug': location_slug,
      'page': page
  }

  payload = {}
  headers = {
    'authority': 'www.lohono.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'accept': 'application/json',
    'user-agent': mock_user_agent(),
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': f'https://www.lohono.com/villas/india/{ location_slug.split("-")[-1] }',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
  }


  response = requests.get(url, headers=headers, data = payload, params=params)

  search_data = json.loads(response.text.encode('utf8'))

  return search_data

# lohono listing API wrapper
def lohono_listing_api(slug='prop-villa-magnolia-p5sp'):
  url = f"https://www.lohono.com/api/property/{slug}"

  payload = {}
  headers = {
    'authority': 'www.lohono.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'accept': 'application/json',
    'user-agent':  mock_user_agent(),
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.lohono.com/villas/india/goa/prop-fonteira-vaddo-a-C6Cn',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
  }

  response = requests.get(url, headers=headers, data = payload)

  listing_data = json.loads(response.text.encode('utf8'))
  return listing_data['response']

# lohono Pricing API wrapper
def lohono_pricing_api(slug,checkin,checkout,adult=2,child=0):

  url = f"https://www.lohono.com/api/property/{slug}/price"

  payload = "{\"property_slug\":\""+slug+"\",\"checkin_date\":\""+str(checkin)+"\",\"checkout_date\":\""+str(checkout)+"\",\"adult_count\":"+str(adult)+",\"child_count\":"+str(child)+",\"coupon_code\":\"\",\"price_package\":\"\",\"isEH\":false}"

  headers = {
    'authority': 'www.lohono.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'accept': 'application/json',
    'user-agent': mock_user_agent(),
    'content-type': 'application/json',
    'origin': 'https://www.lohono.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': f'https://www.lohono.com/villas/india/goa/{slug}?checkout_date={checkout}&adult_count={adult}&checkin_date={checkin}',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
  }

  response = requests.post(url, headers=headers, data = payload)
  pricing_data = json.loads(response.text.encode('utf8'))

  return pricing_data

# Basic details from the search API
def lohono_search(location_slugs=lohono_locations()):
  page = 1
  all_properties = []

  for location_slug in location_slugs:
    while True:
      print(f"page{ page } for {location_slug}")
      search_response = lohono_search_api(location_slug,page)
      all_properties.extend(search_response['response']['properties'])
      if search_response['paginate']['total_pages'] == page:
        break
      page += 1
      
  return pd.DataFrame(all_properties)

# All details for all the listings
def lohono_master_dataframe():
  search_data = lohono_search()

  slugs = search_data['property_slug'].values

  all_properties = []

  for slug in slugs:
    print(f"getting {slug}")
    listing_raw = lohono_listing_api(slug)
    all_properties.append(listing_raw)

  all_properties = pd.DataFrame(all_properties)

  all_properties['amenities'] = [[amenity['name'] for amenity in amenities] for amenities in all_properties['amenities']]
  all_properties['price'] = search_data['rate']
  all_properties['search_name'] = search_data['name']

  return all_properties

"""# AirBnb"""

airbnb_home_types = ['Entire home apt','Hotel room','Private room', 'Shared room']

airbnb_imp_amenities = [5,4,16,7,9,12]
# AC, Wifi , Breakfast, Parking, Pool, Pets  (Not in order)

# Airbnb Search API
def airbnb_search_api(place_id = "ChIJRYHfiwkB6DsRWIbipWBKa2k", city = "", state = "", min_price = 4000, max_price=50000, min_bedrooms=1, home_type=airbnb_home_types, items_per_grid = 50, amenities = [], items_offset = 0):

  home_type = [item.replace(" ","%20") for item in home_type]
  home_type = ["Entire%20home%2Fapt" if x=="Entire%20home%20apt" else x for x in home_type]
  home_type_filter = "%22%2C%22".join(home_type)

  amenities = [str(item) for item in amenities]
  amenities_filter = "%2C".join(amenities)  

  url = f"https://www.airbnb.co.in/api/v3/ExploreSearch?locale=en-IN&operationName=ExploreSearch&currency=INR&variables=%7B%22request%22%3A%7B%22metadataOnly%22%3Afalse%2C%22version%22%3A%221.7.8%22%2C%22itemsPerGrid%22%3A{items_per_grid}%2C%22tabId%22%3A%22home_tab%22%2C%22refinementPaths%22%3A%5B%22%2Fhomes%22%5D%2C%22source%22%3A%22structured_search_input_header%22%2C%22searchType%22%3A%22filter_change%22%2C%22mapToggle%22%3Afalse%2C%22roomTypes%22%3A%5B%22{home_type_filter}%22%5D%2C%22priceMin%22%3A{min_price}%2C%22priceMax%22%3A{max_price}%2C%22placeId%22%3A%22{place_id}%22%2C%22itemsOffset%22%3A{items_offset}%2C%22minBedrooms%22%3A{min_bedrooms}%2C%22amenities%22%3A%5B{amenities_filter}%5D%2C%22query%22%3A%22{city}%2C%20{state}%22%2C%22cdnCacheSafe%22%3Afalse%2C%22simpleSearchTreatment%22%3A%22simple_search_only%22%2C%22treatmentFlags%22%3A%5B%22simple_search_1_1%22%2C%22oe_big_search%22%5D%2C%22screenSize%22%3A%22large%22%7D%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22274161d4ce0dbf360c201612651d5d8f080d23820ce74da388aed7f9e3b00c7f%22%7D%7D"
  #url = f"https://www.airbnb.co.in/api/v3/ExploreSearch?locale=en-IN&operationName=ExploreSearch&currency=INR&variables=%7B%22request%22%3A%7B%22metadataOnly%22%3Afalse%2C%22version%22%3A%221.7.8%22%2C%22itemsPerGrid%22%3A20%2C%22roomTypes%22%3A%5B%22Entire%20home%2Fapt%22%5D%2C%22minBedrooms%22%3A0%2C%22source%22%3A%22structured_search_input_header%22%2C%22searchType%22%3A%22pagination%22%2C%22tabId%22%3A%22home_tab%22%2C%22mapToggle%22%3Afalse%2C%22refinementPaths%22%3A%5B%22%2Fhomes%22%5D%2C%22ib%22%3Atrue%2C%22amenities%22%3A%5B4%2C5%2C7%2C9%2C12%2C16%5D%2C%22federatedSearchSessionId%22%3A%22e597713a-7e46-4d10-88e7-3a2a9f15dc8d%22%2C%22placeId%22%3A%22ChIJM6uk0Jz75zsRT1nlkg6PwiQ%22%2C%22itemsOffset%22%3A20%2C%22sectionOffset%22%3A2%2C%22query%22%3A%22Karjat%2C%20Maharashtra%22%2C%22cdnCacheSafe%22%3Afalse%2C%22simpleSearchTreatment%22%3A%22simple_search_only%22%2C%22treatmentFlags%22%3A%5B%22simple_search_1_1%22%2C%22oe_big_search%22%5D%2C%22screenSize%22%3A%22large%22%7D%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22274161d4ce0dbf360c201612651d5d8f080d23820ce74da388aed7f9e3b00c7f%22%7D%7D"

  payload = {}
  headers = {
    'authority': 'www.airbnb.co.in',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'device-memory': '4',
    'x-airbnb-graphql-platform-client': 'apollo-niobe',
    #'x-csrf-token': 'V4$.airbnb.co.in$lHdA3kStJv0$yEvcPM_C6eeUUHkQuYEdGFWrZreA5ui1e4A-pMzDFI=',
    'x-airbnb-api-key': 'd306zoyjsyarp7ifhu67rjxn52tv0t20',
    'x-csrf-without-token': '4',
    'user-agent': mock_user_agent(),
    'viewport-width': '1600',
    'content-type': 'application/json',
    'accept': '*/*',
    'dpr': '1',
    'ect': '4g',
    'x-airbnb-graphql-platform': 'web',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    # 'referer': f'https://www.airbnb.co.in/s/{city}--{state}/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&adults=2&source=structured_search_input_header&search_type=filter_change&map_toggle=false&room_types%5B%5D=Entire%20home%2Fapt&price_min=4221&place_id={place_id}',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
  }

  response = requests.get(url, headers=headers, data = payload)

  response = json.loads(response.text.encode('utf8'))

  return response



# Airbnb Calendar API
def airbnb_calendar_api(listing_id,start_month=9,start_year=2020,bev='1600684519_NDg5ZGY1ZDQ4YjNk',month_count=4):
  url = f"https://www.airbnb.co.in/api/v3/PdpAvailabilityCalendar?operationName=PdpAvailabilityCalendar&locale=en-IN&currency=INR&variables=%7B%22request%22%3A%7B%22count%22%3A{month_count}%2C%22listingId%22%3A%22{listing_id}%22%2C%22month%22%3A{start_month}%2C%22year%22%3A{start_year}%7D%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22b94ab2c7e743e30b3d0bc92981a55fff22a05b20bcc9bcc25ca075cc95b42aac%22%7D%7D"

  payload = {}
  headers = {
    'authority': 'www.airbnb.co.in',
    #'pragma': 'no-cache',
    #'cache-control': 'no-cache',
    #'device-memory': '8',
    'x-airbnb-graphql-platform-client': 'minimalist-niobe',
    #'x-csrf-token': 'V4$.airbnb.co.in$lHdA3kStJv0$yEvcPMB_C6eeUUHkQuYEdGFWrZreA5ui1e4A-pMzDFI=',
    'x-airbnb-api-key': 'd306zoyjsyarp7ifhu67rjxn52tv0t20',
    #'x-csrf-without-token': '1',
    'user-agent': mock_user_agent(),
    'viewport-width': '1600',
    'content-type': 'application/json',
    'accept': '*/*',
    'dpr': '1',
    'ect': '4g',
    'x-airbnb-graphql-platform': 'web',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': f'https://www.airbnb.co.in/rooms/{listing_id}?adults=2&source_impression_id=p3_1598719581_vge1qn5YJ%2FXWgUKg&check_in=2020-10-01&guests=1',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cookie': f'bev={bev};'
  }

  response = requests.request("GET", url, headers=headers, data = payload)
  response = json.loads(response.text.encode('utf8'))

  return response

#Airbnb search DataFrame
def airbnb_search(place_ids = ["ChIJRYHfiwkB6DsRWIbipWBKa2k"], max_iters = 5, min_price=4000,max_price=200000, home_type=[],amenities=[], min_bedrooms=1 ):

  all_items = []

  for place_id in place_ids:

    counter = 1

    offset = 0

    while counter<=max_iters:  

      print(f"Round {counter} for {place_id}")
      counter+=1

      response = airbnb_search_api(place_id = place_id, min_price = min_price ,max_price=max_price, min_bedrooms=min_bedrooms,home_type=home_type,amenities=amenities, items_offset = offset)
      offset += 50

      if not response['data']['dora']['exploreV3']['sections']:
        break

      else:
        for sections in response['data']['dora']['exploreV3']['sections']:
          if 'listing' in sections['items'][0].keys():
            all_items.extend(sections['items'])


  items_df = pd.DataFrame([item['listing'] for item in all_items])
  prices_df = pd.DataFrame([item['pricingQuote'] for item in all_items])
  items_df[['canInstantBook','weeklyPriceFactor','monthlyPriceFactor','priceDropDisclaimer','priceString','rateType']] = prices_df[['canInstantBook','weeklyPriceFactor','monthlyPriceFactor','priceDropDisclaimer','priceString','rateType']]
  return_obj = items_df[['id','name','roomAndPropertyType','reviews','avgRating','starRating','reviewsCount','amenityIds','previewAmenityNames','bathrooms','bedrooms','city','lat','lng','personCapacity','publicAddress','pictureUrl','pictureUrls','isHostHighlyRated','isNewListing','isSuperhost','canInstantBook','weeklyPriceFactor','monthlyPriceFactor','priceDropDisclaimer','priceString','rateType']]
  return_obj = return_obj.drop_duplicates('id')

  return return_obj

# Airbnb Calendar DataFrame
def airbnb_calendar(listing_id,start_month=datetime.datetime.today().month,start_year=datetime.datetime.today().year):

  api_response = airbnb_calendar_api(listing_id,start_month,start_year)

  all_months = [month['days'] for month in api_response['data']['merlin']['pdpAvailabilityCalendar']['calendarMonths']]

  all_days=[]

  for month in all_months:
    all_days.extend(month)

  all_days = pd.DataFrame(all_days)
  all_days['price'] = [item['localPriceFormatted'][1:].replace(",","") for item in all_days['price'].values]

  all_days['calendarDate'] = pd.to_datetime(all_days['calendarDate'])

  all_days['listing_id'] = listing_id

  all_days = all_days.astype({'price':'int32'})

  return all_days

# Get Occupancy data for a listing id
def airbnb_occupancy(listing_id):
  clndr = airbnb_calendar(listing_id=listing_id,start_month=datetime.datetime.today().month,start_year=datetime.datetime.today().year)

  clndr = clndr.set_index('calendarDate')

  clndr_monthly = clndr.groupby(pd.Grouper(freq='M')).mean()

  clndr_monthly['month-year'] = [str(item.month_name())+" "+str(item.year) for item in clndr_monthly.index]

  clndr_monthly = clndr_monthly.set_index('month-year')

  clndr_monthly['occupancy'] = 1-clndr_monthly['available']

  occupancy = clndr_monthly['occupancy'].to_json()
  available = clndr[clndr['available']==True].index
  blocked = clndr[clndr['available']==False].index

  available = [str(item.date()) for item in available]
  blocked = [str(item.date()) for item in blocked]

  return_obj = {
      "listing_id": listing_id,
      "monthly_occupancy" : occupancy,
      "blocked_dates" : blocked,
      "available_dates": available
  }

  return return_obj





"""# Helper Functions


```
next_weekday()
mock_user_agent()
mock_proxy()
earth_distance(lat1,lon1,lat2,lon2)
```


"""

# Get the next weekday ( 0=monday , 1 = tuesday ... )
def next_weekday(weekday=0, d=datetime.date.today()):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

# default - next monday

# gives a random user-agent to use in the API call
def mock_user_agent():
  users = ["Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0",
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41",
  "Opera/9.80 (Macintosh; Intel Mac OS X; U; en) Presto/2.2.15 Version/10.00",
  "Opera/9.60 (Windows NT 6.0; U; en) Presto/2.1.1",
  "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1",
  "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)"]

  return users[random.randint(0,7)]

# Gives a 'proxies' object for a 'requests' call
def mock_proxy():

  proxies_list = ["45.72.30.159:80",
  "45.130.255.156:80",
  "193.8.127.117:80",
  "45.130.255.147:80",
  "193.8.215.243:80",
  "45.130.125.157:80",
  "45.130.255.140:80",
  "45.130.255.198:80",
  "185.164.56.221:80",
  "45.136.231.226:80"]

  proxy = proxies_list[random.randint(0,9)]

  proxies = {
  "http": proxy,
  "https": proxy
  }

  return proxies

# Arial distance between 2 pairs of coordinates 
def earth_distance(lat1,lon1,lat2,lon2):

  # Radius of the earth
  R = 6373.0

  lat1 = math.radians(lat1)
  lon1 = math.radians(lon1)
  lat2 = math.radians(lat2)
  lon2 = math.radians(lon2)

  dlon = lon2 - lon1
  dlat = lat2 - lat1

  #Haversine formula
  a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
  
  distance = R * c

  return distance

def to_fancy_date(date):
  tmstmp = pd.to_datetime(date)
  day = tmstmp.day
  
  if 4 <= day <= 20 or 24 <= day <= 30:
      suffix = "th"
  else:
      suffix = ["st", "nd", "rd"][day % 10 - 1]

  return f"{tmstmp.day}{suffix} {tmstmp.month_name()} {tmstmp.year}"

"""# TEST"""

def final_test():
  ss_latest()
  vista_latest()
  vista_locations()
  vista_search_locations_json(locations=["nainital, uttarakhand"],guests=2,get_all=False)
  vista_search_locations(locations=["nainital, uttarakhand"],guests=2,get_all=False)
  vista_listing(slug='the-boulevard-villa',guests=2,checkin=datetime.date.today()+datetime.timedelta(1), checkout=datetime.date.today()+datetime.timedelta(2))
  vista_listing_other_details_api(slug='the-boulevard-villa')
  vista_price_calculator(property_id='310', checkin=datetime.date.today()+datetime.timedelta(1), checkout = datetime.date.today()+datetime.timedelta(2), guest = 2, adult = 2, child = 0)
  next_weekday(weekday=0, d=datetime.date.today())
  vista_master_dataframe(slugs=(['vista-greenwoods-five-villa','maison-calme-villa','vista-greenwoods-four-villa','mehta-mansion','villa-maira']))
  vista_map_all()
  ss_map_all()
  ss_vs_vista()

  return "All Good :)"

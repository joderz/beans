# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from   flask_migrate import Migrate
from   flask_minify  import Minify
from   sys import exit
from flask import Flask, redirect, request, render_template, url_for, session, flash

from apps.config import config_dict
from apps import create_app, db

from sqlalchemy import create_engine
from sqlalchemy import text

#run SQL Queries 
class Modelz:
    def __init__(self):
        #self.engine = create_engine('postgresql://postgres:chua@localhost:5432/postgres', echo=True)
        self.engine = create_engine(os.environ['DB_URL'])

    def executeRawSql(self, statement, params={}):
        out = None
        with self.engine.connect() as con:
            out = con.execute(text(statement), params)
        return out

    def hostsgraph(self):
        return self.executeRawSql("""SELECT account_created,count(*) FROM host GROUP BY account_created ORDER BY account_created ASC""")

    def reservation_list(self):
        return self.executeRawSql("""SELECT * FROM reservation LIMIT 10""")

    def date_1(self):
        return self.executeRawSql("""select d.year, count(r.reservation_id) as no_of_reservation, sum(r.duration*r.price_per_day) as total_spending
                                    from reservation r, date d
                                    where r.date_id=d.id
                                    group by d.year
                                    """)

    def date_3(self):
        return self.executeRawSql("""select d.day_of_week, count(r.reservation_id) as no_of_reservation, sum(r.duration*r.price_per_day) as total_spending
                                    from reservation r, date d
                                    where r.date_id=d.id
                                    group by d.day_of_week
                                    order by count(r.reservation_id) desc;
                                    """)

    def date_2(self):
        return self.executeRawSql("""
                                    select d.month, count(r.reservation_id) as no_of_reservation, sum(r.duration*r.price_per_day) as total_spending
                                    from reservation r, date d
                                    where r.date_id=d.id
                                    group by d.month
                                    order by count(r.reservation_id) desc;
                                    """)
    def date_4(self):
        return self.executeRawSql("""
                                    select d.is_weekend, count(r.reservation_id) as no_of_reservation, sum(r.duration*r.price_per_day) as total_spending
                                    from reservation r, date d
                                    where r.date_id=d.id
                                    group by d.is_weekend
                                    order by count(r.reservation_id) desc;
                                    """)
    def MemberSilver(self):
        return self.executeRawSql("""SELECT DISTINCT c.customer_name, c.email, c.phone, c.gender
                                    FROM customers c
                                    WHERE (c.total_spending>=2000 and c.total_spending<3500)
                                    OR (c.no_of_booking>=15 and c.no_of_booking<25)
                                    AND (c.account_created<=2017);
                                    """)
    
    def MemberGold(self):
        return self.executeRawSql("""SELECT DISTINCT c.customer_name, c.email, c.phone, c.gender
                                    FROM customers c
                                    WHERE (c.total_spending>=3500 and c.total_spending<5000)
                                    OR (c.no_of_booking>=25 and c.no_of_booking<35)
                                    AND (c.account_created<=2017);
                                    """)
    
    def MemberDiamond(self):
        return self.executeRawSql("""  SELECT DISTINCT c.customer_name, c.email, c.phone, c.gender
                                    FROM customers c
                                    WHERE c.total_spending>=5000
                                    OR c.no_of_booking>=35
                                    AND c.account_created<=2017;
                                    """)


    def host_1(self):
        return self.executeRawSql("""select h.host_name,h.email,h.account_created
                                    from host h
                                    where h.review_scores_rating=100
                                    order by h.number_of_reviews;
                                    """)

    def host_2(self):
        return self.executeRawSql("""select distinct h1.host_name, h1.email, h1.account_created, h1.number_of_reviews
                                    from host h1
                                    where h1.number_of_reviews>=all(
                                    select h2.number_of_reviews
                                    from host h2
                                    where h1.email!=h2.email)
                                    group by h1.email;
                                    """)

    def host_3(self):
        return self.executeRawSql("""select h.email, h.review_scores_cleanliness, h.review_scores_accuracy, h.review_scores_communication, h.review_scores_location, h.review_scores_checkin, h.review_scores_value
                                    from host h
                                    where h.review_scores_cleanliness<=5 
                                    or h.review_scores_accuracy<=5
                                    or h.review_scores_communication<=5
                                    or h.review_scores_location<=5
                                    or h.review_scores_checkin<=5
                                    or h.review_scores_value<=5;
                                    """)   

    def host_4(self):
        return self.executeRawSql("""select h.host_name,h.email,h.number_of_listings
                                    from host h
                                    order by h.number_of_listings desc;
                                    """)

    def host_5(self):
        return self.executeRawSql("""select h.email, h.number_of_listings, p.country, p.city
                                    from host h, property p
                                    where h.email=p.email
                                    group by h.email, p.country, p.city
                                    order by h.number_of_listings desc;
                                    """)

    def host_6(self):
        return self.executeRawSql("""select h.email, sum(r.duration*r.price_per_day) as total_spending
                                    from reservation r, host h
                                    where r.host_email=h.email
                                    group by h.email
                                    order by sum(r.duration*r.price_per_day) desc;
                                    """)    

    def property_11(self):
        return self.executeRawSql("""select p.property_type, trunc(avg(h.review_scores_rating),0) as avg_rating
                                    from property p, host h
                                    where p.email=h.email 
                                    and h.review_scores_rating is not null
                                    group by p.property_type
                                    order by avg(h.review_scores_rating) DESC;
                                    """)

    def property_12(self):
        return self.executeRawSql("""select p.room_type, trunc(avg(h.review_scores_rating),0) as avg_rating
                                    from property p, host h
                                    where p.email=h.email 
                                    and h.review_scores_rating is not null
                                    group by p.room_type
                                    order by avg(h.review_scores_rating) DESC;
                                    """)

    def property_13(self):
        return self.executeRawSql("""select p.accommodates, trunc(avg(h.review_scores_rating),0) as avg_rating
                                    from property p, host h
                                    where p.email=h.email 
                                    and h.review_scores_rating is not null
                                    group by p.accommodates
                                    order by avg(h.review_scores_rating) DESC;
                                    """)   

    def property_14(self):
        return self.executeRawSql("""select p.city, trunc(avg(h.review_scores_rating),0) as avg_rating
                                    from property p, host h
                                    where p.email=h.email 
                                    and h.review_scores_rating is not null
                                    group by p.city
                                    order by avg(h.review_scores_rating) DESC;
                                    """)

    def property_21(self):
        return self.executeRawSql("""select sum(r.price_per_day*r.duration) as total_revenue, p.city, d.year
                                    from reservation r
                                    natural join property p
                                    natural join date d
                                    where d.year='2022'
                                    group by p.city, d.year
                                    order by sum(r.price_per_day*r.duration) desc;

                                    """)

    def property_22(self):
        return self.executeRawSql("""select sum(r.price_per_day*r.duration) as total_revenue, p.city, d.year
                                    from reservation r
                                    natural join property p
                                    natural join date d
                                    where d.year='2021'
                                    group by p.city, d.year
                                    order by sum(r.price_per_day*r.duration) desc;

                                    """) 

    def property_23(self):
        return self.executeRawSql("""select sum(r.price_per_day*r.duration) as total_revenue, p.city, d.year
                                    from reservation r
                                    natural join property p
                                    natural join date d
                                    where d.year='2020'
                                    group by p.city, d.year
                                    order by sum(r.price_per_day*r.duration) desc;

                                    """)

    def property_31(self):
        return self.executeRawSql("""select p.property_type, trunc(avg(r.number_of_guests),0)
                                    from property p, reservation r
                                    where p.property_id=r.property_id
                                    group by p.property_type;
                                    """)

    def property_32(self):
        return self.executeRawSql("""select p.room_type, trunc(avg(r.number_of_guests),0) as avg_guests
                                    from property p, reservation r
                                    where p.property_id=r.property_id
                                    group by p.room_type;
                                    """)   

    def property_33(self):
        return self.executeRawSql("""select p.city, trunc(avg(r.number_of_guests),0) as avg_guests
                                    from property p, reservation r
                                    where p.property_id=r.property_id
                                    group by p.city;
                                    """)

    def property_41(self):
        return self.executeRawSql("""select p.property_type, count(p.property_type) as no_of_propertytype , p.country, p.city
                                    from property p
                                    group by p.property_type, p.country, p.city
                                    order by count(p.property_type) desc;
                                    """)

    def property_42(self):
        return self.executeRawSql("""select p.room_type, count(p.room_type) as no_of_propertytype , p.country, p.city
                                    from property p
                                    group by p.room_type, p.country, p.city
                                    order by count(p.room_type) desc;
                                    """) 

    def overview(self,value):
        return self.executeRawSql("""SELECT 
                                        r.date_id, r.property_id, p.country, p.city,
                                        p.property_type, p.room_type, p.accommodates, p.beds, p.bed_type, p.bathrooms,
                                        h.email, h.account_created, h.number_of_listings, h.number_of_reviews, 
                                        h.review_scores_rating, h.review_scores_cleanliness, h.review_scores_accuracy, h.review_scores_communication, h.review_scores_location, h.review_scores_checkin, h.review_scores_value,
                                        r.duration, r.price_per_day, r.number_of_guests
                                        from reservation r, date d, property p, host h
                                        WHERE r.date_id = d.id
                                        AND r.property_id = p.property_id
                                        AND r.host_email = h.email
                                        -- filters
                                        AND d.month = :month
                                        AND d.year = :year
                                        AND r.price_per_day >= :price
                                        AND r.duration >= :duration
                                        AND p.accommodates >= :accommodates
                                        AND p.beds >= :beds
                                        AND p.bathrooms >= :bathrooms
                                        AND h.review_scores_rating >= :rating;""",value)



#result = db.session.execute('SELECT * FROM my_table WHERE my_column = :val', {'val': 5})




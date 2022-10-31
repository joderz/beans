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
        self.engine = create_engine('postgresql://postgres:chua@localhost:5432/postgres', echo=True)

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

    def date_2(self):
        return self.executeRawSql("""select d.day_of_week, count(r.reservation_id) as no_of_reservation, sum(r.duration*r.price_per_day) as total_spending
                                    from reservation r, date d
                                    where r.date_id=d.id
                                    group by d.day_of_week
                                    order by sum(r.duration*r.price_per_day) desc;
                                    """)

    def date_3(self):
        return self.executeRawSql("""Months of less than 80 reservations 
                                    select d.month, count(r.reservation_id) as no_of_reservation, sum(r.duration*r.price_per_day) as total_spending
                                    from reservation r, date d
                                    where r.date_id=d.id
                                    group by d.month
                                    having count(*)<80;
                                    """)
    def Member(self):
        return self.executeRawSql("""SELECT DISTINCT c.customer_name, c.email, c.phone, c.gender
                                    FROM customers c
                                    WHERE (c.total_spending>=2000 and c.total_spending<3500)
                                    OR (c.no_of_booking>=15 and c.no_of_booking<25)
                                    AND (c.account_created<=2017);

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




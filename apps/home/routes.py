# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from models import Modelz
from apps.home import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound

import sys
sys.path.append(r"C:\Users\Jodi\Documents\GitHub\beans")

Modelz = Modelz()


@blueprint.route('/overview', methods=['GET', 'POST'])
@login_required
def index():
    # drop down data
    data2 = ['Month', '1', '2', '3', '4', '5',
             '6', '7', '8', '9', '10', '11', '12']
    data3 = ['Year', '2022', '2021', '2020']
    data4 = ['Price', 'all', '>=500', '>=1000']
    data5 = ['Duration', 'all', '2 or more', '4 or more']
    data6 = ['Accommodates', 'all', '2 or more', '4 or more']
    data7 = ['Beds', 'all', '2 or more', '4 or more']
    data8 = ['Bathrooms', 'all', '2 or more', '4 or more']
    data9 = ['Rating', 'all', '2 or more', '4 or more']
    # data2=[{'option2': 'Month'},{'option2': '1'}, {'option2': '2'},{'option2': '3'}, {'option2': '4'},{'option2': '5'}, {'option2': '6'},{'option2': '7'}, {'option2': '8'},{'option2': '9'}, {'option2': '10'},{'option2': '11'}, {'option2': '12'}]
    # data3=[{'option3': 'Year'}, {'option3': '2022'}, {'option3': '2021'},{'option3': '2020'}]
    # data4=[{'option4': 'Price'}, {'option4': 'all'},{'option4': '>=500'}, {'option4': '>=1000'}]
    # data5=[{'option5': 'Duration'}, {'option5': 'all'}, {'option5': '2 or more'},{'option5': '4 or more'}]
    # data6=[{'option6': 'Accommodates'}, {'option6': 'all'}, {'option6': '2 or more'},{'option6': '4 or more'}]
    # data7=[{'option7': 'Beds'}, {'option7': 'all'}, {'option7': '2 or more'},{'option7': '4 or more'}]
    # data8=[{'option8': 'Bathrooms'}, {'option8': 'all'}, {'option8': '2 or more'},{'option8': '4 or more'}]
    # data9=[{'option9': 'rating'}, {'option9': 'all'}, {'option9': '2 or more'},{'option9': '4 or more'}]

    date_1 = Modelz.date_1()

    # query results
    if request.method == 'GET':
        user = {}
    else:
        output_raw = list(request.form.values())
        temp_dict = {k: v for k, v in enumerate(
            [data2, data3, data4, data5, data6, data7, data8, data9])}
        output = []
        for i in range(8):
            output.append(temp_dict[i][int(output_raw[i])])
        for i in range(len(output)):
            if output[i] == '>=500':
                output[i] = "500"
            elif output[i] == '>=1000':
                output[i] = '1000'
            elif output[i] == '4 or more':
                output[i] = '4'
            elif output[i] == '2 or more':
                output[i] = '2'
            elif output[i] == 'all':
                output[i] = '0'

        user = Modelz.overview({"month": output[0], "year": output[1], "price": output[2], "duration": output[3],
                               "accommodates": output[4], "beds": output[5], "bathrooms": output[6], "rating": output[7]})

    return render_template('home/index.html', segment='index', results=user, date_1=date_1,
                           data2=data2, data3=data3, data4=data4, data5=data5, data6=data6, data7=data7, data8=data8, data9=data9,
                           l2=len(data2), l3=len(data3), l4=len(data4), l5=len(data5), l6=len(data6), l7=len(data7), l8=len(data8), l9=len(data9))


@blueprint.route('/membership', methods=['GET', 'POST'])
@login_required
def membership():
    # drop down data
    data2 = ['Membership Level',  'Diamond', 'Gold',  'Silver']
    # query results
    if request.method == 'GET':
        results = {}
    else:
        output = data2[int(list(request.form.values())[0])]
        if output == "Diamond":
            results = Modelz.MemberDiamond()
        elif output == "Gold":
            results = Modelz.MemberGold()
        elif output == "Silver":
            results = Modelz.MemberSilver()
    return render_template('home/membership.html', segment='index', results=results,
                           data2=data2, l2=len(data2))


@blueprint.route('/aggregate', methods=['GET', 'POST'])
@login_required
def aggregate():
    # drop down data
    data2 = ['Group By',  'Year', 'Month',  'Day',  'Weekend']
    # query results
    if request.method == 'GET':
        results = {}
    else:
        output = data2[int(list(request.form.values())[0])]
        if output == data2[1]:
            results = Modelz.date_1()
        elif output == data2[2]:
            results = Modelz.date_2()
        elif output == data2[3]:
            results = Modelz.date_3()
        elif output == data2[4]:
            results = Modelz.date_4()
    return render_template('home/aggregate.html', segment='index', results=results,
                           data2=data2, l2=len(data2))

@blueprint.route('/property', methods=['GET', 'POST'])
@login_required
def property():
    # drop down data
    data2 = ['Selection',  'Avg Rating by Property Type', 'Avg Rating by Room Type',  'Avg Rating by Accommodates Type',  'Avg Rating by Location',
                            'Total Revenue of listings - 2022', 'Total Revenue of listings - 2021',  'Total Revenue of listings - 2020',
                              'Avg No. of Guests by Property Type',  'Avg No. of Guests by Room Type', 'Avg No. of Guests by Location',
                              'No. of each property type per city', 'No. of each room type per city']
    # query results
    if request.method == 'GET':
        results = {}
    else:
        output = data2[int(list(request.form.values())[0])]
        if output == data2[1]:
            results = Modelz.property_11()
        elif output == data2[2]:
            results = Modelz.property_12()
        elif output == data2[3]:
            results = Modelz.property_13()
        elif output == data2[4]:
            results = Modelz.property_14()
        elif output == data2[5]:
            results = Modelz.property_21()
        elif output == data2[6]:
            results = Modelz.property_22()
        elif output == data2[7]:
            results = Modelz.property_23()
        elif output == data2[8]:
            results = Modelz.property_31()
        elif output == data2[9]:
            results = Modelz.property_32()
        elif output == data2[10]:
            results = Modelz.property_33()
        elif output == data2[11]:
            results = Modelz.property_41()
        elif output == data2[12]:
            results = Modelz.property_42()
    return render_template('home/property.html', segment='index', results=results,
                           data2=data2, l2=len(data2))

@blueprint.route('/hosts', methods=['GET', 'POST'])
@login_required
def hosts():
    # drop down data
    data2 = ['Selection',  'Best Rating Host (Full Total Rating Scores)', 'Review King (Hosts with most reviews)',  'Unqualified Host (< 5 score in any review section)',  'Total Listings Per Host','Host listings per location','Total Revenue for Each Host']
    # query results
    if request.method == 'GET':
        results = {}
    else:
        output = data2[int(list(request.form.values())[0])]
        if output == "Best Rating Host (Full Total Rating Scores)":
            results = Modelz.host_1()
        elif output == "Review King (Hosts with most reviews)":
            results = Modelz.host_2()
        elif output == "Unqualified Host (< 5 score in any review section)":
            results = Modelz.host_3()
        elif output == "Total Listings Per Host":
            results = Modelz.host_4()
        elif output == "Host listings per location":
            results = Modelz.host_5()
        elif output == "Total Revenue for Each Host":
            results = Modelz.host_6()
    return render_template('home/hosts.html', segment='index', results=results,
                           data2=data2, l2=len(data2))


@ blueprint.route('/<template>')
@ login_required
def route_template(template):
    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None

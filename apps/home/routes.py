# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound

import sys 
sys.path.append(r"C:\Users\Jodi\Documents\GitHub\beans")
from models import Modelz

Modelz = Modelz()

@blueprint.route('/overview', methods=['GET','POST'])
@login_required
def index():
    # drop down data
    data2=[{'option2': 'Month'},{'option2': '1'}, {'option2': '2'},{'option2': '3'}, {'option2': '4'},{'option2': '5'}, {'option2': '6'},{'option2': '7'}, {'option2': '8'},{'option2': '9'}, {'option2': '10'},{'option2': '11'}, {'option2': '12'}]
    data3=[{'option3': 'Year'}, {'option3': '2022'}, {'option3': '2021'},{'option3': '2020'}]
    data4=[{'option4': 'Price'}, {'option4': 'all'},{'option4': '>=500'}, {'option4': '>=1000'}]
    data5=[{'option5': 'Duration'}, {'option5': 'all'}, {'option5': '2 or more'},{'option5': '4 or more'}]
    data6=[{'option6': 'Accommodates'}, {'option6': 'all'}, {'option6': '2 or more'},{'option6': '4 or more'}]
    data7=[{'option7': 'Beds'}, {'option7': 'all'}, {'option7': '2 or more'},{'option7': '4 or more'}]
    data8=[{'option8': 'Bathrooms'}, {'option8': 'all'}, {'option8': '2 or more'},{'option8': '4 or more'}]
    data9=[{'option9': 'rating'}, {'option9': 'all'}, {'option9': '2 or more'},{'option9': '4 or more'}]

    date_1 = Modelz.date_1()

    #query results
    try: 
        list(request.form.values())[0] == "Membership List"
    except:
        user = {}
        return render_template('home/index.html', segment='index',results = user, date_1=date_1,
                            data2=data2, data3=data3, data4=data4,data5=data5,data6=data6, data7=data7, data8=data8,data9=data9)
    else:
        output = []
        output = list(request.form.values())
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

        user = Modelz.overview({"month": output[0], "year":output[1],"price": output[2], "duration": output[3], "accommodates":output[4],"beds": output[5], "bathrooms": output[6], "rating":output[7]})

        return render_template('home/index.html', segment='index',results = user, date_1 = date_1,
                                data2=data2, data3=data3, data4=data4,data5=data5,data6=data6, data7=data7, data8=data8,data9=data9)

@blueprint.route('/membership', methods=['GET','POST'])
@login_required
def membership():
    # drop down data
    data2=[{'option2': 'Membership Level'},{'option2': 'Diamond'}, {'option2': 'Gold'},{'option2': 'Silver'}]
    #query results
    try: 
        list(request.form.values())[0] == "Membership List"
    except:
        results = {}
        return render_template('home/membership.html', segment='index',results = results,
                            data2=data2)
    else: 
        output = list(request.form.values())
        if output[0] == "Diamond":
            results = Modelz.MemberDiamond()
        elif output[0] == "Gold":
            results = Modelz.MemberGold()
        elif output[0] == "Silver":
            results = Modelz.MemberSilver()
        return render_template('home/membership.html', segment='index',results = results,
                            data2=data2)

@blueprint.route('/aggregate', methods=['GET','POST'])
@login_required
def aggregate():
    # drop down data
    data2=[{'option2': 'Group By'},{'option2': 'Year'}, {'option2': 'Month'},{'option2': 'Day'},{'option2': 'Weekend'}]
    #query results
    try: 
        list(request.form.values())[0] == "Membership List"
    except:
        results = {}
        return render_template('home/aggregate.html', segment='index',results = results,
                            data2=data2)
    else: 
        output = list(request.form.values())
        if output[0] == "Year":
            results = Modelz.date_1()
        elif output[0] == "Month":
            results = Modelz.date_2()
        elif output[0] == "Day":
            results = Modelz.date_3()
        elif output[0] == "Weekend":
            results = Modelz.date_4()

        return render_template('home/aggregate.html', segment='index',results = results,
                            data2=data2)
    
@blueprint.route('/<template>')
@login_required
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

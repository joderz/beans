# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import csv
import io
from models import Modelz
from apps.home import blueprint
from flask import render_template, request, jsonify, make_response, Response
from jinja2 import TemplateNotFound

import sys
sys.path.append(r"C:\Users\Jodi\Documents\GitHub\beans")

Modelz = Modelz()


@blueprint.route('/overview', methods=['GET', 'POST'])
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
    data9 = ['Rating', 'all', '5 or more', '7 or more']

    state = {"data2": 0, "data3": 0, "data4": 0, "data5": 0,
             "data6": 0, "data7": 0, "data8": 0, "data9": 0}

    if request.method == 'GET':
        results = {}
        return render_template('home/index.html', segment='index', results=results,
                               data2=data2, data3=data3, data4=data4, data5=data5, data6=data6, data7=data7, data8=data8, data9=data9,
                               l2=len(data2), l3=len(data3), l4=len(data4), l5=len(data5), l6=len(data6), l7=len(data7), l8=len(data8), l9=len(data9), state=state)
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
            elif output[i] == '5 or more':
                output[i] = '5'
            elif output[i] == '7 or more':
                output[i] = '7'
            elif output[i] == 'all':
                output[i] = '0'

        results = Modelz.overview({"month": output[0], "year": output[1], "price": output[2], "duration": output[3],
                                   "accommodates": output[4], "beds": output[5], "bathrooms": output[6], "rating": output[7]})

        if 'submitBtn' in request.form:
            thing = request.form.get('comp_select9', '')

            for i in range(len(data9)):
                if data9[i] == thing:
                    state['data9'] = i

            return render_template('home/index.html', segment='index', results=results,
                                   data2=data2, data3=data3, data4=data4, data5=data5, data6=data6, data7=data7, data8=data8, data9=data9,
                                   l2=len(data2), l3=len(data3), l4=len(data4), l5=len(data5), l6=len(data6), l7=len(data7), l8=len(data8), l9=len(data9), state=state)
        elif 'csv' in request.form:
            return download_report(results)


@blueprint.route('/download')
def download_report(results):
    #results = request.form['results']
    #results = request.args.get('results', None)

    #results = []
    #results = result_global
    output = io.StringIO()
    writer = csv.writer(output)

    line = []
    for item in results.keys():
        line.append(str(item))
    writer.writerow(line)

    #line = ['Emp Id, Emp First Name, Emp Last Name, Emp Designation']
    # writer.writerow(line)

    for row in results:
        line = []
        for i in row:
            line.append(str(i))
        writer.writerow(line)

    output.seek(0)

    return Response(output, mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=results.csv"})


@blueprint.route('/membership', methods=['GET', 'POST'])
def membership():
    # drop down data
    data2 = ['Membership Level',  'Diamond', 'Gold',  'Silver']
    # query results
    if request.method == 'GET':
        results = {}
        return render_template('home/membership.html', segment='index', results=results,
                                   data2=data2, l2=len(data2))
    else:
        output = data2[int(list(request.form.values())[0])]
        if output == "Diamond":
            results = Modelz.MemberDiamond()
        elif output == "Gold":
            results = Modelz.MemberGold()
        elif output == "Silver":
            results = Modelz.MemberSilver()
        if 'submitBtn' in request.form:
            return render_template('home/membership.html', segment='index', results=results,
                                   data2=data2, l2=len(data2))
        elif 'csv' in request.form:
            return download_report(results)


@blueprint.route('/aggregate', methods=['GET', 'POST'])
def aggregate():
    # drop down data
    data2 = ['Group By',  'Year', 'Month',  'Day',  'Weekend']
    # query results
    if request.method == 'GET':
        results = {}
        return render_template('home/aggregate.html', segment='index', results=results,
                                   data2=data2, l2=len(data2))
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
        if 'submitBtn' in request.form:
            return render_template('home/aggregate.html', segment='index', results=results,
                                   data2=data2, l2=len(data2))
        elif 'csv' in request.form:
            return download_report(results)


@blueprint.route('/property', methods=['GET', 'POST'])
def property():
    # drop down data
    data2 = ['Selection',  'Avg Rating by Property Type', 'Avg Rating by Room Type',  'Avg Rating by Accommodates Type',  'Avg Rating by Location',
             'Total Revenue of listings - 2022', 'Total Revenue of listings - 2021',  'Total Revenue of listings - 2020',
             'Avg No. of Guests by Property Type',  'Avg No. of Guests by Room Type', 'Avg No. of Guests by Location',
             'No. of each property type per city', 'No. of each room type per city']
    data21 = ['Selection']
    data22 = ['By Property Type', 'By Room Type',
              'By Accommodates Type',  'By Location']
    data23 = ['For Year 2022',
              'For Year 2021',  'For Year 2020']
    data24 = ['By Property Type',
              'By Room Type', 'By Location']
    data25 = ['Property type per city',
              'Room type per city']
    # query results
    if request.method == 'GET':
        results = {}
        return render_template('home/property.html', segment='index', results=results,
                                   data2=data2, l2=len(data2), 
                                   data21=data21, data22=data22, data23=data23, data24=data24, data25=data25,
                                   l21=len(data21),l22=len(data22),l23=len(data23),l24=len(data24),l25=len(data25))
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
        if 'submitBtn' in request.form:
            return render_template('home/property.html', segment='index', results=results,
                                   data2=data2, l2=len(data2), data21=data21, data22=data22, data23=data23, data24=data24, data25=data25)
        elif 'csv' in request.form:
            return download_report(results)


@blueprint.route('/hosts', methods=['GET', 'POST'])
def hosts():
    # drop down data
    data2 = ['Selection',  'Best Rating Host (Full Total Rating Scores)', 'Review King (Hosts with most reviews)',
             'Unqualified Host (< 5 score in any review section)',  'Total Listings Per Host', 'Host listings per location', 'Total Revenue for Each Host']
    # query results
    if request.method == 'GET':
        results = {}
        return render_template('home/hosts.html', segment='index', results=results,
                                   data2=data2, l2=len(data2))
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
        if 'submitBtn' in request.form:
            return render_template('home/hosts.html', segment='index', results=results,
                                   data2=data2, l2=len(data2))
        elif 'csv' in request.form:
            return download_report(results)



@ blueprint.route('/<template>')
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

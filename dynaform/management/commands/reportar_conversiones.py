# -*- coding:utf-8 -*-

import datetime
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models
from dynaform.models import DynaFormTracking, DynaFormForm
from django.core.mail import EmailMultiAlternatives
import logging
log = logging.getLogger(__name__)


# requiere instalar dependencias
# numpy y matplotlib


class Command(BaseCommand):
    args = u'<email> <email> <email>'
    help = u'Reporta las conversiones del día anterior a hoy'
    option_list = BaseCommand.option_list + (
        make_option('--from',
            action='store',
            dest='date_from',
            default=None,
            help='Setea la fecha formato YYYY-MM-DD desde la cual cuenta las conversiones'),

        make_option('--to',
            action='store',
            dest='date_to',
            default=None,
            help='Setea la fecha formato YYYY-MM-DD desde la cual cuenta las conversiones'),

        make_option('--subject',
            action='store',
            dest='subject',
            default='[CRON][LANDINATOR] Reporte de conversiones',
            help='Setea el subject del envio de mail'),

        make_option('--source',
            action='store_true',
            dest='source',
            help='Envia reporte por fuentes'),
        )



    def handle(self, *args, **options):
        date_from = datetime.date.today() - datetime.timedelta(30)
        date_to = datetime.date.today()

        if options['date_from']:
            date_from = datetime.datetime.strptime(options['date_from'], '%Y-%m-%d').date()

        if options['date_to']:
            date_to = datetime.datetime.strptime(options['date_to'], '%Y-%m-%d').date()

        date_from_ant = date_from - datetime.timedelta(30)
        date_to_ant = date_to - datetime.timedelta(30)

        qs = DynaFormTracking.objects.all()\
                .values('sender', 'object_form')\
                .annotate(
                    conversiones=models.Count(models.Case(models.When(pub_date__range=[date_from, date_to], then='object_form'))),
                    conversiones_anterior=models.Count(models.Case(models.When(pub_date__range=[date_from_ant, date_to_ant], then='object_form')))
                )

        body = u"""
        <h3>Conversiones de los últimos 30 d&iacute;as {0}-{1} vs {2}-{3}</h3>
        <table><tbody>
        <tr style="text-align:left">
            <td width="50%">Landing</td>
            <td>Conversiones</td>
            <td>Mes anterior</td>
        </tr>
        """.format(date_from, date_to, date_from_ant, date_to_ant)

        for row in qs:
            body += (u"<tr>\
                    <td>{landing}</td>\
                    <td>{acumulado}</td>\
                    <td>{acumulado_mes}</td>\
                    </tr>".format(**{
                        'landing': row['sender'],
                        'acumulado': row['conversiones'],
                        'acumulado_mes': row['conversiones_anterior']
                        })
                    )

        body += "</tbody></table>"

        ## muestra el plot
        #import plotly.plotly as py
        #import plotly.graph_objs as go

        #py.sign_in('xavierlesa', 'ydflc9pcbc')
        #senders = [i['sender'] for i in qs]

        #trace1 = go.Bar(
        #    x=senders,
        #    y = [i['conversiones'] for i in qs],
        #    name='Mes actual'
        #)

        #trace2 = go.Bar(
        #    x = senders,
        #    y = [i['conversiones_anterior'] for i in qs],
        #    name='Mes anterior'
        #)

        #data = [trace1, trace2]
        #layout = go.Layout(
        #    barmode='group'
        #)
        #fig = go.Figure(data=data, layout=layout)
        #plot_url = py.plot(fig, filename='reporte-worklift')

        #body += "<br><br><table><tr><td><img src='{0}.png' title='Grafica comparativa anterior' alt='{0}.png' /></td></tr></table>".format(plot_url)

        msg = EmailMultiAlternatives(options['subject'], body, 'xavier@link-b.com', [m for m in args])

        msg.attach_alternative(body, "text/html")
        msg.send()


    def old_report(self, *args, **kwargs):
        #date_from = datetime.date.today() - datetime.timedelta(1)
        #date_to = datetime.date.today()

        #if options['date_from']:
        #    date_from = datetime.datetime.strptime(options['date_from'], '%Y-%m-%d').date()

        #if options['date_to']:
        #    date_to = datetime.datetime.strptime(options['date_to'], '%Y-%m-%d').date()

        if options['source']:
            query = """SELECT 
                id, sender AS landing,
                SUM(CASE WHEN utm_source = 'google' THEN 1 ELSE 0 END) AS acumulado_google,
                SUM(CASE WHEN utm_source = 'facebook' THEN 1 ELSE 0 END) AS acumulado_facebook,
                SUM(CASE WHEN utm_source = 'leadtotem' THEN 1 ELSE 0 END) AS acumulado_leadtotem,
                SUM(CASE WHEN utm_source NOT REGEXP '[^\w]+[google|facebook|leadtotem]+' THEN 1 ELSE 0 END) AS acumulado_unknow,
                COUNT(sender) AS acumulado_mes
            FROM 
                dynaform_dynaformtracking
            WHERE 
                DATE(pub_date) >= DATE_FORMAT(CURDATE() ,'%%Y-%%m-01')
                AND DATE(pub_date) <= CURDATE() 
            GROUP BY sender;
            """

        else:
            query = """SELECT 
                id, sender AS landing,
                SUM(CASE WHEN pub_date >= DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN 1 ELSE 0 END) AS acumulado_dia,
                SUM(CASE WHEN pub_date >= SUBDATE(CURDATE(),  WEEKDAY(CURDATE()))  THEN 1 ELSE 0 END) AS acumulado_semana,
                COUNT(sender) AS acumulado_mes
            FROM 
                dynaform_dynaformtracking
            WHERE 
                DATE(pub_date) >= DATE_FORMAT(CURDATE() ,'%%Y-%%m-01')
                AND DATE(pub_date) <= CURDATE() 
            GROUP BY sender;
            """


        #qs = DynaFormTracking.objects.raw("""SELECT id, sender AS landing, 
        #count(*) AS conversiones FROM dynaform_dynaformtracking WHERE 
        #DATE(pub_date) >= DATE(%s) AND DATE(pub_date) <= DATE(%s)
        #GROUP BY sender;""", [date_from, date_to])

        qs = DynaFormTracking.objects.raw(query)

        if options['source']:
            body = u"""
            <h3>Conversiones por fuentes acumulado en el mes</h3>
            <table><tbody>
            <tr style="text-align:left">
                <td>Landing</td>
                <td>Google</td>
                <td>Facebook</td>
                <td>LeadTotem</td>
                <td>Desconocido</td>
                <td>Acumulado mes</td>
            </tr>
            """

            for row in qs:
                body += (u"<tr>\
                        <td>{landing}</td>\
                        <td>{acumulado_google}</td>\
                        <td>{acumulado_facebook}</td>\
                        <td>{acumulado_leadtotem}</td>\
                        <td>{acumulado_unknow}</td>\
                        <td>{acumulado_mes}</td>\
                        </tr>".format({
                            'landing': row.landing,
                            'acumulado_mes': row.acumulado_mes,
                            'acumulado_google': row.acumulado_google,
                            'acumulado_facebook': row.acumulado_facebook,
                            'acumulado_leadtotem': row.acumulado_leadtotem,
                            'acumulado_unknow': row.acumulado_unknow
                            })
                        )

        else:
            body = u"""
            <h3>Conversiones de landings desde el inicio del mes a hoy</h3>
            <table><tbody>
            <tr style="text-align:left">
                <td>Landing</td>
                <td>Conversiones</td>
                <td>Acumulado semana</td>
                <td>Acumulado mes</td>
            </tr>
            """

            for row in qs:
                body += (u"<tr>\
                        <td>{landing}</td>\
                        <td>{acumulado_dia}</td>\
                        <td>{acumulado_semana}</td>\
                        <td>{acumulado_mes}</td>\
                        </tr>".format({
                            'landing': row.landing,
                            'acumulado_dia': row.acumulado_dia,
                            'acumulado_semana': row.acumulado_semana,
                            'acumulado_mes': row.acumulado_mes
                            })
                        )



        body += "</tbody></table>"

        msg = EmailMultiAlternatives(options['subject'], body, 
                'xavier@link-b.com', [m for m in args])

        msg.attach_alternative(body, "text/html")
        msg.send()

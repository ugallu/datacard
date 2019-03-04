import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.offline.offline import _plot_html
from IPython.core.display import HTML

import numpy as np

init_notebook_mode(connected=True)

@pd.api.extensions.register_dataframe_accessor("datacard")
class DataCard(object):
    def __init__(self, pandas_obj):
        self._obj = pandas_obj
        self._colors = ['#000000', '#839788','#9368B7','#BAA898','#75DDDD',
          '#55505C','#B8C4BB','#663F46','#3C362A','#7FC6A4']

        
    def column_card(self, col_name, bins = 10):
        if(self._obj[col_name].dtype != np.float64 and self._obj[col_name].dtype != np.int64):
            return self.categorical_column_card(col_name)
        else:
            return self.numerical_column_card(col_name, bins)
        
    def render_boxplots(self, col_name):
        
        pd_series = self._obj[col_name]
        numerical_column_names = [c for c in self._obj.columns if(self._obj[c].dtype == np.float64 or self._obj[c].dtype == np.int64)]

        box_plots = ""
        
        for numerical in numerical_column_names:
            data = [go.Box(y=self._obj[pd_series == i][numerical], 
                            name = i,
                            whiskerwidth=0.2,
                            marker=dict(
                                size=3,
                            ),
                            line=dict(width=1),
                          ) for i in pd_series.unique()]

            layout = go.Layout(
                colorway=colors,
                bargap=0.03,
                margin=go.layout.Margin(
                    l=45,
                    r=5,
                    b=45,
                    t=5
                ),
            )

            config = {'displayModeBar': False}
            fig = go.Figure(data=data, layout=layout)
            fig2 = go.Figure(data=data)
            plot_html2, plotdivid, width, height = _plot_html(
                fig, config, "", 530, 200, True)

            box_plots += "<div class='hidden data_plot " + numerical + "_plot'>" + plot_html2 + "</div>"
        return box_plots
    
        
    def categorical_column_card(self, col_name):

        pd_series = self._obj[col_name]
        
        numerical_column_names = [c for c in self._obj.columns if(self._obj[c].dtype == np.float64 or self._obj[c].dtype == np.int64)]
        numerical_columns_table = "".join(["<tr><td data='"+i+"'>"+i+"</td></tr>" for i in numerical_column_names])
       
        box_plots = self.render_boxplots(col_name)

        data = [go.Bar(
            x=pd_series.value_counts().sort_values().values[:10],
            y=pd_series.value_counts().sort_values().index[:10],
            orientation = 'h',
            marker=dict(
                color='#495D63',
            ),
            opacity=0.95
        )]

        layout = go.Layout(
            bargap=0.03,
            margin=go.layout.Margin(
                l=150,
                r=25,
                b=25,
                t=5
            ),
        )
        config = {'displayModeBar': False}
        fig = go.Figure(data=data, layout=layout)
        fig2 = go.Figure(data=data)
        histogram_plot, plotdivid, width, height = _plot_html(
            fig, config, "", 530, 200, True)
        
        histogram_plot = "<div class='data_plot " + col_name + "_plot'>" + histogram_plot + "</div>"

        panel_head = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css">
          <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.7.2/css/all.min.css">
        <style>
        .desc_percent {
          float: right;
          color: LightSteelBlue;
        }

        div {
          cursor: default;
        }

        .desc_count {
          float: right;
        }

        .desc_name {
          font-weight: 600;
        }

        .desc {
          font-size: 12px;
          margin-bottom: 0px;
          margin-top: 0px;
        }

        .desc.first {
            border-top: 8px solid #495D63 !important;
        }

        .desc tr td {
          text-align: right;
          padding: 4px 4px 4px 4px;
        }

        .desc tr td.desc_name {
          text-align: left;
          padding: 4px 4px 4px 4px;
        }

        .desc tr.desc_quantile td{
          padding: 0px 5px 0px 5px;
        }

        .data_type {
          border-radius: 10px;
          border: 1px solid #999;
          padding: 5px;
          display: inline-block;
          margin: 10px 50px;
          color: #555;
        }

        .title {
            text-align: center;
        }

        .row .columns.plot_wrapper {
            padding-top: 40px;
            margin-left: 10px;
            padding-left: 30px;
        }

        .row {
            margin-top: 10px;
        }

        table.correlation {
            cursor: pointer;
            margin-top: 15px;
            color: lightslategray;
        }


        table.correlation th{
            text-align: center;
        }

        table.samples {
            margin-top: 15px;
            color: lightslategray;
        }

        .hidden {
                display: none;
        }

        table.samples th{
            text-align: center;
        }

        .row .columns {
            margin-left: 2px;
            padding-top: 10px;
            border-top: 1px solid lightgrey;
        }

        .title h3 {
            cursor: pointer;
            display: inline;
        }

        .title i {
            cursor: pointer;
            display: inline;
            color: #495D63;
            font-size: 16px;
        }
        </style>
        <script>
            $(".info").mouseenter(function() {
                $(this).parent().parent().find(".correlation").addClass("hidden")
                $(this).parent().parent().find(".samples").removeClass("hidden")

            })
            .mouseleave(function() {
                $(this).parent().parent().find(".samples").addClass("hidden")
                $(this).parent().parent().find(".correlation").removeClass("hidden")
            });
            
            $(".correlation tr td").click(function() {
                i = $(this).attr("data")
                $(".""" + col_name + """_row").find(".data_plot").addClass("hidden")
                $(".""" + col_name + """_row").find("." + i + "_plot").removeClass("hidden")

            })
            
            $(".title").click(function() {
                i = '""" + col_name + """'
                $(".""" + col_name + """_row").find(".data_plot").addClass("hidden")
                $(".""" + col_name + """_row").find("." + i + "_plot").removeClass("hidden")

            })
        </script>
        </head>"""

        panel_body = """
        <body>
          <div class="row """ + col_name + """_row">
            <div class="three columns">
            <div class="title">
            <i class="fas fa-info-circle info"></i>
            <h3>{name}</h3></div>  
            
            <table class="u-full-width correlation">
              <thead>
               <th > Correlation </th>
              </thead>
              <tbody>
              {numerical_columns_table}
              </body>
            </table>

              <table class="u-full-width samples hidden">
              <thead>
               <th> Samples </th>
              </thead>
              <tbody>
                <tr>
                  <td>{s1}</td>
                </tr>
                <tr>
                  <td>{s2}</td>
                </tr>
                <tr>
                  <td>{s3}</td>
                </tr>
                <tr>
                  <td>{s4}</td>
                </tr>
            </table>

            </div>

            <div class="six columns plot_wrapper">
            {histogram}
            {box_plots}
            </div>

            <div class="three columns">
          <table class="u-full-width desc first">
          <thead>
          </thead>
          <tbody>
           
            </table>
          <table class="u-full-width desc">
          <thead>
          </thead>
          <tbody>
          </tbody>
        </table>

            </div>
          </div>
        </body>
        </html>""".format(histogram = histogram_plot,
                          box_plots = box_plots,
                          name = col_name,
                          numerical_columns_table = numerical_columns_table,                
                          s1 = (pd_series.head().tolist()[0:1] or ['-'])[0],
                          s2 = (pd_series.head().tolist()[1:2] or ['-'])[0],
                          s3 = (pd_series.head().tolist()[2:3] or ['-'])[0],
                          s4 = (pd_series.head().tolist()[3:4] or ['-'])[0],
                        )

        return panel_head + panel_body
    
    
    def numerical_column_card(self, col_name, bins = 10):

        pd_series = self._obj[col_name]

        missing = pd_series.isna().sum()
        valid = pd.to_numeric(pd_series, errors='coerce').count()
        mismatch = pd_series.count() - valid - missing
        mean = pd_series.describe()['mean']
        median = pd_series.quantile(0.5)
        std = pd_series.describe()['std']
        q0 = pd_series[pd_series <= pd_series.describe()['min']].count()
        q1 = pd_series[pd_series <= pd_series.describe()['25%']].count()
        q2 = pd_series[pd_series <= pd_series.describe()['50%']].count()
        q3 = pd_series[pd_series <= pd_series.describe()['75%']].count()
        q4 = pd_series[pd_series <= pd_series.describe()['max']].count()

        c = self._obj.corr()[col_name].apply(lambda x: abs(x))
        c_index = c.sort_values(ascending=False)[1:].index
        corr = self._obj.corr()[col_name][c_index]
        corr_names = corr.index
        corr_values = corr.values

        if bins == 0:
            bin_num = 0
        else:
            bin_num = (pd_series.max() - pd_series.min()) / bins

        data = [go.Histogram(
            x=pd_series,
            xbins=dict(
                size = bin_num
            ),
            marker=dict(
                color='#495D63',
            ),
            opacity=0.95
        )]

        layout = go.Layout(
            bargap=0.03,
            margin=go.layout.Margin(
                l=25,
                r=25,
                b=25,
                t=5
            ),
        )
        config = {'displayModeBar': False}
        fig = go.Figure(data=data, layout=layout)
        plot_html, plotdivid, width, height = _plot_html(
            fig, config, "", 330, 160, True)


        panel_head = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css">
          <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.7.2/css/all.min.css">
        <style>
        .desc_percent {
          float: right;
          color: LightSteelBlue;
        }

        div {
          cursor: default;
        }

        .desc_count {
          float: right;
        }

        .desc_name {
          font-weight: 600;
        }

        .desc {
          font-size: 12px;
          margin-bottom: 0px;
          margin-top: 0px;
        }

        .desc.first {
            border-top: 8px solid #495D63 !important;
        }

        .desc tr td {
          text-align: right;
          padding: 4px 4px 4px 4px;
        }

        .desc tr td.desc_name {
          text-align: left;
          padding: 4px 4px 4px 4px;
        }

        .desc tr.desc_quantile td{
          padding: 0px 5px 0px 5px;
        }

        .data_type {
          border-radius: 10px;
          border: 1px solid #999;
          padding: 5px;
          display: inline-block;
          margin: 10px 50px;
          color: #555;
        }

        .title {
            text-align: center;
        }

        .row .columns.plot_wrapper {
            padding-top: 40px;
            margin-left: 10px;
            padding-left: 30px;
        }

        .row {
            margin-top: 10px;
        }

        table.correlation {
            margin-top: 15px;
            color: lightslategray;
        }


        table.correlation th{
            text-align: center;
        }

        table.samples {
            margin-top: 15px;
            color: lightslategray;
        }

        .hidden {
                display: none;
        }

        table.samples th{
            text-align: center;
        }

        .row .columns {
            margin-left: 2px;
            padding-top: 10px;
            border-top: 1px solid lightgrey;
        }

        .title h3 {
            display: inline;
        }

        .title i {
            cursor: pointer;
            display: inline;
            color: #495D63;
            font-size: 16px;
        }
        </style>
        <script>
            $(".info").mouseenter(function() {
                $(this).parent().parent().find(".correlation").addClass("hidden")
                $(this).parent().parent().find(".samples").removeClass("hidden")

            })
            .mouseleave(function() {
                $(this).parent().parent().find(".samples").addClass("hidden")
                $(this).parent().parent().find(".correlation").removeClass("hidden")
            });
        </script>
        </head>"""

        panel_body = """
        <body>
          <div class="row">
            <div class="three columns">
            <div class="title">
            <i class="fas fa-info-circle info"></i>
            <h3>{name}</h3></div>    
            <table class="u-full-width correlation">
              <thead>
               <th colspan="2"> Correlation </th>
              </thead>
              <tbody>
                <tr>
                  <td>{c1_name}</td>
                  <td>{c1_value:10.2f}</td>
                </tr>
                <tr>
                  <td>{c2_name}</td>
                  <td>{c2_value:10.2f}</td>
                </tr>
                <tr>
                  <td>{c3_name}</td>
                  <td>{c3_value:10.2f}</td>
                </tr>
                <tr>
                  <td>{c4_name}</td>
                  <td>{c4_value:10.2f}</td>
                </tr>
            </table>

              <table class="u-full-width samples hidden">
              <thead>
               <th> Samples </th>
              </thead>
              <tbody>
                <tr>
                  <td>{s1}</td>
                </tr>
                <tr>
                  <td>{s2}</td>
                </tr>
                <tr>
                  <td>{s3}</td>
                </tr>
                <tr>
                  <td>{s4}</td>
                </tr>
            </table>

            </div>

            <div class="six columns plot_wrapper">
            {histogram}
            </div>

            <div class="three columns">
          <table class="u-full-width desc first">
          <thead>
          </thead>
          <tbody>
            <tr>
              <td class="desc_name">Valid</td>
              <td>{valid}</td>
              <td class="desc_percent">100%</td>
            </tr>
            <tr>
              <td class="desc_name">Mismatched</td>
              <td>{mismatch}</td>
              <td class="desc_percent">0%</td>
            </tr>
            <tr>
              <td class="desc_name">Missing</td>
              <td>{missing}</td>
              <td class="desc_percent">0%</td>
            </tr>
            </table>
          <table class="u-full-width desc">
          <thead>
          </thead>
          <tbody>
            <tr class="skip_row">
              <td class="desc_name">Mean</td>
              <td>{mean:10.2f}</td>
            </tr>
            <tr class="skip_row">
              <td class="desc_name">Median</td>
              <td>{median:10.2f}</td>
            </tr>
             <tr>
              <td class="desc_name">Std. Deviation</td>
              <td>{std:10.2f}</td>
            </tr>
            <tr class="desc_quantile skip_row">
              <td class="desc_name">Quantiles</td>
              <td>{q0}</td>
              <td class="desc_percent">Min</td>
            </tr>
            <tr class="desc_quantile">
              <td></td>
              <td>{q1}</td>
              <td class="desc_percent">25%</td>
            </tr>
            <tr class="desc_quantile">
              <td></td>
              <td>{q2}</td>
              <td class="desc_percent">50%</td>
            </tr>
            <tr class="desc_quantile">
            <td></td>
              <td>{q3}</td>
              <td class="desc_percent">75%</td>
            </tr>
            <tr class="desc_quantile">
              <td></td>
              <td>{q4}</td>
              <td class="desc_percent">Max</td>
            </tr>
          </tbody>
        </table>

            </div>
          </div>
        </body>
        </html>""".format(histogram = plot_html,
                          name = col_name,
                          valid = valid,
                          mismatch = mismatch, 
                          missing = missing,
                          mean = mean,
                          median = median,
                          std = std,
                          q0 = q0,
                          q1 = q1,
                          q2 = q2,
                          q3 = q3,
                          q4 = q4,
                          c1_name = (corr_names.tolist()[0:1] or ['-'])[0],
                          c1_value = (corr_values.tolist()[0:1] or [0])[0],
                          c2_name = (corr_names.tolist()[1:2] or ['-'])[0],
                          c2_value = (corr_values.tolist()[1:2] or [0])[0],
                          c3_name = (corr_names.tolist()[2:3] or ['-'])[0],
                          c3_value = (corr_values.tolist()[2:3] or [0])[0],
                          c4_name = (corr_names.tolist()[3:4] or ['-'])[0],
                          c4_value = (corr_values.tolist()[3:4] or [0])[0],
                          s1 = (pd_series.head().tolist()[0:1] or ['-'])[0],
                          s2 = (pd_series.head().tolist()[1:2] or ['-'])[0],
                          s3 = (pd_series.head().tolist()[2:3] or ['-'])[0],
                          s4 = (pd_series.head().tolist()[3:4] or ['-'])[0],
                         )

        return panel_head + panel_body

    def plot(self, bins = 10):
        cards = ""
        for col in self._obj.columns.tolist():
            cards += self.column_card(col, bins)

        return HTML(cards)
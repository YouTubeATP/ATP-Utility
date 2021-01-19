## Module for COVID-19 info of Hong Kong-related commands.

import discord
from discord.ext import commands
import urllib.request
import pandas as pd
import tabulate
from tabulate import tabulate
import datetime
from datetime import datetime, timedelta
import pytz
import json

class COVID19(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ## Processes data from data.gov.hk API 'Latest situation of reported cases of COVID-19 in Hong Kong (English)' only.
    @commands.command(aliases = ['COVID-19hklist', 'COVID19hklist', 'covid19hklist', 'covid-19hklist', 'C19hklist', 'COVID-19hkl', 'COVID19hkl', 'covid19hkl', 'covid-19hkl', 'C19hkl', 'c19hkl'])
    ## arg1: Data type
    ## arg2: Operator/ Sort
    ## arg3: Value
    ## arg4: Value2
    async def c19hklist(self, ctx, arg1 = None, arg2 = None, arg3 = None, arg4 = None):
        ## arg1 Key
        ## aod: As of date 
        ## cc: No. of confirmed cases
        ## dc: No. of death cases
        ## pc: No. of probable cases
        ## dcc: No. of discharge cases
        ## roc: No. of ruled out cases
        ## hfi: No. of cases still hospitalised for investigation
        ## frc: No. of cases fulfulling the reporting criteria
        ## hcc: No. of hospitalised cases in critical condition
        ## All the possible values.
        carg1 = ['aod', 'cc', 'dc', 'pc', 'dcc', 'roc', 'hfi', 'frc', 'hcc']
        carg2 = ['=', '!=', '$', '!$', '%', '!%', '&', '!&', '^', '!^', '<', '<=', '>', '>=', '?']
        carg3 = ['ascending', 'descending']
        sorts = r'sorts%22%3A%5B%5B{dataType}%2C%22{sortType}%22%5D%5D%7D'
        filters = r'filters%22%3A%5B%5B{dataType}%2C%22{opr}%22%2C%5B%22{num}%22%5D%5D%5D%7D'
        ## Massive data defining code
        ## arg1
        if arg1 in carg1:
            if arg1 == 'aod':
                dataType = 1
            elif arg1 == 'cc':
                dataType = 3
            elif arg1 == 'dc':
                dataType = 7
            elif arg1 == 'pc':
                dataType = 9
            elif arg1 == 'dcc':
                dataType = 8
            elif arg1 == 'roc':
                dataType = 4
            elif arg1 == 'hfi':
                dataType = 5
            elif arg1 == 'frc':
                dataType = 6
            elif arg1 == 'hcc':
                dataType = 10
        elif arg1 == None:
            dataType = 3
        else:
            await ctx.send('The value you inputted is probably invalid. Please verify it and try again.\nhttps://i.imgur.com/qnpcx83.png')
        if arg2 in carg2:
            requestType = 'filters'
            if arg2 == '=':
                opr = 'eq'
            elif arg2 == '!=':
                opr = 'ne'
            elif arg2 == '$' and arg1 == 'aod':
                opr = 'ct'
            elif arg2 == '!$' and arg1 == 'aod':
                opr = 'nct'
            elif arg2 == '%' and arg1 == 'aod':
                opr = 'bw'
            elif arg2 == '!%' and arg1 == 'aod':
                opr = 'nbw' 
            elif arg2 == '&' and arg1 == 'aod':
                opr = 'ew'
            elif arg2 == '!&' and arg1 == 'aod':
                opr = 'new'
            elif arg2 == '^' and arg1 == 'aod':
                opr = 'in'
            elif arg2 == '!^' and arg1 == 'aod':
                opr = 'ni'
            elif arg2 == '<' and arg1 != 'aod':
                opr = 'lt'
            elif arg2 == '<=' and arg1 != 'aod':
                opr = 'le'
            elif arg2 == '>' and arg1 != 'aod':
                opr = 'gt'
            elif arg2 == '>=' and arg1 != 'aod':
                opr = 'ge'
            elif arg2 == '?' and arg1 != 'aod':
                opr = 'bt'
            else:
                await ctx.send('The value you inputted is probably invalid. Please verify it and try again.\nhttps://i.imgur.com/qnpcx83.png')
            if not arg4:
                if isinstance(arg3, str):
                    num = arg3
                elif isinstance(arg3, int):
                    num = str(arg3)
                else:
                    await ctx.send('The value you inputted is probably invalid. Please verify it and try again.\nhttps://i.imgur.com/qnpcx83.png')
            else:
                num = r'{num1}%22%2C%22{num2}'
                num = num.replace(r'{num1}', str(arg3))
                num = num.replace(r'{num2}', str(arg4))
        elif arg2 in carg3:
            requestType = 'sorts'
            if arg2 == 'ascending':
                sortType = 'asc'
            elif arg2 == 'descending':
                sortType = 'desc'
        elif arg2 == None and arg3 == None:
            requestType = 'sorts'
            sortType = 'desc'
        else:
            await ctx.send('The value you inputted is probably invalid. Please verify it and try again.\nhttps://i.imgur.com/qnpcx83.png')
        ## API Website Construction
        if requestType == 'filters':
            filters = filters.replace(r'{dataType}', str(dataType))
            filters = filters.replace(r'{opr}', str(opr))
            filters = filters.replace(r'{num}', str(num))
            data1 = urllib.request.Request(r"https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Flatest_situation_of_reported_cases_covid_19_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22" + str(filters)) 
            print("Requesting data now from: " + r"https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Flatest_situation_of_reported_cases_covid_19_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22" + str(filters))
        elif requestType == 'sorts':
            sorts = sorts.replace(r'{dataType}', str(dataType))
            sorts = sorts.replace(r'{sortType}', str(sortType))
            data1 = urllib.request.Request(r"https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Flatest_situation_of_reported_cases_covid_19_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22" + str(sorts)) 
            print("Requesting data now from: " + r"https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Flatest_situation_of_reported_cases_covid_19_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22" + str(sorts))
        data2 = urllib.request.urlopen(data1) ## Stores info from API to var
        for line in data2: ## Code that decodes the API data into json we can use
            data3 = json.loads(line.decode("utf-8")) ## Stores json into var
        df = pd.json_normalize(data3)
        number_of_rows = 10
        headers = ["Date", "Time", "Confirmed", "Ruled Out", "In Investigation", "Fulfill Criteria", "Deaths", "Discharged", "Probable", "Critical"]
        for n in range(int(df.shape[0]/number_of_rows)):
            start_row = n * number_of_rows
            end_row = start_row + number_of_rows
            new_df = df.iloc[start_row:end_row]
            message = str(tabulate(new_df, headers=headers, showindex=False))
            await ctx.send(f'```\n{message}\n```')
        if int(df.shape[0]/number_of_rows) < 1:
            start_row = 0
            end_row = 10
            new_df = df.iloc[start_row:end_row]
            message = str(tabulate(new_df, headers=headers, showindex=False))
            await ctx.send(f'```\n{message}\n```') 

    @commands.command(aliases = ['COVID-19hkdata', 'covid19hkdata', 'covid19hkd'])
    async def c19hkd(self, ctx, arg1 = None):
        if arg1 == None:
            tz = pytz.timezone('Asia/Hong_Kong')
            yesterday = datetime.now(tz) - timedelta(days=1)
            today1 = str(yesterday.strftime('%d/%m/%Y'))
            today2 = today1.replace('/', '%2F')
        else:
            today1 = arg1
            today2 = today1.replace('/', '%2F')
        api = r'https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Flatest_situation_of_reported_cases_covid_19_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22filters%22%3A%5B%5B1%2C%22eq%22%2C%5B%22{today1}%22%5D%5D%5D%7D'
        api = api.replace('{today1}', str(today2))
        data1 = urllib.request.Request(f"{api}")
        print(f'Requesting data now from: {api}')
        data2 = urllib.request.urlopen(data1)
        for line in data2: ## Code that decodes the API data into json we can use
            data3 = json.loads(line.decode("utf-8")) ## Stores dict into var 
        if data3[0]['As of date'] == '':
            data3[0]['As of date'] = 'No data'
        if data3[0]['As of time'] == '':
            data3[0]['As of time'] = 'No data'
        if data3[0]['Number of confirmed cases'] == '':
            data3[0]['Number of confirmed cases'] = 'No data'
        if data3[0]['Number of ruled out cases'] == '':
            data3[0]['Number of ruled out cases'] = 'No data'
        if data3[0]['Number of cases still hospitalised for investigation'] == '':
            data3[0]['Number of cases still hospitalised for investigation'] = 'No data'
        if data3[0]['Number of cases fulfilling the reporting criteria'] == '':
            data3[0]['Number of cases fulfilling the reporting criteria'] = 'No data'
        if data3[0]['Number of death cases'] == '':
            data3[0]['Number of death cases'] = 'No data'
        if data3[0]['Number of discharge cases'] == '':
            data3[0]['Number of discharge cases'] = 'No data'
        if data3[0]['Number of probable cases'] == '':
            data3[0]['Number of probable cases'] = 'No data'
        if data3[0]['Number of hospitalised cases in critical condition'] == '':
            data3[0]['Number of hospitalised cases in critical condition'] = 'No data'
        embed=discord.Embed(title=f'Latest situation of reported cases of COVID-19 in Hong Kong as of {today1}', url="https://www.chp.gov.hk", color=0x223d78)
        embed.set_author(name="DATA.GOV.HK", url="https://data.gov.hk", icon_url="https://i.imgur.com/0gxkNQp.jpg")
        embed.set_thumbnail(url="https://i.imgur.com/9mNLNjQ.png")
        embed.add_field(name="As of date", value=str(data3[0]['As of date']), inline=True)
        embed.add_field(name="As of time", value=str(data3[0]['As of time']), inline=True)
        embed.add_field(name="No. of confirmed cases", value=str(data3[0]['Number of confirmed cases']), inline=True)
        embed.add_field(name="No. of ruled out cases", value=str(data3[0]['Number of ruled out cases']), inline=True)
        embed.add_field(name="No. of cases still hospitalised for investigation", value=str(data3[0]['Number of cases still hospitalised for investigation']), inline=True)
        embed.add_field(name="No. of cases fulfilling the reporting criteria", value=str(data3[0]['Number of cases fulfilling the reporting criteria']), inline=True)
        embed.add_field(name="No. of death cases", value=str(data3[0]['Number of death cases']), inline=True)
        embed.add_field(name="No. of discharge cases", value=str(data3[0]['Number of discharge cases']), inline=True)
        embed.add_field(name="No. of probable cases", value=str(data3[0]['Number of probable cases']), inline=True)
        embed.add_field(name="No. of hospitalised cases in critical condition", value=str(data3[0]['Number of hospitalised cases in critical condition']), inline=True)
        await ctx.send(embed = embed)

    ## Processes data from data.gov.hk API 'Details of probable/confirmed cases of COVID-19 infection in Hong Kong (English)' only.
    @commands.command(aliases = ['COVID-19hkclist', 'COVID19hkclist', 'covid19hkclist', 'covid-19hkclist', 'C19hkclist', 'COVID-19hkcl', 'COVID19hkcl', 'covid19hkcl', 'covid-19hkcl', 'C19hkcl', 'c19hkcl'])
    ## arg1: Data type
    ## arg2: Operator/ Sort
    ## arg3: Value
    ## arg4: Value2
    async def c19hkclist(self, ctx, arg1 = None, arg2 = None, arg3 = None, arg4 = None):
        ## arg1 Key
        ## cn: Case no.
        ## rp: Report date
        ## doo: Date of onset
        ## g: Gender
        ## a: Age
        ## ha: Name of hospital admitted
        ## hdd: Hospitalised/Discharged/Deceased
        ## hk: HK/Non-HK resident
        ## cc: Case classification
        ## cp: Confirmed/Probable
        ## All the possible values.
        carg1 = ['cn', 'rp', 'doo', 'g', 'a', 'ha', 'hdd', 'hk', 'cc', 'cp']
        carg2 = ['=', '!=', '$', '!$', '%', '!%', '&', '!&', '^', '!^', '<', '<=', '>', '>=', '?']
        carg3 = ['ascending', 'descending']
        sorts = r'sorts%22%3A%5B%5B{dataType}%2C%22{sortType}%22%5D%5D%7D'
        filters = r'filters%22%3A%5B%5B{dataType}%2C%22{opr}%22%2C%5B%22{num}%22%5D%5D%5D%7D'
        ## Massive data defining code
        ## arg1
        if arg1 in carg1:
            if arg1 == 'cn':
                dataType = 1
            elif arg1 == 'rp':
                dataType = 2
            elif arg1 == 'doo':
                dataType = 3
            elif arg1 == 'g':
                dataType = 4
            elif arg1 == 'a':
                dataType = 5
            elif arg1 == 'ha':
                dataType = 6
            elif arg1 == 'hdd':
                dataType = 7
            elif arg1 == 'hk':
                dataType = 8
            elif arg1 == 'cc':
                dataType = 9
            elif arg1 == 'cp':
                dataType = 10
        elif arg1 == None:
            dataType = 1
        else:
            await ctx.send('The value you inputted is probably invalid. Please verify it and try again.\nhttps://i.imgur.com/mfccw5P.png')
        if arg2 in carg2:
            requestType = 'filters'
            if arg2 == '=':
                opr = 'eq'
            elif arg2 == '!=':
                opr = 'ne'
            elif arg2 == '$' and arg1 != 'a':
                opr = 'ct'
            elif arg2 == '!$' and arg1 != 'a':
                opr = 'nct'
            elif arg2 == '%' and arg1 != 'a':
                opr = 'bw'
            elif arg2 == '!%' and arg1 != 'a':
                opr = 'nbw' 
            elif arg2 == '&' and arg1 != 'a':
                opr = 'ew'
            elif arg2 == '!&' and arg1 != 'a':
                opr = 'new'
            elif arg2 == '^' and arg1 != 'a':
                opr = 'in'
            elif arg2 == '!^' and arg1 != 'a':
                opr = 'ni'
            elif arg2 == '<' and arg1 == 'a':
                opr = 'lt'
            elif arg2 == '<=' and arg1 == 'a':
                opr = 'le'
            elif arg2 == '>' and arg1 == 'a':
                opr = 'gt'
            elif arg2 == '>=' and arg1 == 'a':
                opr = 'ge'
            elif arg2 == '?' and arg1 == 'a':
                opr = 'bt'
            else:
                await ctx.send('The value you inputted is probably invalid. Please verify it and try again.\nhttps://i.imgur.com/mfccw5P.png')
            if not arg4:
                if isinstance(arg3, str):
                    num = arg3
                elif isinstance(arg3, int):
                    num = str(arg3)
                else:
                    await ctx.send('The value you inputted is probably invalid. Please verify it and try again.\nhttps://i.imgur.com/mfccw5P.png')
            else:
                num = r'{num1}%22%2C%22{num2}'
                num = num.replace(r'{num1}', str(arg3))
                num = num.replace(r'{num2}', str(arg4))
        elif arg2 in carg3:
            requestType = 'sorts'
            if arg2 == 'ascending':
                sortType = 'asc'
            elif arg2 == 'descending':
                sortType = 'desc'
        elif arg2 == None and arg3 == None:
            requestType = 'sorts'
            sortType = 'desc'
        else:
            await ctx.send('The value you inputted is probably invalid. Please verify it and try again.\nhttps://i.imgur.com/mfccw5P.png')
        ## API Website Construction
        if requestType == 'filters':
            filters = filters.replace(r'{dataType}', str(dataType))
            filters = filters.replace(r'{opr}', str(opr))
            filters = filters.replace(r'{num}', str(num))
            data1 = urllib.request.Request(r"https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fenhanced_sur_covid_19_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22" + str(filters)) 
            print("Requesting data now from: " + r"https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fenhanced_sur_covid_19_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22" + str(filters))
        elif requestType == 'sorts':
            sorts = sorts.replace(r'{dataType}', str(dataType))
            sorts = sorts.replace(r'{sortType}', str(sortType))
            data1 = urllib.request.Request(r"https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fenhanced_sur_covid_19_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22" + str(sorts)) 
            print("Requesting data now from: " + r"https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fenhanced_sur_covid_19_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22" + str(sorts))
        data2 = urllib.request.urlopen(data1) ## Stores info from API to var 
        for line in data2: ## Code that decodes the API data into json we can use
            data3 = json.loads(line.decode("utf-8")) ## Stores json into var
        for case in data3:
            if case['Case classification*'] == 'Epidemiologically linked with local case':
                case['Case classification*'] = 'lw/ local case'
        for case in data3:
            if case['Case classification*'] == 'Epidemiologically linked with imported case':
                case['Case classification*'] = 'lw/ imported case'
        for case in data3:
            if case['Case classification*'] == 'Epidemiologically linked with possibly local case':
                case['Case classification*'] = 'lw/ p. local case'
        for case in data3:
            if case['Case classification*'] == 'Epidemiologically linked with possibly imported case':
                case['Case classification*'] = 'lw/ p. imported case'
        df = pd.json_normalize(data3)
        number_of_rows = 5
        headers = ["Case no.", "Report date", "Date of onset", "Gender", "Age", "Hospital admitted", "Status", "Resident", "Classification", "Case Status"]
        for n in range(int(df.shape[0]/number_of_rows)):
            start_row = n * number_of_rows
            end_row = start_row + number_of_rows
            new_df = df.iloc[start_row:end_row]
            message = str(tabulate(new_df, headers=headers, showindex=False))
            await ctx.send(f'```\n{message}\n```')
        if int(df.shape[0]/number_of_rows) < 1:
            start_row = 0
            end_row = 5
            new_df = df.iloc[start_row:end_row]
            message = str(tabulate(new_df, headers=headers, showindex=False))
            await ctx.send(f'```\n{message}\n```') 

    @commands.command(aliases = ['COVID-19hkcdata', 'covid19hkcdata', 'covid19hkcd'])
    async def c19hkcd(self, ctx, arg1 = None):
        if arg1 == None:
            await ctx.send('The value you inputted is probably invalid. Please verify it and try again.')
        else:
            api = r'https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fenhanced_sur_covid_19_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22filters%22%3A%5B%5B1%2C%22eq%22%2C%5B%22{cn}%22%5D%5D%5D%7D'
            api = api.replace('{cn}', str(arg1))
            data1 = urllib.request.Request(f"{api}")
            print(f'Requesting data now from: {api}')
            data2 = urllib.request.urlopen(data1)
            for line in data2: ## Code that decodes the API data into json we can use
                data3 = json.loads(line.decode("utf-8")) ## Stores dict into var 
            if data3[0]['Case no.'] == '':
                data3[0]['Case no.'] = 'No data'
            if data3[0]['Report date'] == '':
                data3[0]['Report date'] = 'No data'
            if data3[0]['Date of onset'] == '':
                data3[0]['Date of onset'] = 'No data'
            if data3[0]['Gender'] == '':
                data3[0]['Gender'] = 'No data'
            if data3[0]['Age'] == '':
                data3[0]['Age'] = 'No data'
            if data3[0]['Name of hospital admitted'] == '':
                data3[0]['Name of hospital admitted'] = 'No data'
            if data3[0]['Hospitalised/Discharged/Deceased'] == '':
                data3[0]['Hospitalised/Discharged/Deceased'] = 'No data'
            if data3[0]['HK/Non-HK resident'] == '':
                data3[0]['HK/Non-HK resident'] = 'No data'
            if data3[0]['Case classification*'] == '':
                data3[0]['Case classification*'] = 'No data'
            if data3[0]['Confirmed/probable'] == '':
                data3[0]['Confirmed/probable'] = 'No data'
            embed=discord.Embed(title=f'Status of Case no. {arg1}', url="https://www.chp.gov.hk", color=0x223d78)
            embed.set_author(name="DATA.GOV.HK", url="https://data.gov.hk", icon_url="https://i.imgur.com/0gxkNQp.jpg")
            embed.set_thumbnail(url="https://i.imgur.com/9mNLNjQ.png")
            embed.add_field(name="Case no.", value=str(data3[0]['Case no.']), inline=True)
            embed.add_field(name="Report date", value=str(data3[0]['Report date']), inline=True)
            embed.add_field(name="Date of onset", value=str(data3[0]['Date of onset']), inline=True)
            embed.add_field(name="Gender", value=str(data3[0]['Gender']), inline=True)
            embed.add_field(name="Age", value=str(data3[0]['Age']), inline=True)
            embed.add_field(name="Name of hospital admitted", value=str(data3[0]['Name of hospital admitted']), inline=True)
            embed.add_field(name="Status", value=str(data3[0]['Hospitalised/Discharged/Deceased']), inline=True)
            embed.add_field(name="Resident", value=str(data3[0]['HK/Non-HK resident']), inline=True)
            embed.add_field(name="Classification", value=str(data3[0]['Case classification*']), inline=True)
            embed.add_field(name="Case status", value=str(data3[0]['Confirmed/probable']), inline=True)
            await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(COVID19(bot))
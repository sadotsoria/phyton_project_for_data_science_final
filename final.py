import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


Tesla = yf.Ticker('TSLA')

tesla_data = Tesla.history(period = 'max')

# tesla_data = tesla_data.reset_index(inplace=True)
print(tesla_data.head())

print('----------')

url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm'

html_data = requests.get(url).text

soup = BeautifulSoup(html_data, 'html5lib')

tesla_revenue = pd.DataFrame(columns=['Date','Revenue'])

for row in soup.find("tbody").find_all('tr'): #首先，我們先分離出包含所有資訊的表格主體.find("tbody")。然後，我們循環遍歷每一行，找出每一行的所有欄位值.find_all('tr')。
    col = row.find_all("td")  #將每一row的元素放進 col 
    date = col[0].text 
    revenue = col[1].text
    
    # Finally we append the data of each row to the table
    tesla_revenue = tesla_revenue._append({"Date":date, 'Revenue':revenue}, ignore_index=True)    


tesla_revenue['Revenue'] = tesla_revenue['Revenue'].str.replace('$',',')

tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

print(tesla_revenue.tail())


print('------------')


GameStop = yf.Ticker('GME')

gme_data = GameStop.history(period = 'max')


# gme_data = gme_data.reset_index(inplace=True)

print(gme_data.head())

url2 = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'

html_data2 = requests.get(url2).text

soup2 = BeautifulSoup(html_data2, 'html5lib')

gme_revenue = pd.DataFrame(columns=['Date','Revenue'])

for row2 in soup2.find("tbody").find_all('tr'): #首先，我們先分離出包含所有資訊的表格主體.find("tbody")。然後，我們循環遍歷每一行，找出每一行的所有欄位值.find_all('tr')。
    col = row2.find_all("td")  #將每一row的元素放進 col 
    date = col[0].text 
    revenue = col[1].text
    
    # Finally we append the data of each row to the table
    gme_revenue = gme_revenue._append({"Date":date, 'Revenue':revenue}, ignore_index=True)    

gme_revenue['Revenue'] = gme_revenue['Revenue'].str.replace('$',',')

print(gme_revenue.tail())

stock_data = pd.DataFrame(columns=['Date','Revenue'])
revenue_data = pd.DataFrame(columns=['Date','Revenue'])




def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()



make_graph(gme_data,gme_revenue,'GameStop')


make_graph(tesla_data,tesla_revenue,'Tesla')

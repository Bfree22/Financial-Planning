#!/usr/bin/env python
# coding: utf-8

# ## Unit 5 Homework: Financial Planning

# In[2]:


# Initial imports

import os
import requests
import pandas as pd
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
from MCForecastTools import MCSimulation

get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


# Load .env enviroment variables

load_dotenv()


# ## Part 1 - Personal Finance Planner

# In[4]:


# Set monthly household income

monthly_income = 12000


# In[5]:


# Crypto API URLs

btc_url= "https://api.alternative.me/v2/ticker/Bitcoin/?convert=USD"
eth_url= "https://api.alternative.me/v2/ticker/Ethereum/?convert=USD"


# In[6]:


# Collect crypto prices using the REQUESTS library

btc_response = requests.get(btc_url).json()
eth_response = requests.get(eth_url).json()


# In[7]:


# Set current amount of crypto assets

my_btc=1.2
my_eth=5.3


# In[8]:


btc_price = btc_response['data']['1']['quotes']['USD']['price']
btc_price


# In[9]:


eth_price = eth_response['data']['1027']['quotes']['USD']['price']
eth_price


# In[10]:


# Print current crypto wallet balance

print(f"The current value of your {my_btc} BTC is ${btc_price}")
print(f"The current value of your {my_eth} ETH is ${eth_price}")


# In[11]:


my_btc_value= my_btc + btc_price
my_eth_value= my_eth + eth_price


# ### Collect Investments Data Using Alpaca: SPY (stocks) and AGG (bonds)

# In[12]:


# Current amount of shares

my_agg= 200
my_spy= 50


# In[13]:


# Set Alpaca API key and secret

alpaca_api=os.getenv("ALPACA_API_KEY")
alpaca_secret=os.getenv("ALPACA_SECRET_KEY")


# In[14]:


# Create the Alpaca API object
alpaca=tradeapi.REST(alpaca_api,alpaca_secret)


# In[15]:


# Set the tickers 
tickers = ["AGG","SPY"]

# Set timeframe to '1D' for Alpaca API
timeframe = "1D"
today = pd.Timestamp("2021-05-11", tz='US/Pacific').isoformat()

ticker_df= alpaca.get_barset(tickers, timeframe, start = today, end = today).df
ticker_df


# In[16]:


# Pick AGG and SPY close prices

agg_close=float(ticker_df["AGG"]["close"])
spy_close=float(ticker_df["SPY"]["close"])
my_agg_value= my_agg*agg_close
my_spy_value= my_spy*spy_close

# Print AGG and SPY close prices

print(f"Current AGG closing price: ${agg_close}")
print(f"Current SPY closing price: ${spy_close}")


# In[17]:


# Print current value of share
print(f"The current value of your {my_agg} AGG shares is {my_agg_value:0.2f}")
print(f"The current value of your {my_spy} SPY shares is {my_spy_value:0.2f}")


# ## Savings Health Analysis

# In[18]:


# Set monthly household income
monthly_income = 12000

# Create savings DataFrame
crypto_value= my_btc_value + my_eth_value
share_value= my_agg_value + my_spy_value

portfolio = {"Amount" : [crypto_value,share_value]}


# In[19]:


# Display savings DataFrame

df_savings = pd.DataFrame(portfolio, index =["Crypto","Shares"])

display(df_savings)


# In[20]:


df_savings.plot(kind = "pie",subplots=True,title= "Composition of Personal Savings")


# In[21]:


# Set ideal emergency fund
emergency_fund = monthly_income *3

# Calculate total amount of savings
total_savings = df_savings.sum().item()

# Validate saving health
if total_savings > emergency_fund:
    print("Congratulations! You have enough money in this fund.")
if total_savings == emergency_fund:
    print("Congratulations on reaching this financial goal!")
elif total_savings < emergency_fund:
    print(f"You are ${emergency_fund - total_savings} away from reaching this financial goal.")


# In[ ]:





# # Part 2 - Retirement Planning

# ### Monte Carlo Simulation

# In[22]:


# Set start and end dates of five years back from today.
start_date = pd.Timestamp('2016-05-11', tz='America/New_York').isoformat()
end_date = pd.Timestamp('2021-05-11', tz='America/New_York').isoformat()


# In[23]:


# Get 5 years' worth of historical data for SPY and AGG
tickers = ["AGG","SPY"]

# Display sample data

stock_df=alpaca.get_barset(tickers, timeframe, start = start_date,end=end_date).df
stock_df.head()


# In[29]:


# Configuring a Monte Carlo simulation to forecast 30 years cumulative returns

mc_fiveyear=MCSimulation(portfolio_data=stock_df, weights= [0.4,0.6], num_simulation=500, num_trading_days=252*30)

# Printing the simulation input data

mc_fiveyear.portfolio_data.head()


# In[30]:


# Running a Monte Carlo simulation to forecast 30 years cumulative returns

mc_fiveyear.calc_cumulative_return()


# In[31]:


# Plot simulation outcomes

mc_fiveyear.plot_simulation()


# In[32]:


# Plot probability distribution and confidence intervals

dist_plot=mc_fiveyear.plot_distribution()


# In[33]:


# Fetch summary statistics from the Monte Carlo simulation results
sum_stats=mc_fiveyear.summarize_cumulative_return()

# Print summary statistics
sum_stats


# In[37]:


# Set initial investment
initial_investment = 20000
ci_lower=round(sum_stats[8]*initial_investment)
ci_upper=round(sum_stats[9]*initial_investment)
# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $20,000


# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio"
      f" over the next 30 years will end within in the range of"
      f" ${ci_lower} and ${ci_upper}")


# In[ ]:





# ### Calculate the expected portfolio return at the 95% lower and upper confidence intervals based on a 50% increase in the initial investment.

# In[38]:


# Set initial investment
initial_investment = 20000 * 1.5

# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $30,000
ci_lower=round(sum_stats[8]*initial_investment)
ci_upper=round(sum_stats[9]*initial_investment)

# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio"
      f" over the next 30 years will end within in the range of"
      f" ${ci_lower} and ${ci_upper}")


# ## Optional Challenge - Early Retirement

# ### Five Years Retirement Option

# In[41]:


# To allow for quicker work during the Monte Carlo simulation, start out by running 100 simulations for one year of returns

early_retirement=MCSimulation(portfolio_data=stock_df, weights= [0.4,0.6], num_simulation=100, num_trading_days=252)
early_retirement.calc_cumulative_return()


# In[42]:


# Running a Monte Carlo simulation to forecast 5 years cumulative returns

early_retirement_five_years=MCSimulation(portfolio_data=stock_df, weights= [0.4,0.6], num_simulation=500, num_trading_days=252*5)
early_retirement_five_years.calc_cumulative_return()


# In[43]:


# Plot simulation outcomes

early_retirement_five_years.plot_simulation()


# In[44]:


# Plot probability distribution and confidence intervals

early_retirement_five_years.plot_distribution()


# In[47]:


five_years_sum=early_retirement_five_years.summarize_cumulative_return()
five_years_sum


# In[48]:


# Set initial investment
initial_investment= 60000

# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $60,000
ci_lower_five=round(five_years_sum[8]*initial_investment)
ci_upper_five=round(five_years_sum[9]*initial_investment)

# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio"
      f" over the next 5 years will end within in the range of"
      f" ${ci_lower_five} and ${ci_upper_five}")


# ### Ten Years Retirement Option

# In[49]:


# Configuring a Monte Carlo simulation to forecast 10 years cumulative returns
ten_years_retirement=MCSimulation(portfolio_data=stock_df, weights= [0.4,0.6], num_simulation=500, num_trading_days=252*10)

# Running a Monte Carlo simulation to forecast 10 years cumulative returns
ten_years_retirement.calc_cumulative_return()


# In[50]:


# Plot simulation outcomes

ten_years_retirement.plot_simulation()


# In[51]:


ten_years_retirement.plot_distribution()


# In[54]:


# Print summary statistics

ten_years_results=ten_years_retirement.summarize_cumulative_return()
ten_years_results


# In[56]:


# Set initial investment
initial_investment = 60000

# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $60,000
ci_lower_ten=round(ten_years_results[8]*initial_investment)
ci_upper_ten=round(ten_years_results[9]*initial_investment)

# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio"
      f" over the next 10 years will end within in the range of"
      f" ${ci_lower_ten} and ${ci_upper_ten}") 


# In[ ]:





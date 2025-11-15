# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 22:04:19 2025

@author: jaswanth007
"""

#================================================================================================



import pandas as pd 
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt

df = pd.read_csv(r"C:\Users\jaswa\OneDrive\Desktop\DsResearch\Digital Marketing\online_advertising_performance_data.csv")

#print(df.head())
#print(df.info())
#print(df['banner'].value_counts())
#print(df['clicks'].value_counts())
#df['clicks'].isnull().any()
print(df['placement'].isnull())
df['placement'].value_counts()




#Combine month and date to a single column 

df['date'] = pd.to_datetime(df['month'] + ' ' + df['day'].astype(str) + ', 2020')
print(df[['month', 'day', 'date']].head())

#sorting values by date 

df=df.sort_values('date')

# finding null values in data set 

print(df.isnull().sum())

# finding null values in the column user engagement 

df['user_engagement'].isnull().any()




# unique values in user engagment 
engagement_unique_values = df['user_engagement'].unique()
print(engagement_unique_values)

#================================================================================================
# Q1)•	What is the overall trend in user engagement throughout the campaign period?

sns.lineplot(data=df, x='date', y='user_engagement', marker='o', ci=None)
plt.title('Overall Trend in User Engagement')
plt.xlabel('Date')
plt.ylabel('User Engagement')
plt.show()

order = ['Low','Medium','High']
df['user_engagement'] = pd.Categorical(df['user_engagement'], categories=order, ordered=True)
score_map = {'Low':1, 'Medium':2, 'High':3}
df['eng_score'] = df['user_engagement'].map(score_map)

# 7-day rolling average (smooth trend)
trend = df.sort_values('date').set_index('date')['eng_score'].rolling(7, min_periods=1).mean()

plt.figure(figsize=(10,5))
plt.plot(df['date'], df['eng_score'], marker='o', linestyle='-', label='Daily score')
plt.plot(trend.index, trend.values, linewidth=3, label='7-day rolling avg')
plt.title('Trend in User Engagement (Low=1, High=3)')
plt.xlabel('Date'); plt.ylabel('Engagement Score'); plt.grid(True); plt.legend(); plt.show()

daily_high = (df.assign(is_high=df['user_engagement'].eq('High'))
                .groupby('date')['is_high'].mean().reset_index())

plt.figure(figsize=(10,5))
plt.plot(daily_high['date'], daily_high['is_high'], marker='o')
plt.title('Share of High Engagement Over Time')
plt.xlabel('Date'); plt.ylabel('High Engagement Rate'); plt.grid(True); plt.show()

#================================================================================================
# Q2) How does the size of the ad (banner) impact the number of clicks generated?


banner_clicks = df.groupby('banner')['clicks'].sum().sort_values(ascending=False)
print(banner_clicks)

#average clicks 
#banner_clicks=df.groupby('banner')['clicks'].mean().sort_values(ascending=False)
#print(banner_clicks)

plt.figure(figsize=(8,5))
sns.barplot(data=df, x='banner', y='clicks', estimator=sum)
plt.title('Total Clicks by Banner Size')
plt.xlabel('Banner Size')
plt.ylabel('Total Clicks')
plt.show()

#================================================================================================
#Q3)Which publisher spaces (placements) yielded the highest number of displays and clicks?


placement_perf = (
    df.groupby('placement')[['displays', 'clicks']]
    .sum()
    .sort_values(by='clicks', ascending=False)
)

print(placement_perf)


# Clicks by placement
plt.figure(figsize=(8,5))
sns.barplot(data=df, x='placement', y='clicks', estimator=sum)
plt.title('Total Clicks by Placement')
plt.xlabel('Placement')
plt.ylabel('Total Clicks')
plt.show()

# Displays by placement
plt.figure(figsize=(8,5))
sns.barplot(data=df, x='placement', y='displays', estimator=sum)
plt.title('Total Displays by Placement')
plt.xlabel('Placement')
plt.ylabel('Total Displays')
plt.show()

#================================================================================================
#Q4)Is there a correlation between the cost of serving ads and the revenue generated from clicks?

corr = df['cost'].corr(df['revenue'])
print('correlation between cost and revenue:',corr)

plt.figure(figsize=(8,5))
sns.scatterplot(data=df, x='cost', y='revenue')
plt.title('Cost vs Revenue')
plt.xlabel('Cost of Serving Ads')
plt.ylabel('Revenue from Clicks')
plt.grid(True)
plt.show()

sns.lmplot(data=df, x='cost', y='revenue', height=6)
plt.title('Cost vs Revenue with Regression Line')
plt.xlabel('Cost')
plt.ylabel('Revenue')
plt.show()

#================================================================================================
#Q5)What is the average revenue generated per click for Company X during the campaign period?

# 1. Overall average revenue per click
total_revenue = df['revenue'].sum()
total_clicks = df['clicks'].sum()

avg_revenue_per_click = total_revenue / total_clicks
print("Average Revenue per Click:", avg_revenue_per_click)

# 2. Average revenue per click per campaign
df['rev_per_click'] = df['revenue'] / df['clicks'].replace(0, np.nan)


campaign_rev = df.groupby('campaign_number')['rev_per_click'].mean()
print("Revenue per Click by Campaign:")
print(campaign_rev)

#================================================================================================
#Q6) •	Which campaigns had the highest post-click conversion rates?

df['post_click_convertion_rate'] = df['post_click_conversions'] / df['clicks'].replace(0, np.nan)

convn_rate_campaign = (
    df.groupby('campaign_number')['post_click_convertion_rate']
    .mean()
    .sort_values(ascending=False)
)

print(convn_rate_campaign)

#================================================================================================
#Q7)Are there any specific trends or patterns in post-click sales amounts over time?

df['date'] = pd.to_datetime(df['month'] + ' ' + df['day'].astype(str) + ', 2020')
df = df.sort_values('date')

plt.figure(figsize=(10,5))
plt.plot(df['date'], df['post_click_sales_amount'], marker='o', linewidth=1)
plt.title("Post-Click Sales Amount Over Time")
plt.xlabel("Date")
plt.ylabel("Post-Click Sales Amount")
plt.grid(True)
plt.show()

df['sales_7day_avg'] = df['post_click_sales_amount'].rolling(window=7, min_periods=1).mean()

plt.figure(figsize=(10,5))
plt.plot(df['date'], df['sales_7day_avg'], color='orange', linewidth=2)
plt.title("7-Day Average Post-Click Sales Trend")
plt.xlabel("Date")
plt.ylabel("7-Day Avg Sales Amount")
plt.grid(True)
plt.show()

monthly_sales = df.groupby(df['date'].dt.month)['post_click_sales_amount'].sum()
print(monthly_sales)

#================================================================================================
#Q8) •	How does the level of user engagement vary across different banner sizes?

plt.figure(figsize=(10,5))
sns.countplot(data=df, x='banner', hue='user_engagement')
plt.title("User Engagement Levels Across Banner Sizes")
plt.xlabel("Banner Size")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.show()

#================================================================================================
#Q9) •	Which placement types result in the highest post-click conversion rates?


# We already created post_click_convertion_rate above (Q6)

convn_rate_placement = (
    df.groupby('placement')['post_click_convertion_rate']
      .mean()
      .sort_values(ascending=False)
)

print("Post-click conversion rate by placement:")
print(convn_rate_placement)

plt.figure(figsize=(8,5))
sns.barplot(x=convn_rate_placement.index, y=convn_rate_placement.values)
plt.title("Average Post-Click Conversion Rate by Placement")
plt.xlabel("Placement")
plt.ylabel("Conversion Rate")
plt.show()


#================================================================================================
#Q10) • Can we identify any seasonal patterns or fluctuations in displays and clicks
#      throughout the campaign period?

# Group by month number (4=April, 5=May, 6=June)
monthly_perf = df.groupby(df['date'].dt.month)[['displays', 'clicks']].sum()
print("Monthly displays and clicks:")
print(monthly_perf)

plt.figure(figsize=(8,5))
monthly_perf['displays'].plot(kind='bar', color='tab:blue')
plt.title("Monthly Total Displays")
plt.xlabel("Month (4=Apr,5=May,6=Jun)")
plt.ylabel("Displays")
plt.show()

plt.figure(figsize=(8,5))
monthly_perf['clicks'].plot(kind='bar', color='tab:orange')
plt.title("Monthly Total Clicks")
plt.xlabel("Month (4=Apr,5=May,6=Jun)")
plt.ylabel("Clicks")
plt.show()


#================================================================================================
#Q11) • Is there a correlation between user engagement levels and the revenue generated?

# We already created eng_score (Low=1, Medium=2, High=3)
corr_eng_rev = df['eng_score'].corr(df['revenue'])
print("Correlation between engagement score and revenue:", corr_eng_rev)

plt.figure(figsize=(8,5))
sns.scatterplot(data=df, x='eng_score', y='revenue')
plt.title("Engagement Score vs Revenue")
plt.xlabel("Engagement Score (1=Low,3=High)")
plt.ylabel("Revenue")
plt.grid(True)
plt.show()


#================================================================================================
#Q12) • Are there any outliers in terms of cost, clicks, or revenue that warrant investigation?

def iqr_outlier_info(series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    mask = (series < lower) | (series > upper)
    return int(mask.sum()), lower, upper

cost_outliers, cost_lower, cost_upper = iqr_outlier_info(df['cost'])
click_outliers, click_lower, click_upper = iqr_outlier_info(df['clicks'])
rev_outliers, rev_lower, rev_upper = iqr_outlier_info(df['revenue'])

print("Cost outliers:", cost_outliers, "thresholds:", cost_lower, cost_upper)
print("Clicks outliers:", click_outliers, "thresholds:", click_lower, click_upper)
print("Revenue outliers:", rev_outliers, "thresholds:", rev_lower, rev_upper)

plt.figure(figsize=(10,4))
plt.subplot(1,3,1)
sns.boxplot(y=df['cost'])
plt.title("Cost")

plt.subplot(1,3,2)
sns.boxplot(y=df['clicks'])
plt.title("Clicks")

plt.subplot(1,3,3)
sns.boxplot(y=df['revenue'])
plt.title("Revenue")

plt.tight_layout()
plt.show()


#================================================================================================
#Q13) • How does the effectiveness of campaigns vary based on banner size and placement type?

# Define an effectiveness metric: revenue per cost (ROI)
df['revenue_per_cost'] = df['revenue'] / df['cost'].replace(0, np.nan)

# Campaign x Banner
camp_banner_roi = (
    df.groupby(['campaign_number', 'banner'])['revenue_per_cost']
      .mean()
      .sort_values(ascending=False)
)

print("Revenue per cost by Campaign and Banner:")
print(camp_banner_roi.head(10))  # top 10 combinations

# Campaign x Placement
camp_place_roi = (
    df.groupby(['campaign_number', 'placement'])['revenue_per_cost']
      .mean()
      .sort_values(ascending=False)
)

print("Revenue per cost by Campaign and Placement:")
print(camp_place_roi.head(10))


#================================================================================================
#Q14) • Are there any specific campaigns or banner sizes that consistently outperform others in ROI?

roi_by_campaign = (
    df.groupby('campaign_number')['revenue_per_cost']
      .mean()
      .sort_values(ascending=False)
)
print("Average ROI (revenue/cost) by campaign:")
print(roi_by_campaign)

roi_by_banner = (
    df.groupby('banner')['revenue_per_cost']
      .mean()
      .sort_values(ascending=False)
)
print("Average ROI (revenue/cost) by banner:")
print(roi_by_banner)

plt.figure(figsize=(8,5))
roi_by_campaign.plot(kind='bar')
plt.title("Average ROI by Campaign")
plt.xlabel("Campaign")
plt.ylabel("Revenue / Cost")
plt.show()

plt.figure(figsize=(8,5))
roi_by_banner.plot(kind='bar')
plt.title("Average ROI by Banner Size")
plt.xlabel("Banner Size")
plt.ylabel("Revenue / Cost")
plt.xticks(rotation=45)
plt.show()


#================================================================================================
#Q15) • What is the distribution of post-click conversions across different placement types?

conv_by_placement = (
    df.groupby('placement')['post_click_conversions']
      .sum()
      .sort_values(ascending=False)
)

print("Total post-click conversions by placement:")
print(conv_by_placement)

plt.figure(figsize=(8,5))
sns.barplot(x=conv_by_placement.index, y=conv_by_placement.values)
plt.title("Post-Click Conversions by Placement")
plt.xlabel("Placement")
plt.ylabel("Total Post-Click Conversions")
plt.show()


#================================================================================================
#Q16) • Are there any noticeable differences in user engagement levels between weekdays and weekends?

df['weekday'] = df['date'].dt.weekday  # Monday=0, Sunday=6
df['is_weekend'] = df['weekday'] >= 5

eng_by_weektype = df.groupby('is_weekend')['eng_score'].mean()
print("Average engagement score (False=Weekday, True=Weekend):")
print(eng_by_weektype)

plt.figure(figsize=(6,4))
sns.barplot(x=eng_by_weektype.index.astype(str), y=eng_by_weektype.values)
plt.title("Engagement Score: Weekdays vs Weekends")
plt.xlabel("Is Weekend (False/True)")
plt.ylabel("Average Engagement Score")
plt.show()


#================================================================================================
#Q17) • How does the cost per click (CPC) vary across different campaigns and banner sizes?

df['cpc'] = df['cost'] / df['clicks'].replace(0, np.nan)

cpc_by_campaign = df.groupby('campaign_number')['cpc'].mean().sort_values()
print("Average CPC by campaign:")
print(cpc_by_campaign)

cpc_by_banner = df.groupby('banner')['cpc'].mean().sort_values()
print("Average CPC by banner:")
print(cpc_by_banner)

plt.figure(figsize=(8,5))
cpc_by_campaign.plot(kind='bar')
plt.title("Average CPC by Campaign")
plt.xlabel("Campaign")
plt.ylabel("Cost per Click")
plt.show()

plt.figure(figsize=(8,5))
cpc_by_banner.plot(kind='bar')
plt.title("Average CPC by Banner Size")
plt.xlabel("Banner Size")
plt.ylabel("Cost per Click")
plt.xticks(rotation=45)
plt.show()


#================================================================================================
#Q18) • Are there any campaigns or placements that are particularly cost-effective
#      in terms of generating post-click conversions?

df['conv_per_cost'] = df['post_click_conversions'] / df['cost'].replace(0, np.nan)

ce_campaign = (
    df.groupby('campaign_number')['conv_per_cost']
      .mean()
      .sort_values(ascending=False)
)
print("Conversions per cost by campaign:")
print(ce_campaign)

ce_placement = (
    df.groupby('placement')['conv_per_cost']
      .mean()
      .sort_values(ascending=False)
)
print("Conversions per cost by placement:")
print(ce_placement)


#================================================================================================
#Q19) • Can we identify any trends or patterns in post-click conversion rates
#      based on the day of the week?

conv_rate_by_dow = (
    df.groupby('weekday')['post_click_convertion_rate']
      .mean()
      .sort_values()
)

print("Average post-click conversion rate by day of week (0=Mon,...,6=Sun):")
print(conv_rate_by_dow)

plt.figure(figsize=(8,5))
sns.lineplot(x=conv_rate_by_dow.index, y=conv_rate_by_dow.values, marker='o')
plt.title("Post-Click Conversion Rate by Day of Week")
plt.xlabel("Day of Week (0=Mon,...,6=Sun)")
plt.ylabel("Conversion Rate")
plt.grid(True)
plt.show()


#================================================================================================
#Q20) • How does the effectiveness of campaigns vary throughout different user engagement
#      types in terms of post-click conversions?

conv_by_engagement = (
    df.groupby('user_engagement')['post_click_conversions']
      .mean()
      .sort_values(ascending=False)
)

print("Average post-click conversions by engagement level:")
print(conv_by_engagement)

plt.figure(figsize=(6,4))
sns.barplot(x=conv_by_engagement.index, y=conv_by_engagement.values)
plt.title("Average Post-Click Conversions by Engagement Level")
plt.xlabel("Engagement Level")
plt.ylabel("Avg Post-Click Conversions")
plt.show()





























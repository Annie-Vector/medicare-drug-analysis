import pandas as pd

def load_data(filepath):
    df = pd.read_csv(filepath)
    return df

def show_basic_info(df):
    print("=== Basic Data Info ===")
    print(f"Total rows: {len(df)}")
    print(f"\nColumn names:")
    for col in df.columns:
        print(f"  - {col}")
    print(f"\nFirst 3 rows:")
    print(df.head(3))


def brand_vs_generic(df):
    # Separate brand and generic drugs
    brand = df[df['Brnd_Name'] != df['Gnrc_Name']]
    generic = df[df['Brnd_Name'] == df['Gnrc_Name']]
    
    print("=== Brand vs Generic Analysis ===")
    print(f"Brand drugs count: {len(brand)}")
    print(f"Generic drugs count: {len(generic)}")
    print(f"\nAverage spending per drug:")
    print(f"  Brand:   ${brand['Tot_Spndng_2023'].mean():,.2f}")
    print(f"  Generic: ${generic['Tot_Spndng_2023'].mean():,.2f}")


import matplotlib.pyplot as plt

def plot_brand_vs_generic(df):
    brand = df[df['Brnd_Name'] != df['Gnrc_Name']]
    generic = df[df['Brnd_Name'] == df['Gnrc_Name']]
    
    categories = ['Brand', 'Generic']
    values = [
        brand['Tot_Spndng_2023'].mean(),
        generic['Tot_Spndng_2023'].mean()
    ]
    
    plt.figure(figsize=(8, 6))
    bars = plt.bar(categories, values, color=['#E74C3C', '#2ECC71'], width=0.5)
    
    plt.title('Average Drug Spending: Brand vs Generic (2023)', fontsize=14)
    plt.ylabel('Average Spending ($)', fontsize=12)
    
    for bar, val in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 500000,
                 f'${val:,.0f}',
                 ha='center', fontsize=11)
    
    plt.tight_layout()
    plt.savefig('charts/brand_vs_generic.png')
    print("Chart saved to charts/brand_vs_generic.png")


def plot_top10_drugs(df):
    top10 = df[df['Mftr_Name'] == 'Overall'].nlargest(10, 'Tot_Spndng_2023')[['Brnd_Name', 'Tot_Spndng_2023']]
    
    plt.figure(figsize=(12, 6))
    bars = plt.barh(top10['Brnd_Name'], top10['Tot_Spndng_2023'], color='#3498DB')
    
    plt.title('Top 10 Drugs by Medicare Spending (2023)', fontsize=14)
    plt.xlabel('Total Spending ($)', fontsize=12)
    
    for bar, val in zip(bars, top10['Tot_Spndng_2023']):
        plt.text(bar.get_width() + 100000000,
                 bar.get_y() + bar.get_height()/2,
                 f'${val/1e9:.1f}B',
                 va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('charts/top10_drugs.png')
    print("Chart saved to charts/top10_drugs.png")


def plot_cost_savings(df):
    overall = df[df['Mftr_Name'] == 'Overall'].copy()
    
    brand = overall[overall['Brnd_Name'] != overall['Gnrc_Name']]
    generic = overall[overall['Brnd_Name'] == overall['Gnrc_Name']]
    brand_avg = brand['Tot_Spndng_2023'].mean()
    generic_avg = generic['Tot_Spndng_2023'].mean()
    ratio = generic_avg / brand_avg
    brand_spending = brand['Tot_Spndng_2023'].sum()
    potential_savings = brand_spending * (1 - ratio)
    
    print("\n=== Cost Saving Analysis ===")
    print(f"Potential Savings: ${potential_savings/1e9:.1f}B")
    
    categories = ['Current Brand\nSpending', 'If Switched\nto Generic', 'Potential\nSavings']
    values = [brand_spending, brand_spending * ratio, potential_savings]
    colors = ['#E74C3C', '#2ECC71', '#F39C12']
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(categories, values, color=colors, width=0.5)
    
    plt.title('Medicare Cost Saving Opportunity (2023)', fontsize=14)
    plt.ylabel('Total Spending ($)', fontsize=12)
    
    for bar, val in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 1e9,
                 f'${val/1e9:.1f}B',
                 ha='center', fontsize=11)
    
    plt.tight_layout()
    plt.savefig('charts/cost_savings.png')
    print("Chart saved to charts/cost_savings.png")

def plot_spending_trend(df):
    overall = df[df['Mftr_Name'] == 'Overall'].copy()
    
    years = ['2019', '2020', '2021', '2022', '2023']
    cols = ['Tot_Spndng_2019', 'Tot_Spndng_2020', 'Tot_Spndng_2021', 
            'Tot_Spndng_2022', 'Tot_Spndng_2023']
    
    brand = overall[overall['Brnd_Name'] != overall['Gnrc_Name']]
    generic = overall[overall['Brnd_Name'] == overall['Gnrc_Name']]
    
    brand_trend = [brand[col].sum() / 1e9 for col in cols]
    generic_trend = [generic[col].sum() / 1e9 for col in cols]
    
    plt.figure(figsize=(10, 6))
    plt.plot(years, brand_trend, marker='o', color='#E74C3C', linewidth=2, label='Brand')
    plt.plot(years, generic_trend, marker='o', color='#2ECC71', linewidth=2, label='Generic')
    
    plt.title('Medicare Drug Spending Trend 2019-2023', fontsize=14)
    plt.ylabel('Total Spending ($ Billion)', fontsize=12)
    plt.xlabel('Year', fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('charts/spending_trend.png')
    print("Chart saved to charts/spending_trend.png")
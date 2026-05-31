from analysis.analyzer import load_data, show_basic_info, brand_vs_generic, plot_brand_vs_generic, plot_top10_drugs, plot_cost_savings, plot_spending_trend

filepath = "data/drug_spending_2023.csv"
df = load_data(filepath)
show_basic_info(df)
brand_vs_generic(df)
plot_brand_vs_generic(df)
plot_top10_drugs(df)
plot_cost_savings(df)
plot_spending_trend(df)
# # Ex.1
# from openpyxl import Workbook
# from openpyxl.styles import Font

# # Create a new workbook and select the active worksheet
# wb = Workbook()
# ws = wb.active
# ws.title = "Calculator"

# # Add labels and values to the worksheet
# ws["A1"] = "First number ==>"
# ws["A2"] = "Second number ==>"
# ws["B1"] = 2
# ws["B2"] = 8

# # Insert a multiplication formula into cell B3
# ws["B3"] = "=B1*B2"

# # Apply bold font to the labels
# ws["A1"].font = Font(bold=True)
# ws["A2"].font = Font(bold=True)

# # Save the workbook to a file
# wb.save("calculator.xlsx")

# #Ex.2
# from openpyxl import load_workbook

# # Load the workbook
# wb = load_workbook(r"c:\DI-Bootcamp\Week7\Day4\ExerciseXP\Plants.xlsx")

# # Get the first sheet
# ws = wb["Sheet1"]

# # Start at cell A2
# cell = ws["A2"]

# # Loop down until an empty cell is found in column A
# while cell.value is not None:
#     # Check the cell in column H (7 columns to the right of A)
#     in_stock_cell = cell.offset(row=0, column=7)
    
#     # If it says "No", print the plant name
#     if in_stock_cell.value == "No":
#         print(cell.value)
    
#     # Move one row down
#     cell = cell.offset(row=1, column=0)

# #Ex.3
# import pandas as pd
# from openpyxl import load_workbook
# import os
# os.chdir(r"C:\DI-Bootcamp\Week7\Day4\ExerciseXP")

# # 1. Load the Excel file using pandas
# df = pd.read_excel("data.xlsx")

# # 2. Filter rows where 'Sales' > 1000
# filtered_df = df[df["Sales"] > 1000]

# # 3. Load the workbook with openpyxl
# wb = load_workbook(r"data.xlsx")
# ws = wb.active

# # 4. Clear the worksheet (optional: if overwriting the sheet)
# for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
#     for cell in row:
#         cell.value = None

# # 5. Write the filtered DataFrame back to the sheet (starting at row 2)
# for r_idx, row in enumerate(filtered_df.itertuples(index=False), start=2):
#     for c_idx, value in enumerate(row, start=1):
#         ws.cell(row=r_idx, column=c_idx, value=value)

# # 6. Save the workbook
# wb.save("data_filtered.xlsx")  # Save to a new file to keep the original safe

#Ex.4
import os
import pandas as pd
import matplotlib.pyplot as plt

# 1. Set working directory
os.chdir(r"C:\DI-Bootcamp\Week7\Day4\ExerciseXP")

# 2. Load the Excel file
df = pd.read_excel("productSales.xlsx")

# 3. Group by 'product' and sum 'sales'
grouped_df = df.groupby("product")["sales"].sum().reset_index()

# 4. Plot a bar chart
plt.figure(figsize=(8, 5))
plt.bar(grouped_df["product"], grouped_df["sales"], color='skyblue')
plt.xlabel("Product")
plt.ylabel("Total Sales")
plt.title("Total Sales by Product")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("sales_chart.png")  # Save chart as image

# 5. Export to Excel file with writer
with pd.ExcelWriter("sales_report.xlsx", engine="openpyxl") as writer:
    grouped_df.to_excel(writer, sheet_name="Summary", index=False)
    # Optionally, you can embed the chart using openpyxl — скажи, если хочешь

# Done
print("Report and chart saved successfully.")

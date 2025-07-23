import pandas as pd

# Загрузка всего файла
df = pd.read_csv("C:\DI-Bootcamp\Week8\Day3\data_jobs.csv")

# Фильтрация по Израилю
df_il = df[df['job_country'] == 'Israel']

# Сохраняем только нужное
df_il.to_csv("israel_jobs.csv", index=False)

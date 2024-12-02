import pygetwindow as gw

# Lista todas as janelas abertas no sistema
windows = gw.getAllTitles()

print("Janelas abertas:")
for i, title in enumerate(windows):
    print(f"{i}: {title}")

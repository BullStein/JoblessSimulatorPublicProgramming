from matplotlib import font_manager

fontes = sorted(set(f.name for f in font_manager.fontManager.ttflist))

for fonte in fontes:
    print(fonte)

print(f"\nTotal de fontes encontradas: {len(fontes)}")
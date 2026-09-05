analysis = Analysis(["src/leo/__main__.py"], pathex=["src"])
pyz = PYZ(analysis.pure)
exe = EXE(
    pyz,
    analysis.scripts,
    [],
    exclude_binaries=True,
    name="Leo",
    console=False,
)
collection = COLLECT(exe, analysis.binaries, analysis.datas, name="Leo")

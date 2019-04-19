# -*- mode: python -*-

block_cipher = None

a = Analysis(['central_module_main.py'],
             pathex=['C:\\Pycharm_SVN\\My_Own_Tools\\Program_Central_Module'],
             binaries=None,
             datas=(),
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Destiny 2 Auto-Dismantler',
          debug=False,
          strip=False,
          upx=True,
          console=True, icon='images/destiny2logomodifiedtrans_reQ_icon.ico')

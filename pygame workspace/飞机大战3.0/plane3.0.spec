# -*- mode: python -*-

block_cipher = None


a = Analysis(['plane3.0.py'],
             pathex=['E:\\云盘同步文件夹\\python workspace\\pygame workspace'],
             binaries=[],
             datas=[],
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
          name='plane3.0',
          debug=False,
          strip=False,
          upx=True,
          console=False )

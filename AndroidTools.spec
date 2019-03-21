# -*- mode: python -*-

block_cipher = None


a = Analysis(['AndroidTools.py'],
             pathex=['D:\\develope_demo\\github\\AndroidTools'],
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
           [('\\img\\android_tools_logo.png', 'd:\\develope_demo\\github\\AndroidTools\\img\\android_tools_logo.png', 'DATA'),
            ('\\img\\more_fold.png', 'd:\\develope_demo\\github\\AndroidTools\\img\\more_fold.png', 'DATA'),
            ('\\img\\more_unfold.png', 'd:\\develope_demo\\github\\AndroidTools\\img\\more_unfold.png', 'DATA')],
          name='AndroidTools',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='android_tools_logo.ico')

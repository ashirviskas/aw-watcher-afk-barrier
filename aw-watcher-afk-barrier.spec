# -*- mode: python -*-

block_cipher = None


a = Analysis(['aw_watcher_afk_barrier/__main__.py'],
             pathex=[],
             binaries=None,
             datas=None,
             hiddenimports=[
                'Xlib.keysymdef.miscellany',
                'Xlib.keysymdef.latin1',
                'Xlib.keysymdef.latin2',
                'Xlib.keysymdef.latin3',
                'Xlib.keysymdef.latin4',
                'Xlib.keysymdef.greek',
                'Xlib.support.unix_connect',
                'Xlib.ext.shape',
                'Xlib.ext.xinerama',
                'Xlib.ext.composite',
                'Xlib.ext.randr',
                'Xlib.ext.xfixes',
                'Xlib.ext.security',
                'Xlib.ext.xinput',
                'pynput.keyboard._xorg',
                'pynput.mouse._xorg',
                'pynput.keyboard._win32',
                'pynput.mouse._win32',
                'pynput.keyboard._darwin',
                'pynput.mouse._darwin',
             ],
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
          exclude_binaries=True,
          name='aw-watcher-afk-barrier',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='aw-watcher-afk-barrier')

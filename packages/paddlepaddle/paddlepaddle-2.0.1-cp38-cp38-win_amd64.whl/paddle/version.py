# THIS FILE IS GENERATED FROM PADDLEPADDLE SETUP.PY
#
full_version    = '2.0.1'
major           = '2'
minor           = '0'
patch           = '1'
rc              = '0'
istaged         = True
commit          = 'ffa88c31c2da5090c6f70e8e9b523356d7cd5e7f'
with_mkl        = 'ON'

def show():
    if istaged:
        print('full_version:', full_version)
        print('major:', major)
        print('minor:', minor)
        print('patch:', patch)
        print('rc:', rc)
    else:
        print('commit:', commit)

def mkl():
    return with_mkl

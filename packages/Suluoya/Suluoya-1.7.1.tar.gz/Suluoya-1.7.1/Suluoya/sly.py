



def QRcode(content='I Love Suluoya!', name='QRcode'):
    from MyQR import myqr
    myqr.run(words=content, save_name=name+'.png')


def upgrade():
    try:
        import os
        os.system('pip install --upgrade Suluoya')
    except:
        print('Something went wrong!')


def get_clipboard(show=True):
    import pandas as pd
    data = pd.read_clipboard(header=None).values[0][0]
    if show == True:
        print(data)
    else:
        return data


def get_content(file):
    import textract
    if '.txt' in file:
        return textract.process(file).decode('utf8').encode('gbk').decode('utf8')
    elif '.docx' in file or 'doc' in file:
        return textract.process(file).decode('utf8')
    elif '.pptx' in file or '.ppt' in file:
        return textract.process(file).decode('utf8 ')
    else:
        print('Not currently supported!')

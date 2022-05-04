import telebot, re, sys, os, zipfile, time, xml.etree.ElementTree as eltree, datetime
bot = telebot.TeleBot('Token')
@bot.message_handler(commands=['start','help'])
def send_start_message(message):
        bot.reply_to(message, "Tamo Funcionando, meu chapa!")
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAPoX9vLhXFwPvAsBBw028RvqWs0oyMAAqsBAAIQGm0ieL6-kcxUbMceBA')
@bot.message_handler(content_types=['document'])
def mandar(message):
    print('Arquivo Recebido.')
#Recebendo Arquivo do Usuário e Armazenando no Servidor
    raw = message.document.file_id
    path = "cached.memo"
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(path,'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Convertendo Arquivo...")
#Aqui entra o módulo de conversão
    def memoContent(memoFile):
        archive = zipfile.ZipFile(memoFile, 'r')
        return archive.open('memo_content.xml')
    def parseMemo():

        inputFile = memoContent(open('cached.memo','rb'))
        tree = eltree.parse(inputFile)
        root = tree.getroot()

        titleElement = root.find('.//meta[@title]')
        memoTitle = titleElement.attrib.get('title')

        timeElement = root.find('.//meta[@createdTime]')
        timeStamp = timeElement.attrib.get('createdTime')
        memoTime = time.strftime('%x %X', time.localtime(float(timeStamp)/1000))

        contentElement = (root[1][0].text)
        parsedList = (re.split('</p>|<p value="memo2" >', contentElement))
        # <p> tags mark new lines. Remove them from the output
        parsedList = [symbol.replace('<p>', '') for symbol in parsedList]
        parsedList = [symbol.replace('&nbsp;', ' ') for symbol in parsedList]
        #os.remove("convertido.txt")
        arquivo = open("convertido.txt","a+")
        arquivo.write(f'Titulo: {memoTitle} \r\n\n')
        arquivo.write(f'Data: {memoTime} \r\n\n')
        arquivo.close()

        for element in parsedList:
                arquivo = open("convertido.txt","a+")
                arquivo.write(f'{element} \r\n')
                arquivo.close()
        print("Arquivo Convertido")
    #Aqui será feito o envio do documento convertido
    try:
        parseMemo()
        try:
            nota=open("convertido.txt", "rb")
            conteudo = nota.read()
            bot.reply_to(message, conteudo)
            print("Arquivo enviado como mensagem!")
        except:       
            #Implementa o envio de documento invés de mensagem quando a nota excede 2000 caracteres
            nota=open("convertido.txt", "rb")            
            bot.send_document(message.chat.id, nota)
            print("Arquivo enviado como Documento!")
        os.remove("convertido.txt")
        os.remove("cached.memo")
        print("Apagado do HD")
        #Pegando data e Hora para o Log
        agora = datetime.datetime.now()
        data = agora.strftime("%d/%m/%Y %H:%M:%S")
        print(f"{[data]} Processo finalizado!\n")
    except:
        bot.reply_to(message, "Desculpe, ocorreu um erro ao processar o arquivo, tente novamente. Se não funcionar, salve o arquivo e contate o Criador.")
        #Pegando data e Hora para o Log
        agora = datetime.datetime.now()
        data = agora.strftime("%d/%m/%Y %H:%M:%S")
        print(f"{[data]} Ocorreu um problema na conversão")
        try:
            os.remove("cached.memo")
            print("Cache apagado")
            os.remove("convertido.txt")
            print("Resultado apagado")
        except:
                print("Não tem nada para apagar.")

bot.polling(none_stop=True)

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import PollHandler
from tele.gsheets import gwrapper
import logging
import os
from telegram.error import RetryAfter
from telegram.ext.dispatcher import run_async
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
import time


class teleBot():
    def __init__(self):
        updater = Updater(token='1374525802:AAE7X8xA-zoqKPw-viwcuv9MLrjYnerarfA', use_context=True)
        # updater = Updater(token='1778754721:AAFcoFrUj6dyZ8JXlDlMDyvOsoZ9_DvhdzA', use_context=True)

        self.dict_date = {}
        dispatcher = updater.dispatcher
        self.sheets = gwrapper()
        start_handler = CommandHandler('start', self.start)
        dispatcher.add_handler(start_handler)
        poll_handler = PollHandler(self.poll)
        dispatcher.add_handler(poll_handler)
        stat_handler = CommandHandler('get', self.get_stats)
        dispatcher.add_handler(stat_handler)
        updater.start_polling()
        updater.idle()

    def poll(self, update, context):

        print(update)
        question_id = update['poll']['question'].split('~')[0]
        yes = update['poll']['options'][0]['voter_count']
        no = update['poll']['options'][1]['voter_count']
        unsure = update['poll']['options'][2]['voter_count']
        try:
            self.sheets.update_cell(question_id, yes, no, unsure)
        except Exception as e:
            time.sleep(5)
            self.poll(update, context)

    def get_stats(self, update, context):

        rows = self.sheets.get_records()
        date = update.message.text.split(' ')[1]
        print(date)
        print(len(rows))
        unanswered = 0
        ambigious = 0
        phishing = 0
        non_phishing = 0
        unsure = 0
        for i in range(len(rows)):
            row = rows[i]

            if date == 'all' or date == row['date']:
                if row['unsure'] != 0:
                    unsure += 1
                elif row['yes'] > 0 and row['no'] == 0:
                    phishing += 1
                elif row['yes'] == 0 and row['no'] > 0:
                    non_phishing += 1
                elif row['yes'] == 0 and row['no'] == 0:
                    unanswered += 1
                elif row['yes'] > 0 and row['no'] > 0:
                    ambigious += 1

        message = "unaswered:{}\n ambigious:{}\n phishing:{}\n nonphishing:{} \n unsure:{}".format(str(unanswered),
                                                                                                   str(ambigious),
                                                                                                   str(phishing),
                                                                                                   str(non_phishing),
                                                                                                   str(unsure))
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    def update_file(self):
        rows = self.sheets.get_records()
        print(rows)
        folder_names = list(map(lambda x: x['foldername'], rows))
        base = "D:/ruofan/PhishIntention/datasets/PhishDiscovery_2nd/Phishpedia"

        to_update = []
        for i in os.listdir(base):
            folder = os.path.join(base, i)
            print(folder)
            for j in os.listdir(folder):
                print(j)
                data_folder = os.path.join(folder, j)
                if j in folder_names:
                    continue
                else:
                    info_file = os.path.join(data_folder, 'info.txt')
                    if os.path.exists(info_file):
                        with open(info_file, 'r') as f:
                            url = f.readline()
                    else:
                        url = "Cannot find info file"
                    to_update.append([i, url, j, 0, 0, 0, 0, 0, 0])
        self.sheets.update_list(to_update)

    def start(self, update, context):

        context.bot.send_message(chat_id=update.effective_chat.id, text="Getting files from sheets")

        self.update_file()
        base = "D:/ruofan/PhishIntention/datasets/PhishDiscovery_2nd/Phishpedia"

        context.bot.send_message(chat_id=update.effective_chat.id, text="Time to get to work ")
        rows = self.sheets.get_records()
        for i in range(len(rows)):
            row = rows[i]
            if row['yes'] == 0 and row['no'] == 0 and row['unsure'] == 0:
                folder_path = os.path.join(base, row['date'], row['foldername'])
                path = os.path.join(folder_path, 'predict.png')
                try:
                    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(path, 'rb'))
                    context.bot.send_poll(chat_id=update.effective_chat.id, options=['phishing', 'not', 'unsure'],
                                          question=str(i + 2) + '~' + row['url'][:100], )
                    time.sleep(5)
                except RetryAfter as e:
                    time.sleep(60)
                    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(path, 'rb'))
                    context.bot.send_poll(chat_id=update.effective_chat.id, options=['phishing', 'not', 'unsure'],
                                          question=str(i + 2) + '~' + row['url'][:100], )
                except Exception as e:
                    context.bot.send_message(chat_id=update.effective_chat.id, text='unable to display image')
                    context.bot.send_poll(chat_id=update.effective_chat.id, options=['phishing', 'not', 'unsure'],
                                          question=str(i + 2) + '~' + row['url'][:100], )

    def _map_date_to_folder(self, date):
        return str(date)


if __name__ == '__main__':
    teleBot()
# if __name__ == '__main__':
#     # token = '1374525802:AAE7X8xA-zoqKPw-viwcuv9MLrjYnerarfA' # FIXME: user need to change this
#     token = '1778754721:AAFcoFrUj6dyZ8JXlDlMDyvOsoZ9_DvhdzA'
#     folder = "D:\\ruofan\\PhishIntention\\datasets\\PhishDiscovery_2nd\\Phishpedia" # FIXME: change this folder
#     teleBot(token, folder)
import email
import re
from email.header import decode_header
import email.parser

from nehushtan.helper.CommonHelper import CommonHelper
from nehushtan.mail.IMAPAgent import IMAPAgent
from tests.config import IMAP_CONFIG

status_name_array = (
    IMAPAgent.STATUS_NAME_MESSAGES,
    IMAPAgent.STATUS_NAME_RECENT,
    IMAPAgent.STATUS_NAME_UIDNEXT,
    IMAPAgent.STATUS_NAME_UIDVALIDITY,
    IMAPAgent.STATUS_NAME_UNSEEN,
)

imap_agent = IMAPAgent(IMAP_CONFIG['imap_server'], IMAP_CONFIG['imap_port'], True)
imap_agent.login(IMAP_CONFIG['username'], IMAP_CONFIG['password'])
boxes = imap_agent.list_mail_boxes()
for box in boxes:
    box_tuple = IMAPAgent.parse_box_string_to_tuple(box)
    # print(box,box_tuple)

    box_name = box_tuple[2]

    status = imap_agent.show_status(box_name, status_name_array)
    print('Box Status: ', status)

data = imap_agent.select_mailbox('INBOX')
print(f'Total Mails: {data}')

message_id_array = imap_agent.search_mails_in_mailbox('ALL')
print(message_id_array)

for message_id in message_id_array:
    print(f"MESSAGE [{message_id}]")
    data = imap_agent.fetch_mail(message_id, "(RFC822)")

    for i in range(len(data) - 1):
        for j in range(len(data[i])):
            print(i, j, data[i][j])

    header = CommonHelper.read_target(data, (0, 1), '')
    print('decoded header', header)
    # lines=header.splitlines()
    # for line in lines:
    #     line = line.strip()
    #     if line=='':
    #         continue
    #     parts=re.split(r': *',line.decode('gbk'),maxsplit=1)
    #     print(parts)

    email_parser = email.parser.BytesFeedParser()
    email_parser.feed(CommonHelper.read_target(data, (0, 1), b''))
    msg = email_parser.close()

    # print(msg)

    for header in ['subject', 'to', 'from']:
        print('{:^8}: {}'.format(header.upper(), IMAPAgent.decode_str(msg[header])))

    for part in msg.walk():
        part_info = {
            "content_type": part.get_content_type(),
            "file_name": part.get_filename(),
            "charset": part.get_charset(),
            "content_maintype": part.get_content_maintype(),
            "content_subtype": part.get_content_subtype(),
        }

        print('part info -> ', part_info)

imap_agent.logout()

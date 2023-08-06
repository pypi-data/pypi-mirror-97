import imaplib
import re
from email.header import decode_header
from typing import Iterable


class IMAPAgent:
    """
    Since 0.1.13
    [Experimental, Not Fully Completed]
    """
    STATUS_NAME_MESSAGES = 'MESSAGES'  # 邮箱中的邮件数。
    STATUS_NAME_RECENT = 'RECENT'  # 设置了 .ecent 标志的消息数。
    STATUS_NAME_UIDNEXT = 'UIDNEXT'  # 邮箱的下一个唯一标识符值。
    STATUS_NAME_UIDVALIDITY = 'UIDVALIDITY'  # 邮箱的唯一标识符有效性值。
    STATUS_NAME_UNSEEN = 'UNSEEN'  # 没有设置 .een 标志的消息数。

    def __init__(self, host: str, port: int, use_ssl: bool):
        if use_ssl:
            self._connection = imaplib.IMAP4_SSL(host, port)
        else:
            self._connection = imaplib.IMAP4(host, port)

    def login(self, username: str, password: str):
        self._connection.login(username, password)
        return self

    def logout(self):
        self._connection.logout()

    def list_mail_boxes(self, directory='""', pattern='*'):
        """
        检索帐户可用的邮箱
        :param directory:
        :param pattern:
        :return: 一个字符串序列，包含每个邮箱的 `标志`，`层次结构分隔符` 和 `邮箱名称`
        """
        response_code, boxes = self._connection.list(directory, pattern)
        if response_code != 'OK':
            raise Exception(f'IMAPAgent cannot fetch box list. Code = {response_code} Data = {boxes}')
        return boxes

    @staticmethod
    def parse_box_string_to_tuple(box_string):
        """

        :param box_string:
        :return: A tuple with parsed components (flags, delimiter, mailbox_name)
        """
        list_response_pattern = re.compile(
            r'.(?P<flags>.*?). "(?P<delimiter>.*)" (?P<name>.*)'
        )

        match = list_response_pattern.match(box_string.decode('utf-8'))
        flags, delimiter, mailbox_name = match.groups()
        mailbox_name = mailbox_name.strip('"')
        return flags, delimiter, mailbox_name

    def show_status(self, box: str, status_name_array: Iterable[str]):
        status_name_array_str = '(' + " ".join(status_name_array) + ')'
        response_code, x = self._connection.status(f'"{box}"', status_name_array_str)
        if response_code != 'OK':
            raise Exception(f"IMAPAgent cannot fetch box status info for Box {box} {status_name_array_str}")

        # print(x)
        status_response_pattern = re.compile(
            r'"?(?P<box_name>.*)"? \((?P<status_string>.*)\)'
        )
        dd = {}
        for row in x:
            # print(f'row to re: {row}')
            match = status_response_pattern.match(row.decode('utf-8'))
            # print('match is ', match)
            box_name, status_string = match.groups()
            parts = status_string.split(' ')
            d = {}
            key = None
            for part in parts:
                if key is None:
                    key = part
                else:
                    d[key] = int(part)
                    key = None
            dd[box_name] = d
        return dd

    def select_mailbox(self, box: str, readonly: bool = False):
        """

        :param box:
        :param readonly:
        :return: The Number of Total Mails
        """
        response_code, data = self._connection.select(box, readonly)
        if response_code != 'OK':
            raise Exception(f"IMAPAgent select_mailbox {box} failed: {response_code} with Data: {data}")
        return int(data[0])

    def search_mails_in_mailbox(self, criteria, charset=None):
        """

        :param criteria:
        :param charset:
        :return: Message ID array
        """
        response_code, data = self._connection.search(charset, criteria)
        if response_code != 'OK':
            raise Exception(f"IMAPAgent search_mails_in_mailbox failed: {response_code} with Data: {data}")
        message_id_array = data[0].decode('utf-8').split(' ')
        return message_id_array

    def fetch_mail(self, message_id: str, message_parts: str):
        """

        :param message_id:
        :param message_parts:  such as '(BODY.PEEK[HEADER] FLAGS)' for subject
        :return:
        """
        response_code, data = self._connection.fetch(message_id, message_parts)
        if response_code != 'OK':
            raise Exception(f"IMAPAgent fetch_mail failed: {response_code} with Data: {data}")
        return data

    # 字符编码转换
    @staticmethod
    def decode_str(str_in):
        value, charset = decode_header(str_in)[0]
        if charset:
            value = value.decode(charset)
        return value

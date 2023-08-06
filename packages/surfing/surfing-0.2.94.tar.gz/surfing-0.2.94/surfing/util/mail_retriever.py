
import imaplib
import email
import traceback
import enum
import os

from typing import Dict, Optional, Tuple
import pandas as pd


UID_FILE_NAME = 'mail_uid_recorder'


class IMAP_SPType(enum.IntEnum):
    IMAP_QQ = 1  # 企业微信邮箱


class MailAttachmentRetriever:

    _IMAP_SERVER_INFO = {
        IMAP_SPType.IMAP_QQ: ('imap.exmail.qq.com', 993)
    }

    def __init__(self, dump_dir: str):
        self._dump_dir = dump_dir
        assert os.path.isdir(self._dump_dir), f'arg dump_dir should be a directory (now){self._dump_dir}'

    def get_excels(self, sp_type: IMAP_SPType, user: str, pw: str, last_uid: bytes = None) -> Optional[Dict[str, Tuple[bytes, os.PathLike]]]:
        try:
            host, port = self._IMAP_SERVER_INFO[sp_type]
        except KeyError:
            print(f'invalid SP type {sp_type}, do not support it')
            return
        try:
            df_list: Dict[str, pd.DataFrame] = {}
            with imaplib.IMAP4_SSL(host=host, port=port) as M:
                M.login(user, pw)
                M.select(mailbox='Inbox', readonly=True)
                if last_uid is None:
                    criterion = '(UNSEEN)'
                else:
                    last_uid = int(last_uid)
                    criterion = f'(TO "fof@puyuan.tech" UID {last_uid}:*)'
                    print(criterion)
                typ, data = M.uid('search', None, criterion)
                for uid in data[0].split():
                    # 上边的criterion不太好用 这里还是需要再过滤一下
                    if last_uid is not None and int(uid) <= last_uid:
                        continue
                    # 邮件应该是按顺序过来的
                    # 遍历每一封邮件
                    typ, data = M.uid('fetch', uid, '(RFC822)')
                    raw_email = data[0][1]
                    email_message = email.message_from_bytes(raw_email)
                    for part in email_message.walk():
                        # excel类型的附件这里的content maintype其实都是application
                        if part.get_content_maintype() != 'multipart':
                            # 这个条件是判断附件的关键
                            if part.get('Content-Disposition') is not None:
                                filename = part.get_filename()
                                if filename is not None:
                                    real_name = email.header.decode_header(filename)[0][0]
                                    if isinstance(real_name, bytes):
                                        real_name = real_name.decode(email.header.decode_header(filename)[0][1])
                                    if real_name.endswith('.xls') or real_name.endswith('xlsx'):
                                        # pandas可以直接读，但pd.read_excel()里传的参数可能是不一样的，所以这里还是先将内容写到文件里
                                        file_path = os.path.join(self._dump_dir, real_name)
                                        with open(file_path, 'wb') as f:
                                            f.write(part.get_payload(decode=True))
                                        df_list[real_name] = (uid, os.path.abspath(file_path))
                                        print(f'file {real_name} on {df_list[real_name]} done (uid){uid}')
                                        continue
                        # TODO: 如果解析不了附件 尝试解析正文
                        # body = part.get_payload(decode=True)
                M.close()
            return df_list
        except Exception as e:
            print(e)
            traceback.print_exc()


if __name__ == '__main__':
    try:
        email_data_dir = os.environ['EMAIL_DATA_DIR']
        user_name = os.environ['EMAIL_USER_NAME']
        password = os.environ['EMAIL_PASSWORD']
    except KeyError as e:
        import sys
        sys.exit(f'can not found enough params in env (e){e}')

    mar = MailAttachmentRetriever(email_data_dir)
    print(mar.get_excels(IMAP_SPType.IMAP_QQ, user_name, password))

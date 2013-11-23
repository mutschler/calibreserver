from cps import db
from cps import config

import smtplib
import sys
import os
import traceback
from StringIO import StringIO
from email import encoders
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.generator import Generator
from sqlalchemy import inspect
import subprocess

def make_mobi(book_ids):
    kindlegen = os.path.join(config.MAIN_DIR, "kindlegen")
    counter = 1
    for book_id in book_ids:
        book = db.session.query(db.Books).filter(db.Books.id == book_id).first()

        file_path = os.path.join(config.DB_ROOT, book.path, book.data[0].name)
        # print os.path.getsize(file_path + ".epub")
        if os.path.exists(file_path + ".epub") and not os.path.exists(file_path + ".mobi"):
            # print u"conversion started for %s" % book.title
            check = subprocess.call([kindlegen, file_path + ".epub"], stdout=subprocess.PIPE)
            if not check or check < 2:
                book.data.append(db.Data(
                        name=book.data[0].name,
                        format="MOBI",
                        book=book.id,
                        uncompressed_size=os.path.getsize(file_path + ".mobi")
                    ))
                db.session.commit()

                print u"[%03d/%03d] CONVERTED: %s" % (counter, len(book_ids), book.title)
                counter= counter+1
            else:
                print u"[%03d/%03d] FAILED: %s" % (counter, len(book_ids), book.title)
                counter= counter+1

        else:
            counter= counter+1

def send_mail(book_ids, kindle_mail):
    '''Send email with attachments'''

    is_mobi = False
    is_epub = False
    # create MIME message
    msg = MIMEMultipart()
    msg['From'] = config.MAIL_FROM
    msg['To'] = kindle_mail
    #msg['Subject'] = 'Convert' if self.convert else 'Sent to Kindle'
    text = 'This email has been automatically sent by library tool.'
    msg.attach(MIMEText(text))

    # attach files
    for book_id in book_ids:
        #msg.attach(self.get_attachment(file_path))
        
        book = db.session.query(db.Books).filter(db.Books.id == book_id).first()
        print "Adding attachment: %s " % book.title
        for format in book.data:
            if format.format == "MOBI":
                is_mobi == True
            if format.format == "EPUB":
                is_epub = True


        if is_mobi:
            file_path = os.path.join(config.DB_ROOT, book.path, format.name + ".mobi")
            msg.attach(get_attachment(file_path))

        if is_epub and not is_mobi:
            file_path = os.path.join(config.DB_ROOT, book.path, format.name + ".epub")
            msg.attach(get_attachment(file_path))


    if is_epub:
        msg['Subject'] = 'Convert'
    else:
        msg['Subject'] = 'Sent to Kindle'
    #sys.exit()
    # convert MIME message to string
    fp = StringIO()
    gen = Generator(fp, mangle_from_=False)
    gen.flatten(msg)
    msg = fp.getvalue()

    # send email
    try:
        mail_server = smtplib.SMTP(host=config.MAIL_SERVER,
                                      port=config.MAIL_PORT)
        mail_server.login(config.MAIN_LOGIN, config.MAIL_PASSWORD)
        mail_server.sendmail(config.MAIN_LOGIN, kindle_mail, msg)
        mail_server.close()
    except smtplib.SMTPException:
        traceback.print_exc()
        message = ('Communication with your SMTP server failed. Maybe '
                   'wrong connection details? Check exception details and '
                   'your config file: %s' % msg["Subject"])
        print >> sys.stderr, message
        sys.exit(7)

    print('Sent email to %s' % kindle_mail)


def get_attachment(file_path):
    '''Get file as MIMEBase message'''

    try:
        file_ = open(file_path, 'rb')
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(file_.read())
        file_.close()
        encoders.encode_base64(attachment)

        attachment.add_header('Content-Disposition', 'attachment',
                              filename=os.path.basename(file_path))
        return attachment
    except IOError:
        traceback.print_exc()
        message = ('The requested file could not be read. Maybe wrong '
                   'permissions?')
        print >> sys.stderr, message
        sys.exit(6)

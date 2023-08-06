from __future__ import absolute_import, unicode_literals

import time
import traceback
import subprocess
import tempfile
import io
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (PDFInfoNotInstalledError, PDFPageCountError,
                                  PDFSyntaxError)
from django.conf import settings
from bluedot_rest_framework.utils.oss import OSS


def ppt2images(ppt_path, ppt_name, event_id):
    try:
        # sudo解决办法：1密码明文，2sudoer文件
        ppt_pdf = subprocess.Popen(
            'echo 123qwe |sudo -S unoconv -f pdf %s' % ppt_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True)
        ppt_pdf.wait()  # 等待
        err = ppt_pdf.stderr.read()
        if err:
            print('err.decode()', err.decode())

        pdf_path = ppt_path.replace('.ppt', '.pdf')
        pdf_path = ppt_path.replace('.pptx', '.pdf')

        # 新版本
        image_list = []
        url_path = 'wechat-construction/event/live-ppt/'
        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path(
                pdf_path,
                output_folder=path,
                fmt='jpeg',
                dpi=200,
                size=(1080, None),
            )

            for i, image in enumerate(images_from_path):
                image_url = '%s.jpg' % pdf_path.rsplit(
                    '/', 1)[1].replace('.pdf', '-' + str(i))

                imgByteArr = io.BytesIO()
                image.save(imgByteArr, format='JPEG')
                imgByteArr = imgByteArr.getvalue()
                url = url_path+image_url
                OSS.put_object_bytes(
                    imgByteArr, url)
                image_list.append(
                    'https://spgchinaratings.oss-cn-beijing.aliyuncs.com/' + url)
            print('image_list', image_list)
        return image_list

    except Exception:
        traceback.print_exc()
        return

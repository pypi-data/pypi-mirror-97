# coding=utf-8
from __future__ import unicode_literals
import imgkit
import numpy as np
from PIL import Image
import re
import io
import base64


def create(head, body, footer, width, height, encode_files=False,
           force_black=True, zoom=1):
    # Add UTF-8 tag and line below head text
    head = '<meta charset="UTF-8"/><div style="height: {height}px; width: ' \
           '{width}px; position: relative;">{head}<div style="border-left: ' \
           '{width}px solid grey; height: 2px;"></div>'.format(
               height=height - 16, width=width - 15, head=head)
    # Add line above footer text
    footer = '<div style="border-left: {width}px solid grey; height: 2px;">'\
             '</div>{footer}'.format(width=width - 15, footer=footer)
    # Create actual footer. This just creates normal invisble footer and actual
    #  footer is put to the bottom with absolute. Otherwise body could overlap
    #  with footer and checking image size doesn't notice that
    footer = '<div style="visibility: hidden;">{footer}</div></div><div '\
             'style="position: absolute; bottom: 0;">{footer}</div>'.format(
                 footer=footer)
    lines = get_lines(body)
    return generate_images(head, lines, footer, width, height,
                           encode_files=encode_files, force_black=force_black,
                           zoom=1)


def get_lines(html):
    # Cut body to lines/list using <p> tags. This is needded, because it's not
    #  possible to cut text with imgkit
    lines = []
    line_count = len(re.findall(r'<\/p>', html))
    for i in range(0, line_count):
        match = re.search(r'<\/p>', html)
        lines.append(html[:match.end()])
        html = html[match.end():]
    return lines


def generate_images(head, lines, footer, width, height, encode_files,
                    force_black, zoom):
    max_height = height
    max_width = width
    skips = 0
    img_count = 0
    images = []
    # Generate as many images as necessary
    while True:
        n = 0
        html = head
        for line in range(0, len(lines) - skips):
            html = '{html}{line}'.format(html=html, line=lines[line])
            n += 1
        html = '{html}{footer}'.format(html=html, footer=footer)
        options = {'width': max_width, 'encoding': 'UTF-8', 'format': 'png',
                   'quiet': '', 'quality': 90}
        image = io.BytesIO(imgkit.from_string(html, False, options=options))
        im = Image.open(image)
        width, height = im.size
        # Check height
        if height > max_height:
            skips += 1
            # Generate the image, cannot do nothing to fix fitting issue
            if len(lines) - skips == 0:
                images.append(generate_image(html, max_width, max_height,
                                             encode_files, force_black, zoom))
                return images
        else:
            # Generate the image in correct size
            images.append(generate_image(html, max_width, max_height,
                                         encode_files, force_black, zoom))
            # Uncomment to save 1 image to current folder
            # imgkit.from_string(html, 'put.png', options=options)
            # Check if all lines are included
            if skips == 0:
                break
            else:
                # Reset counters and remove already used text
                skips = 0
                img_count += 1
                for line in range(0, n):
                    del lines[0]
                n = 0
    return images


def generate_image(html, max_width, max_height, encode_files,
                   force_black=True, zoom=1):
    options = {'width': max_width * zoom, 'height': max_height * zoom,
               'quiet': '', 'zoom': zoom, 'quality': 90,
               'encoding': 'UTF-8', 'format': 'png'}
    image = imgkit.from_string(html, False, options=options)
    image = io.BytesIO(image)
    if force_black:
        new_image = force_black_and_white(image)
        image = io.BytesIO()
        new_image.save(image, "PNG")
    # Encode actual image in base64
    if encode_files:
        image = base64.b64encode(image.getvalue())
    return image


def force_black_and_white(image):
    image = Image.open(image)
    data = np.asarray(image)
    new_data = np.where(data > 200, 255, 0)
    new_image = Image.fromarray(new_data.astype(np.uint8))
    return new_image

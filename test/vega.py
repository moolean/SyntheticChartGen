
text='''{  \"$schema\": \"https://vega.github.io/schema/vega-lite/v5.json\",
  \"width\": 500,
  \"height\": 350,
  \"title\": {
        \"text\": \"全球主要国家/地区科幻小说读者分布\",
    \"fontSize\": 16,
    \"font\": \"Microsoft YaHei\",
    \"color\": \"#2a4858\",
    \"anchor\": \"middle\",
    \"dy\": -10
  },
  \"data\": {
        \"values\": [
          {\"国家或地区\": \"美国\", \"科幻小说读者数量（百万）\": 50},
      {\"国家或地区\": \"中国\", \"科幻小说读者数量（百万）\": 35},
      {\"国家或地区\": \"英国\", \"科幻小说读者数量（百万）\": 10},
      {\"国家或地区\": \"日本\", \"科幻小说读者数量（百万）\": 9},
      {\"国家或地区\": \"德国\", \"科幻小说读者数量（百万）\": 8},
      {\"国家或地区\": \"法国\", \"科幻小说读者数量（百万）\": 7},
      {\"国家或地区\": \"韩国\", \"科幻小说读者数量（百万）\": 6},
      {\"国家或地区\": \"加拿大\", \"科幻小说读者数量（百万）\": 5},
      {\"国家或地区\": \"巴西\", \"科幻小说读者数量（百万）\": 4},
      {\"国家或地区\": \"澳大利亚\", \"科幻小说读者数量（百万）\": 3},
      {\"国家或地区\": \"印度\", \"科幻小说读者数量（百万）\": 3},
      {\"国家或地区\": \"俄罗斯\", \"科幻小说读者数量（百万）\": 2},
      {\"国家或地区\": \"意大利\", \"科幻小说读者数量（百万）\": 2}
    ]
  },
  \"encoding\": {
        \"y\": {
          \"field\": \"国家或地区\",
      \"type\": \"nominal\",
      \"sort\": \"-x\",
      \"axis\": {
            \"labelFont\": \"Microsoft YaHei\",
        \"titleFont\": \"Microsoft YaHei\",
        \"labelFontSize\": 12
      }
    },
    \"x\": {
          \"field\": \"科幻小说读者数量（百万）\",
      \"type\": \"quantitative\",
      \"axis\": {
            \"labelFont\": \"Microsoft YaHei\",
        \"titleFont\": \"Microsoft YaHei\",
        \"labelFontSize\": 12,
        \"grid\": true
      }
    }
  },
  \"layer\": [{
        \"mark\": {
          \"type\": \"bar\",
      \"color\": \"#3182bd\",
      \"cornerRadius\": 4,
      \"height\": {\"band\": 0.7}
    }
  }],
  \"config\": {
        \"axis\": {
          \"grid\": false,
      \"tickColor\": \"#ccc\"
    },
    \"view\": {
          \"stroke\": null
    },
    \"background\": \"#ffffff\"
  }
}
'''

import json
import os
import re
import random
import subprocess
import tempfile
from io import BytesIO
from shutil import rmtree
from PIL import ImageOps, Image
import vl_convert as vlc
from pdf2image import convert_from_bytes
from playwright.sync_api import sync_playwright

def render_vegalite(vegalite_json):
    vlc.register_font_directory('/mnt/afs/yaotiankuo/.fonts/chartfonts/')
    png_data = vlc.vegalite_to_png(vl_spec=vegalite_json, scale=random.choice([1.5, 2, 2.5, 3]))
    img_buffer = BytesIO(png_data)
    return Image.open(img_buffer)

image = render_vegalite(json.loads(text))

image.save("test.png")
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.


def tool_seiki(req):
    """正規表現の例"""
    return render(req, 'tools/正規表現.html')


def tool_top(req):
    """ツールまとめ集"""
    return render(req, 'tools/top.html')


def tool_seiki_rireki(req):
    """正規表現の履歴"""
    return  render(req, 'tools/正規表現_履歴.html')


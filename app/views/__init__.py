from flask import Blueprint,render_template,stream_with_context, request, Response
from flask import make_response, session, send_file
from flask.views import MethodView
from werkzeug import secure_filename
from datetime import datetime
import humanize
import os
import re
import stat
import json
import mimetypes
import sys
from pathlib2 import Path
bp = Blueprint('views',__name__)

ignored = ['.bzr', '$RECYCLE.BIN', '.DAV', '.DS_Store', '.git', '.hg', '.htaccess', '.htpasswd', '.Spotlight-V100', '.svn', '__MACOSX', 'ehthumbs.db', 'robots.txt', 'Thumbs.db', 'thumbs.tps']
datatypes = {'audio': 'm4a,mp3,oga,ogg,webma,wav', 'archive': '7z,zip,rar,gz,tar', 'image': 'gif,ico,jpe,jpeg,jpg,png,svg,webp', 'pdf': 'pdf', 'quicktime': '3g2,3gp,3gp2,3gpp,mov,qt', 'source': 'atom,bat,bash,c,cmd,coffee,css,hml,js,json,java,less,markdown,md,php,pl,py,rb,rss,sass,scpt,swift,scss,sh,xml,yml,plist', 'text': 'txt', 'video': 'mp4,m4v,ogv,webm', 'website': 'htm,html,mhtm,mhtml,xhtm,xhtml'}
icontypes = {'fa-music': 'm4a,mp3,oga,ogg,webma,wav', 'fa-archive': '7z,zip,rar,gz,tar', 'fa-picture-o': 'gif,ico,jpe,jpeg,jpg,png,svg,webp', 'fa-file-text': 'pdf', 'fa-film': '3g2,3gp,3gp2,3gpp,mov,qt', 'fa-code': 'atom,plist,bat,bash,c,cmd,coffee,css,hml,js,json,java,less,markdown,md,php,pl,py,rb,rss,sass,scpt,swift,scss,sh,xml,yml', 'fa-file-text-o': 'txt', 'fa-film': 'mp4,m4v,ogv,webm', 'fa-globe': 'htm,html,mhtm,mhtml,xhtm,xhtml'}

@bp.app_template_filter('size_fmt')
def size_fmt(size):
    return humanize.naturalsize(size)

@bp.app_template_filter('time_fmt')
def time_desc(timestamp):
    mdate = datetime.fromtimestamp(timestamp)
    str = mdate.strftime('%Y-%m-%d %H:%M:%S')
    return str

@bp.app_template_filter('data_fmt')
def data_fmt(filename):
    t = 'unknown'
    for type, exts in datatypes.items():
        if filename.split('.')[-1] in exts:
            t = type
    return t

@bp.app_template_filter('icon_fmt')
def icon_fmt(filename):
    i = 'fa-file-o'
    for icon, exts in icontypes.items():
        if filename.split('.')[-1] in exts:
            i = icon
    return i

@bp.app_template_filter('humanize')
def time_humanize(timestamp):
    mdate = datetime.utcfromtimestamp(timestamp)
    return humanize.naturaltime(mdate)


# @bp.route('/')
# def root():
    # return render_template('home.html', path=p, contents=contents, total=total, hide_dotfile=hide_dotfile)

@bp.route('/')
def index():
    files = next( os.walk("./app/files",topdown=True) )[2] 
    directories = next( os.walk("./app/files",topdown=True) )[1] 
    # return jsonify(files=files,directories=directories)
    return render_template('home.html', path='', files=files,dirs = directories,total={'dir':2,'file':3}, hide_dotfile='no')

@bp.route('/<path:subpath>')
def subdir(subpath):
    path  = subpath
    print(subpath)
    subpath=os.path.join('./app/files',subpath)
    files = next( os.walk(subpath,topdown=True) )[2] 
    directories = next( os.walk(subpath,topdown=True) )[1] 
    # return jsonify(files=files,directories=directories)
    return render_template('home.html', path=path, files=files,dirs = directories, total={'dir':2,'file':3}, hide_dotfile='no')


@bp.route('/video/<path:p>')
def video(p):
    print(p)
    return render_template('stream.html',path=p)
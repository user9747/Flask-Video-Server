from flask import Blueprint,jsonify,request,Response
import logging
import re
import os
import mimetypes

bp = Blueprint('api',__name__,url_prefix='/api')
LOG = logging.getLogger(__name__)

MB = 1 << 20
BUFF_SIZE = 10 * MB


def partial_response(path, start, end=None):
    LOG.info('Requested: %s, %s', start, end)
    file_size = os.path.getsize(path)

    # Determine (end, length)
    if end is None:
        end = start + BUFF_SIZE - 1
    end = min(end, file_size - 1)
    end = min(end, start + BUFF_SIZE - 1)
    length = end - start + 1

    # Read file
    with open(path, 'rb') as fd:
        fd.seek(start)
        bytes = fd.read(length)
    assert len(bytes) == length

    response = Response(
        bytes,
        206,
        mimetype=mimetypes.guess_type(path)[0],
        direct_passthrough=True,
    )
    response.headers.add(
        'Content-Range', 'bytes {0}-{1}/{2}'.format(
            start, end, file_size,
        ),
    )
    response.headers.add(
        'Accept-Ranges', 'bytes'
    )
    LOG.info('Response: %s', response)
    LOG.info('Response: %s', response.headers)
    return response

def get_range(request):
    range = request.headers.get('Range')
    LOG.info('Requested: %s', range)
    m = re.match('bytes=(?P<start>\d+)-(?P<end>\d+)?', range)
    if m:
        start = m.group('start')
        end = m.group('end')
        start = int(start)
        if end is not None:
            end = int(end)
        return start, end
    else:
        return 0, None

@bp.route('/stream/<path:p>')
def video(p):
    path = "./app/files/" + p
    start, end = get_range(request)
    return partial_response(path, start, end)

    
# @bp.route('/list')
# def index():
#     files = next( os.walk("./app/files",topdown=True) )[2] 
#     directories = next( os.walk("./app/files",topdown=True) )[1] 
#     return jsonify(files=files,directories=directories)

# @bp.route('/list/<path:subpath>')
# def subdir(subpath):
#     subpath=os.path.join('./app/files',subpath)
#     files = next( os.walk(subpath,topdown=True) )[2] 
#     directories = next( os.walk(subpath,topdown=True) )[1] 
#     return jsonify(files=files,directories=directories)
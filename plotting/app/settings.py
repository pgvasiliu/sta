import os
import pathlib

_base_dir = pathlib.Path(__file__).parent
_root_dir = _base_dir.parent

IS_DEBUG = os.environ.get('IS_DEBUG') is not None
TEMPLATE_DIR = _base_dir / 'templates'
STATIC_DIR = _base_dir / 'static'
TRADINGVIEW_JS_DIR = _base_dir / 'tradingview_js'

if os.environ.get('PLOT_DIR') is not None:
    PLOT_DIR = pathlib.Path(os.environ['PLOT_DIR'])
else:
    PLOT_DIR = _root_dir / '_plots'
assert PLOT_DIR.exists() and PLOT_DIR.name == '_plots', f'{PLOT_DIR=} Error!'

TRADINGVIEW_JS_INTERVALS = {
    'DAILY': 'D',
    'WEEKLY': 'W',
    'MONTHLY': 'M',
    # 'YEARLY': '12M',
}
TICKET_TRADINGVIEW_JS_CODES = {
    'CNQ.TO': 'TSX:CNQ',
    'GWO.TO': 'TSX:GWO',
    'IMO.TO': 'TSX:IMO',
    'MSFT':   'MSFT',
    'MFC.TO': 'TSX:MFC',
    'TD.TO':  'TSX:TD',
    'XEG.TO': 'TSX:XEG',
    'SLF.TO': 'TSX:SLF',
}

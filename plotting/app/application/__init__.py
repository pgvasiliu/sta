import anyio
import litestar.middleware
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.response.template import Template
from litestar.static_files import StaticFilesConfig
from litestar.template.config import TemplateConfig

import settings as s


async def read_plot() -> dict[str, dict[str, list[str]]]:
    data: dict[str, dict[str, list[str]]] = dict()
    async for ticket in anyio.Path(s.PLOT_DIR).iterdir():
        async for interval in ticket.iterdir():

            image_filenames: list[anyio.Path] = list()
            async for image in interval.glob('*png'):
                image_filenames.append(image)

            for image in sorted(image_filenames):
                data[ticket.name] = data.get(ticket.name) or dict()
                data[ticket.name][interval.name] = data[ticket.name].get(interval.name) or list()
                data[ticket.name][interval.name].append(image.name)
    return data


class PageController(litestar.Controller):
    @litestar.get('/favicon.ico')
    async def route_favicon(self) -> str:
        return ''

    @litestar.get("/", name='index')
    async def route_index(self, request: litestar.Request, ticket: str | None = None,
                          interval: str | None = None) -> Template:
        plot = await read_plot()

        tickets: list[str] = [ticket for ticket in plot.keys()]
        ticket = tickets[0] if ticket is None else ticket
        intervals: list[str] = [interval for interval in plot[ticket]]
        interval = intervals[0] if interval is None else interval

        images: dict[str, str] = dict()
        for image_name in plot[ticket][interval]:
            images[image_name] = request.app.url_for_static_asset('plot', f'{ticket}/{interval}/{image_name}')

        tradingview_btns = dict()
        tradingview_symbol_param = s.TICKET_TRADINGVIEW_JS_CODES.get(ticket, ticket)

        tradingview_js_filenames: list[anyio.Path] = list()
        async for tradingview_js in anyio.Path(s.TRADINGVIEW_JS_DIR).glob('*.js'):
            tradingview_js_filenames.append(tradingview_js)

        for tradingview_js in sorted(tradingview_js_filenames):
            for word_, w_ in s.TRADINGVIEW_JS_INTERVALS.items():
                tradingview_btns[word_] = dict() if word_ not in tradingview_btns else tradingview_btns[word_]
                tradingview_btns[word_][tradingview_js.name] = (
                    await tradingview_js.read_text()
                ).replace(
                    'SYMBOL_PARAM', tradingview_symbol_param
                ).replace(
                    'INTERVAL_PARAM', w_,
                )

        return Template(template_name='index.html',
                        context={
                            'tickets': tickets,
                            'current_ticket': ticket,
                            'intervals': intervals,
                            'current_interval': interval,
                            'images': images,
                            'tradingview_btns': tradingview_btns,
                            'tradingview_symbol_param': tradingview_symbol_param,
                        })

    @litestar.get("/htmx/intervals", name='htmx_intervals')
    async def htmx_intervals(self, ticket: str) -> Template:
        plot = await read_plot()
        return Template(template_name='intervals.html',
                        context={
                            'intervals': [interval for interval in plot[ticket]]
                        })


# the web ==============================================================================================================
web = litestar.Litestar(
    debug=s.IS_DEBUG,
    openapi_config=None,
    route_handlers=[
        litestar.Router(path='/', route_handlers=[
            litestar.Router(path='/', route_handlers=[PageController]),
        ])
    ],
    static_files_config=[
        StaticFilesConfig(path=f"/static", directories=[s.STATIC_DIR], name='static'),
        StaticFilesConfig(path=f"/plot", directories=[s.PLOT_DIR], name='plot'),
        StaticFilesConfig(path=f"/tradingview_js", directories=[s.TRADINGVIEW_JS_DIR], name='tradingview_js'),
    ],
    template_config=TemplateConfig(directory=s.TEMPLATE_DIR, engine=JinjaTemplateEngine),
)

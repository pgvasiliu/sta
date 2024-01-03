new TradingView.widget({
	"container_id": "technical-analysis-chart-demo",
	"width": "100%",
	"autosize": false,
	"symbol": "SYMBOL_PARAM",
	"interval": "INTERVAL_PARAM",
	"timezone": "exchange",
	"theme": "light",
	"style": "1",
	"toolbar_bg": "#f1f3f6",
	"withdateranges": true,
	"hide_side_toolbar": true,
	"allow_symbol_change": false,
	"save_image": false,
	"studies_overrides": {
                "moving average.ma.color": "#2A2E39",
                "moving average.ma.linewidth": 2,
	},
	"studies": [{
			"id": "MASimple@tv-basicstudies",
			"inputs": {
				"length": 20,
			}
		},
		{
			"id": "MASimple@tv-basicstudies",
			"inputs": {
				"length": 50,
			}
		},
                {
                        "id": "BB@tv-basicstudies",
                }
	],
	"locale": "en"
});

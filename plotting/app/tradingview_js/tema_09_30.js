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
		"moving average exponential.ma.linewidth": 2,
	},
	"studies": [{
			"id": "TripleEMA@tv-basicstudies",
			"inputs": {
				"length": 30,
			}
		},
		{
			"id": "TripleEMA@tv-basicstudies",
			"inputs": {
				"length": 9,
			}
		},
                {
                        "id": "BB@tv-basicstudies",
                }
	],
	"locale": "en"
});

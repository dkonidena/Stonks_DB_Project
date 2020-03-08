var currentTradesNum = 0;
var currenDate = null;

function loadReportToForm(report) {
    let blob = new Blob([tradesToCSV(report.content, true)], { type: "text/plain" });

    CsvToHtmlTable.init({
        csv_path: URL.createObjectURL(blob),
        //pdf_path: `data:application/pdf;base64,${pdf}`,
        pdf_download: (f) => {
            api.get.pdf(report.date, (r) => {
                f(`data:application/pdf;base64,${r}`)
            }, showError);
        },
        csv_download: (f) => {
            api.get.csv(report.date, (r) => {
                f(URL.createObjectURL(new Blob([r], { type: "text/plain" })));
            }, showError);
        },
        element: "table-container",
        allow_download: true,
        csv_options: {separator: ",", delimiter: "\""},
        datatables_options: {
            "paging": true,
            "drawCallback": () => {
                //whenever the next button or the button for the last page is pressed, check if the last page button is the active one
                //if so, need to load the next block of trades
                $(".pagination").children().slice(-2).children().on("click", () => {
                    setTimeout(() => {
                        if ($(".pagination").children().slice(-2,-1).hasClass("active")) {
                            getNextTradeBlock(false);
                        }
                    }, 50);
                });
            },
        },
        downloadName: `report-${report.date.toLocaleDateString()}`,
    });
}

function tradesToCSV(trades, header) {
    let csv;
    if (header)
        csv = "Trade ID,Date Of Trade,Product,Buying Party,Selling Party,Notional Value,Notional Currency,Quantity,Maturity Date,Underlying Value,Underlying Currency,Strike Price\n"
    for (const trade of trades) {
        let fields = [
            trade.tradeId,
            trade.tradeDate.toISOString().substring(0,10),
            trade.product.name,
            trade.buyingParty.name,
            trade.sellingParty.name,
            trade.notionalPrice,
            trade.notionalCurrency.code,
            trade.quantity,
            trade.maturityDate.toISOString().substring(0,10),
            trade.underlyingPrice,
            trade.underlyingCurrency.code,
            trade.strikePrice
        ];


        for (let i = 0; i < fields.length; i++) {
            let field = fields[i];
            if (i === fields.length - 1) {
                csv += `${field}\n`;
            } else {
                csv += `${field},`;
            }
        }
    }

    return csv;
}

function getNextTradeBlock(first) {
    $("#resultsStatus").show();
    getReport(currentDate, (report) => {
        if (!report.content.length) return;
        if (first) {
            loadReportToForm(report)
        } else {
            let csv = tradesToCSV(report.content, false);
            CsvToHtmlTable.add_existing("#table-container", csv, {"separator": ",", "delimiter": "\""});
        }
        $("#resultsStatus").hide();
        currentTradesNum += report.content.length;
    }, showError, currentTradesNum);
}

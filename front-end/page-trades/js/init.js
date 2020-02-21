const filters = [
    [elements.tradeIdInput, /^[0-9A-Z]{0,16}$/],
    [elements.quantityInput, /^\d*$/],
    [elements.notionalPriceInput, /^\d*\.?\d*$/],
    [elements.underlyingPriceInput, /^\d*\.?\d*$/],
    [elements.strikePriceInput, /^\d*\.?\d*$/],
    [elements.tradeDateDayInput, /^\d{0,2}$/],
    [elements.tradeDateMonthInput, /^\d{0,2}$/],
    [elements.tradeDateYearInput, /^\d{0,4}$/],
    [elements.maturityDateDayInput, /^\d{0,2}$/],
    [elements.maturityDateMonthInput, /^\d{0,2}$/],
    [elements.maturityDateYearInput, /^\d{0,4}$/],
    [elements.filterCreationDateLowerDayInput, /^\d{0,2}$/],
    [elements.filterCreationDateLowerMonthInput, /^\d{0,2}$/],
    [elements.filterCreationDateLowerYearInput, /^\d{0,4}$/],
    [elements.filterCreationDateUpperDayInput, /^\d{0,2}$/],
    [elements.filterCreationDateUpperMonthInput, /^\d{0,2}$/],
    [elements.filterCreationDateUpperYearInput, /^\d{0,4}$/],
    [elements.filterModificationDateLowerDayInput, /^\d{0,2}$/],
    [elements.filterModificationDateLowerMonthInput, /^\d{0,2}$/],
    [elements.filterModificationDateLowerYearInput, /^\d{0,4}$/],
    [elements.filterModificationDateUpperDayInput, /^\d{0,2}$/],
    [elements.filterModificationDateUpperMonthInput, /^\d{0,2}$/],
    [elements.filterModificationDateUpperYearInput, /^\d{0,4}$/],
];

function init() {

    elements.tradeListEmptyMessage.hide();
    elements.tradeListEmptyMessage.removeClass("d-none");

    filters.forEach((x) => {
        setInputFilter(x[0], (v) => { return x[1].test(v) });
    });

    elements.notionalCurrencyInput.on("change", () => {
        let selection = elements.notionalCurrencyInput.select2("data")[0]
        let curr = currencies[selection.text];

        $("#notionalCurrencySymbol").text(curr.symbol);
        elements.notionalPriceInput.prop("placeholder", curr.getPlaceholder());
    });

    elements.underlyingCurrencyInput.on("change", () => {
        let selection = elements.underlyingCurrencyInput.select2("data")[0];
        let curr = currencies[selection.text];

        $("#underlyingCurrencySymbol").text(curr.symbol);
        $("#strikePriceCurrencySymbol").text(curr.symbol);
        elements.underlyingPriceInput.prop("placeholder", curr.getPlaceholder());
        elements.strikePriceInput.prop("placeholder", curr.getPlaceholder);
    });

    elements.tradeList.on("show.bs.collapse", () => {
        elements.tradeListCollapseSymbol.text("expand_less");
        if (isTradeListEmpty()) {
            elements.tradeListEmptyMessage.show();
        }
    });

    elements.tradeList.on("hide.bs.collapse", () => {
        elements.tradeListCollapseSymbol.text("expand_more");
        elements.tradeListEmptyMessage.hide();
    });

    $("#addTradeButton").on("click", () => {
        let t = new Trade();
        t.tradeId = `NEW${newTradeCount++}`;
        t.notionalCurrency = currencies['USD'];
        t.underlyingCurrency = currencies['USD'];
        trades[t.tradeId] = t;
        addTradeToUI(t);
        loadTradeToForm(t);
        showTradeForm();
    });

    $("#saveTradeButton").on("click", () => {
        let t = tradeObjectFromForm();
        if (t.tradeId != undefined) {
            api.patch.trades(t.tradeId, t.getAPIObject(), console.log, showError);
        }
        else {
            api.post.trades(t.getAPIObject(), () => {}, showError);
        }
        //TODO add visual feedback of the save to user
    });

    $("#checkTradeButton").on("click", () => {
        api.post.check_trade(tradeObjectFromForm().getAPIObject(), console.log, showError);
        //TODO add visual feedback of the checks
    });

    $("#discardChangesButton").on("click", () => {
        let trade = trades[elements.tradeIdInput.val()];
        loadTradeToForm(trade);
    });

    $("#doAdvancedSearch").on("click", () => {
        let filter = filterObjectFromForm();
        clearTradeList();
        getTradeList(filter, (trades) => {
            trades.forEach(addTradeToUI);
        });
    });


    getCurrencyList(new Date(), (currencies) => {
        currencies.forEach(addCurrencyToUI);

        getCompanyList(null, 'mostBoughtFrom', (companies) => {
            companies.forEach(addCompanyToUI);

            getProductList(null, (products) => {
                products.forEach(addProductToUI);

                getTradeList(new TradeFilter(), (trades) => {
                    trades.forEach(addTradeToUI);
                });
            });
        });
    });

    $('.select2-cur').select2({
        maximumInputLength: 3,
        theme: "bootstrap4",
        width: "auto",
        dropdownCss: {"font-size": "0.8rem"}
    });

    $('.select2-comp, .select2-prod').select2({
        theme: "bootstrap4"
    });

    $('.select2-filter').select2({
        theme: "bootstrap4",
        multiple: true,
    });

    $("span[aria-labelledby='select2-notionalCurrencyInput-container']").css("background-color", "#e9ecef");
    $("span[aria-labelledby='select2-underlyingCurrencyInput-container']").css("background-color", "#e9ecef");
}

$(document).ready(init);

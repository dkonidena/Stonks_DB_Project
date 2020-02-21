const filters = [
    ["#tradeIdInput", /^[0-9A-Z]{0,16}$/],
    ["#quantityInput", /^\d*$/],
    ["#notionalPriceInput", /^\d*\.?\d*$/],
    ["#underlyingPriceInput", /^\d*\.?\d*$/],
    ["#strikePriceInput", /^\d*\.?\d*$/],
    ["#tradeDateDayInput", /^\d{0,2}$/],
    ["#tradeDateMonthInput", /^\d{0,2}$/],
    ["#tradeDateYearInput", /^\d{0,4}$/],
    ["#maturityDateDayInput", /^\d{0,2}$/],
    ["#maturityDateMonthInput", /^\d{0,2}$/],
    ["#maturityDateYearInput", /^\d{0,4}$/],
    ["#filter-creationDateLowerDayInput", /^\d{0,2}$/],
    ["#filter-creationDateLowerMonthInput", /^\d{0,2}$/],
    ["#filter-creationDateLowerYearInput", /^\d{0,4}$/],
    ["#filter-creationDateUpperDayInput", /^\d{0,2}$/],
    ["#filter-creationDateUpperMonthInput", /^\d{0,2}$/],
    ["#filter-creationDateUpperYearInput", /^\d{0,4}$/],
    ["#filter-modificationDateLowerDayInput", /^\d{0,2}$/],
    ["#filter-modificationDateLowerMonthInput", /^\d{0,2}$/],
    ["#filter-modificationDateLowerYearInput", /^\d{0,4}$/],
    ["#filter-modificationDateUpperDayInput", /^\d{0,2}$/],
    ["#filter-modificationDateUpperMonthInput", /^\d{0,2}$/],
    ["#filter-modificationDateUpperYearInput", /^\d{0,4}$/],
];

function init() {

    elements.tradeListEmptyMessage.hide();
    elements.tradeListEmptyMessage.removeClass("d-none");

    filters.forEach((x) => {
        var t = $(x[0]);
        setInputFilter(t, (v) => { return x[1].test(v) });
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
        var trade = trades[elements.tradeIdInput.val()];
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

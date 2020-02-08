const filters = [
    ["#tradeIdInput", /^\d{0,9}$/],
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
    ["#creationDateUpperDayInput", /^\d{0,2}$/],
    ["#creationDateUpperMonthInput", /^\d{0,2}$/],
    ["#creationDateUpperYearInput", /^\d{0,4}$/],
    ["#modificationDateLowerDayInput", /^\d{0,2}$/],
    ["#modificationDateLowerMonthInput", /^\d{0,2}$/],
    ["#modificationDateLowerYearInput", /^\d{0,4}$/]
];

function init() {

    $("#notionalCurrencyInput").on("change", () => {
        var selected = $("#notionalCurrencyInput option:selected");
        $("#notionalCurrencySymbol").text(selected.data("symbol"));
        $("#notionalValueInput").prop("placeholder", selected.data("placeholder"));
    });

    $("#underlyingCurrencyInput").on("change", () => {
        var selected = $("#underlyingCurrencyInput option:selected");
        $("#underlyingCurrencySymbol").text(selected.data("symbol"));
        $("#strikePriceCurrencyCymbol").text(selected.data("symbol"));
        $("#underlyingValueInput").prop("placeholder", selected.data("placeholder"));
        $("#strikePriceInput").prop("placeholder", selected.data("placeholder"));
    });

    $("#tradeList").on("show.bs.collapse", () => {
        $("#tradeListCollapseSymbol").text("expand_less");
    });

    $("#tradeList").on("hide.bs.collapse", () => {
        $("#tradeListCollapseSymbol").text("expand_more");
    });

    $("#addTradeButton").on("click", addTradeButton_OnPressed);
    $("#saveTradeButton").on("click",saveTradeButton_OnPressed);
    $("#checkTradeButton").on("click",checkTradeButton_OnPressed);
    $("#discardChangesButton").on("click", cancelTradeButton_OnPressed);

    filters.forEach((x) => {
        var t = x[0];
        setInputFilter(t, (v) => { return x[1].test(v) });
    });


    getCurrencyList(new Date(), (currencies) => {
        currencies.forEach(addCurrencyToUI);
    });

    getCompanyList(new Date(), 'mostBoughtFrom', (companies) => {
        companies.forEach(addCompanyToUI);
    });

    getProductList(new Date(), (products) => {
        products.forEach(addProductToUI);
    });

    getTradeList(new TradeFilter(), (trades) => {
        trades.forEach(addTradeToUI);
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

    $("span[aria-labelledby='select2-notionalCurrencyInput-container']").css("background-color", "#e9ecef");
    $("span[aria-labelledby='select2-underlyingCurrencyInput-container']").css("background-color", "#e9ecef");
}

$(document).ready(function() {
    init();
});

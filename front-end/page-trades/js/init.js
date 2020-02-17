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
    $("#doAdvancedSearch").on("click", advancedSearchButton_OnPressed);

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

    $('.select2-filter').select2({
        theme: "bootstrap4",
        multiple: true,
    });

    $("span[aria-labelledby='select2-notionalCurrencyInput-container']").css("background-color", "#e9ecef");
    $("span[aria-labelledby='select2-underlyingCurrencyInput-container']").css("background-color", "#e9ecef");
}

$(document).ready(function() {
    init();
});

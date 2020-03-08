function init() {

    getCompanyList(null, 'mostBoughtFrom', (companies) => {
        getProductList(null, $.noop);
    });
    getCurrencyList(null, $.noop);
    getUserList($.noop);

    $('.date').datepicker({
        format: "dd-mm-yyyy",
        autoclose: true,
        todayHighlight: true,
        maxViewMode: 3,
        templates: {
            leftArrow: '<i class="material-icons align-bottom">keyboard_arrow_left</i>',
            rightArrow: '<i class="material-icons align-bottom">keyboard_arrow_right</i>',
        },
    });

    $('#filter-reportDateInput').datepicker().on("changeDate", (e) => {
        currentDate = $('#filter-reportDateInput').datepicker("getDate");
        currentTradesNum = 0;
        getNextTradeBlock(true);
    });
}

$(document).ready(() => { init(); });

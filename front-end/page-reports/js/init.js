function init() {

    getCompanyList(null, 'mostBoughtFrom', (companies) => {
        getProductList(null, $.noop);
    });
    getCurrencyList(null, $.noop);
    getUserList($.noop);

    $("#doAdvancedSearch").click(() => {
        let date = $('#filter-reportDateInput').datepicker("getDate");
        getReport(date, loadReportToForm, showError, 0);
    });

    $('.date').datepicker({
        format: "dd-mm-yyyy",
        todayHighlight: true,
        maxViewMode: 3,
        templates: {
            leftArrow: '<i class="material-icons align-bottom">keyboard_arrow_left</i>',
            rightArrow: '<i class="material-icons align-bottom">keyboard_arrow_right</i>',
        },
    });

    $('#filter-reportDateInput').datepicker().on("changeDate", (e) => {
        let date = $('#filter-reportDateInput').datepicker("getDate");
        $("#resultsStatus").show();
        getReport(date, (r) => {
            loadReportToForm(r);
            $("#resultsStatus").hide();
        }, showError, 0);
    });

    $('#advancedSearch').on("show.bs.modal", () => {
        $('#filter-reportDateInput').datepicker("setDate", new Date());
    });
}

$(document).ready(() => { init(); });

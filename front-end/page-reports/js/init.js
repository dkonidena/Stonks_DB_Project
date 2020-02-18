const filters = [
    ["#filter-creationDateLowerDayInput", /^\d{0,2}$/],
    ["#filter-creationDateLowerMonthInput", /^\d{0,2}$/],
    ["#filter-creationDateLowerYearInput", /^\d{0,4}$/],
    ["#filter-creationDateUpperDayInput", /^\d{0,2}$/],
    ["#filter-creationDateUpperMonthInput", /^\d{0,2}$/],
    ["#filter-creationDateUpperYearInput", /^\d{0,4}$/],
];

$(document).ready(() => {
    filters.forEach((x) => {
        var t = x[0];
        setInputFilter(t, (v) => { return x[1].test(v) });
    });


    $("#doAdvancedSearch").click(() => {
        let filter = filterObjectFromForm();
        getReportList(filter, (reports) => {
            reports.forEach(addReportToUI);
        });
    });
});

function addReportToUI(report) {
    let s = "<button class=\"btn report-button d-block text-muted py-0 my-n1\"></button>";
    let b = $(s).text(`Report ${report.date.toLocaleDateString()}`).data("report", report);
    b.on("click", () => {
        loadReportToForm(report);
    })
    let li = $("<li class=\"nav-item\"></li>").html(b);
    $("#reports").append(li);
}

function loadReportToForm(report) {
    $("#reportDateDayInput").val(report.date.getDate());
    $("#reportDateMonthInput").val(report.date.getMonth()+1);
    $("#reportDateYearInput").val(report.date.getFullYear());

    renderTable(report.content);
}

function filterObjectFromForm() {
    // TODO whole function needs error handling
    let filter = new Filter();

    if ($("#filter-creationDateLowerDayInput").val() !== "") {
        filter.dateCreated = [new Date(), new Date()];
        filter.dateCreated[0].setHours(0,0,0,0);
        filter.dateCreated[0].setDate($("#filter-creationDateLowerDayInput").val());
        filter.dateCreated[0].setMonth($("#filter-creationDateLowerMonthInput").val()-1);
        filter.dateCreated[0].setFullYear($("#filter-creationDateLowerYearInput").val());
        filter.dateCreated[1].setHours(0,0,0,0);
        filter.dateCreated[1].setDate($("#filter-creationDateUpperDayInput").val());
        filter.dateCreated[1].setMonth($("#filter-creationDateUpperMonthInput").val()-1);
        filter.dateCreated[1].setFullYear($("#filter-creationDateUpperYearInput").val());
        filter.dateCreated[0] = filter.dateCreated[0].toISOString();
        filter.dateCreated[1] = filter.dateCreated[1].toISOString();
    }

    return filter;
}

function renderTable(csv) {
    let blob = new Blob([csv], { type: "text/plain" });

    CsvToHtmlTable.init({
        csv_path: URL.createObjectURL(blob),
        element: "table-container",
        allow_download: true,
        csv_options: {separator: ",", delimiter: "\""},
        datatables_options: {"paging": true}
    });
}

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

    renderTable(report.content, `report-${report.date.toLocaleDateString()}.csv`);
}

function filterObjectFromForm() {
    // TODO whole function needs error handling
    let filter = new Filter();

    if ($("#filter-creationDateLowerYearInput").val() !== "") {
        if (!filter.dateCreated) { filter.dateCreated = {}; }
        filter.dateCreated['after'] = new Date();
        filter.dateCreated.after.setHours(0,0,0,0);
        filter.dateCreated.after.setDate($("#filter-creationDateLowerDayInput").val());
        filter.dateCreated.after.setMonth($("#filter-creationDateLowerMonthInput").val()-1);
        filter.dateCreated.after.setFullYear($("#filter-creationDateLowerYearInput").val());
        filter.dateCreated.after = filter.dateCreated.after.toISOString();
    }

    if ($("#filter-creationDateUpperYearInput").val() !== "") {
        if (!filter.dateCreated) { filter.dateCreated = {}; }
        filter.dateCreated['before'] = new Date();
        filter.dateCreated.before.setHours(0,0,0,0);
        filter.dateCreated.before.setDate($("#filter-creationDateUpperDayInput").val());
        filter.dateCreated.before.setMonth($("#filter-creationDateUpperMonthInput").val()-1);
        filter.dateCreated.before.setFullYear($("#filter-creationDateUpperYearInput").val());
        filter.dateCreated.before = filter.dateCreated.before.toISOString();
    }

    return filter;
}

function renderTable(csv, name) {
    status.innerText = "loading report...";
    let blob = new Blob([csv], { type: "text/plain" });

    CsvToHtmlTable.init({
        csv_path: URL.createObjectURL(blob),
        element: "table-container",
        allow_download: true,
        csv_options: {separator: ",", delimiter: "\""},
        datatables_options: {"paging": true},
        onComplete: () => { status.innerText = ""; },
        downloadName: name
    });
}

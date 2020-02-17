CsvToHtmlTable.init({
    csv_path: `${API_ENDPOINT}/reports?date=${(new Date()).toISOString()}`,
    element: 'table-container',
    allow_download: true,
    csv_options: {separator: ',', delimiter: '"'},
    datatables_options: {"paging": true}
});

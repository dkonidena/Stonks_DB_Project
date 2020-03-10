var CsvToHtmlTable = CsvToHtmlTable || {};

CsvToHtmlTable = {
    init: function (options) {
        options = options || {};
        var csv_path = options.csv_path || "";
        var pdf_download = options.pdf_download || null;
        var csv_download = options.csv_download || null;
        var el = options.element || "table-container";
        var allow_download = options.allow_download || false;
        var generate_pdf = options.generate_pdf || null;
        var csv_options = options.csv_options || {};
        var datatables_options = options.datatables_options || {};
        var custom_formatting = options.custom_formatting || [];
        var onComplete = options.onComplete;
        var downloadName = options.downloadName;
        var customTemplates = {};
        $.each(custom_formatting, function (i, v) {
            var colIdx = v[0];
            var func = v[1];
            customTemplates[colIdx] = func;
        });

        var $table = $("<table class='table table-striped table-condensed' id='" + el + "-table'></table>");
        var $containerElement = $("#" + el);
        $containerElement.empty().append($table);

        $.when($.get(csv_path)).then(
            function (data) {
                var csvData = $.csv.toArrays(data, csv_options);
                var $tableHead = $("<thead></thead>");
                var csvHeaderRow = csvData[0];
                var $tableHeadRow = $("<tr></tr>");
                for (var headerIdx = 0; headerIdx < csvHeaderRow.length; headerIdx++) {
                    $tableHeadRow.append($("<th></th>").text(csvHeaderRow[headerIdx]));
                }
                $tableHead.append($tableHeadRow);

                $table.append($tableHead);
                var $tableBody = $("<tbody></tbody>");

                for (var rowIdx = 1; rowIdx < csvData.length; rowIdx++) {
                    var $tableBodyRow = $("<tr></tr>");
                    for (var colIdx = 0; colIdx < csvData[rowIdx].length; colIdx++) {
                        var $tableBodyRowTd = $("<td></td>");
                        var cellTemplateFunc = customTemplates[colIdx];
                        if (cellTemplateFunc) {
                            $tableBodyRowTd.html(cellTemplateFunc(csvData[rowIdx][colIdx]));
                        } else {
                            $tableBodyRowTd.text(csvData[rowIdx][colIdx]);
                        }
                        $tableBodyRow.append($tableBodyRowTd);
                        $tableBody.append($tableBodyRow);
                    }
                }
                $table.append($tableBody);

                table = $table.DataTable(datatables_options);

                if (allow_download) {
                    let buttonTemplate = "class='btn btn-info text-light mx-3 my-2'";
                    let icon1 = "<i class='align-bottom material-icons'>dynamic_feed</i>";
                    let icon2 = "<i class='align-bottom material-icons'>get_app</i>";

                    if(isFunction(csv_download)) {
                        let b = $(`<button ${buttonTemplate}>${icon1}Generate CSV</button>`);
                        b.on("click", () => {
                            if (b.prop("href") !== undefined) return;
                            b.html(`${icon1}Generating...`);
                            b.prop("disabled", true);
                            f = function(path) {
                                let a = $(`<a ${buttonTemplate}>${icon2}Download as CSV</a>`).prop({"disabled": false, "href": path, "download": `${downloadName}.csv`});
                                b.replaceWith(a);
                            }
                            csv_download(f);
                        });
                        $containerElement.append(b);
                    }

                    if(isFunction(pdf_download)) {
                        let b = $(`<button ${buttonTemplate}>${icon1}Generate PDF</button>`);
                        b.on("click", () => {
                            if (b.prop("href") !== undefined) return;
                            b.html(`${icon1}Generating...`).prop("disabled", true);
                            f = function(path) {
                                let a = $(`<a ${buttonTemplate}>${icon2}Download as PDF</a>`).prop({"disabled": false, "href": path, "download": `${downloadName}.pdf`});
                                b.replaceWith(a);
                            }
                            pdf_download(f);
                        });
                        $containerElement.append(b);
                    }

                }

                onComplete();
            });
    },
    add_existing: (element, data, csv_options) => {
        var csvData = $.csv.toArrays(data, csv_options);

        for (const row of csvData) {
            table.row.add(row);
        }

        table.draw("full-hold");
    }
};

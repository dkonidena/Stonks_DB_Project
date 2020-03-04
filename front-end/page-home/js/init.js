$(document).ready(() => {
    $("#trades").click(() => window.location = "../page-trades/page-trades.html");
    $("#companies").click(() => window.location = "../page-companies/page-companies.html");
    $("#products").click(() => window.location = "../page-products/page-products.html");
    $("#reports").click(() => window.location = "../page-reports/page-reports.html");

    getUserList();
});

function slide() {
    $("#slide1").animate({
        left: '-50%'
    }, 500, function () {
        $("#slide1").css('left', '150%');
    });

    $("#slide1").next().animate({
        left: '50%'
    }, 500);
}

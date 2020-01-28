class Product {
    constructor() {
        this.id = 0;
        this.name = "";
        this.companyId = 0;
        this.value = 0;
        this.creatioDate = new Date();
        this.userIdCreatedBy = 0;
    }
};

var products = [];

function * productGenerator() {
    while (true) {
        let p = new Product();
        p.id = randInt(0, 999);
        p.name = "Product " + p.id;
        p.companyId = randInt(0, 999999);
        p.value = (randInt(0,9999) + Math.random()).toFixed(2);
        p.creatioDate = randDate();
        p.userIdCreatedBy = randInt(0, 999999);
        yield p;
    }
}

function addProduct(p) {
    let o = "<option></option>";
    let c = $(o).text(p.name);
    $("#productInput").append(c);
}

function getProductList() {
    if (products.length == 0) {
        for (let i = 0; i < 10; i++) {
            products.push(productGenerator().next().value);
        }
    }
    return products;
}

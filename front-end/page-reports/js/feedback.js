const NAMES = {
    buyingParty: "Buyer",
    maturityDate: "Maturity Date",
    notionalCurrency: "Notional Currency",
    notionalPrice: "Notional Price",
    product: "Product",
    quantity: "Quantity",
    sellingParty: "Selling Party",
    strikePrice: "Strike Price",
    underlyingCurrency: "Underlying Currency",
    underlyingPrice: "Underlying Price"
}

function getRow(field, old, new) {
    return `
    <tr>
      <td>${NAMES[field]}</td>
      <td>${old} -> ${new}</td>
      <td>
          <button id="${field}-accept" type="button" class="btn btn-sm btn-outline-dark">
            <i style="font-size:26px;" class="material-icons text-success mr-1">done</i>
          </button>
      </td>
      <td>
          <button id="${field}-ignore" type="button" class="btn btn-sm btn-outline-dark">
            <i style="font-size:26px;" class="material-icons text-fail mr-1">close</i>
          </button>
      </td>
    </tr>`
}

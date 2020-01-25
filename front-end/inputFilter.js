function setInputFilter(textbox, inputFilter) {
	["input", "keydown", "keyup", "mousedown", "mouseup", "select", "contextmenu", "drop"].forEach(function (event) {
		textbox.addEventListener(event, function () {
			if (inputFilter(this.value)) {
				this.oldValue = this.value;
				this.oldSelectionStart = this.selectionStart;
				this.oldSelectionEnd = this.selectionEnd;
			} else if (this.hasOwnProperty("oldValue")) {
				this.value = this.oldValue;
				this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
			} else {
				this.value = "";
			}
		});
	});
}

setInputFilter(document.getElementById("quantityInput"), (value) => {
	return /^\d*\.?\d*$/.test(value);
});

setInputFilter(document.getElementById("strikePriceInput"), (value) => {
	return /^\d*\.?\d*$/.test(value);
});

setInputFilter(document.getElementById("tradeIdInput"), (value) => {
	return /^\d*$/.test(value);
});

setInputFilter(document.getElementById("notionalPriceInput"), (value) => {
	return /^\d*\.?\d*$/.test(value);
});

setInputFilter(document.getElementById("underlyingPriceInput"), (value) => {
	return /^\d*\.?\d*$/.test(value);
});

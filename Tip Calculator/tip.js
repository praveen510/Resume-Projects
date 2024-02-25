function CalculateTip() {
    var totalAmount = document.getElementById("billAmount").value;
    var qualityOfService = document.getElementById("qualityofservice").value;
    var numOfPeople = document.getElementById("numPeople").value;

    if (totalAmount === '') {
        alert("Please enter the total bill amount");
    } else if (numOfPeople === '') {
        alert("Please put the number of people");
    } else {
        var tipPerPerson = Math.round((totalAmount * qualityOfService) / numOfPeople);
        document.getElementById("resultAmount").innerHTML = "Tip amount: <br>$ " + tipPerPerson + "<br>Per Person";
    }
}

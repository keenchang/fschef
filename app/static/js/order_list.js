let tableStates = document.querySelectorAll("td:nth-child(2)");
let orderLinks = document.querySelectorAll("td:nth-child(3) #link");
let orderClears = document.querySelectorAll("td:nth-child(3) #clear");

tableStates.forEach(function (e, i) {
  if (e.textContent == "未點餐") {
    orderLinks[i].setAttribute("class", "btn btn-info disabled");
  } else if (e.textContent == "已付款") {
    orderClears[i].setAttribute("class", "btn btn-danger");
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const socket = io.connect(location.protocol + "//" + document.domain + ":" + location.port);

  socket.on("sendOrderStatus", (message) => {
    console.log(message);

    let tableId = message["tableId"];
    let tableStatus = message["tableStatus"];
    let tableItem = document.querySelector(`tr[data-table-id="${tableId}"]`);
    let tableState = tableItem.querySelector("td:nth-child(2)");
    let orderLink = tableItem.querySelector("td:nth-child(3) #link");
    let orderClear = tableItem.querySelector("td:nth-child(3) #clear");

    tableState.textContent = tableStatus;
    if (message["tableStatus"] == "已點餐") {
      orderLink.setAttribute("class", "btn btn-info");
    } else if (message["tableStatus"] == "已付款") {
      orderClear.setAttribute("class", "btn btn-danger");
    }
  });
});

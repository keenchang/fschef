function fetchWithParams(path, method, params) {
  const body = JSON.stringify(params);

  return fetch(path, {
    method: method,
    headers: {
      "Content-Type": "application/json",
    },
    body: body,
  })
    .then((response) => response.json())
    .catch((err) => {
      console.log(err);
    });
}

let orderForm = document.querySelector("table");
let tableId = orderForm.dataset.tableId;
let tableStatus = orderForm.dataset.tableStatus;
let comment = document.querySelector("#comment");
let acceptBtn = document.querySelector("#accept");
let cancelBtn = document.querySelector("#cancel");

if (tableStatus == "已點餐") {
  comment.disabled = false;
  acceptBtn.disabled = false;
  cancelBtn.disabled = false;
}

document.addEventListener("DOMContentLoaded", () => {
  const socket = io.connect(location.protocol + "//" + document.domain + ":" + location.port);

  acceptBtn.addEventListener("click", () => {
    let path = "/api/order/create";
    let message = { tableId: tableId };

    fetchWithParams(path, "POST", message).then((data) => {
      if (data["tableStatus"] == "已接受") {
        message["tableStatus"] = data["tableStatus"];
        message["orderId"] = data["orderId"];

        socket.emit("accept_order", message);

        window.location.href = data["url"];
      } else {
        window.alert("資料庫新增訂單失敗");
      }
    });
  });

  cancelBtn.addEventListener("click", () => {
    let path = "/api/order/cancel";
    let message = { tableId: tableId, msg: comment.value };

    fetchWithParams(path, "POST", message).then((data) => {
      if (data["tableStatus"] == "已取消") {
        message["tableStatus"] = data["tableStatus"];

        socket.emit("accept_order", message);

        window.location.href = data["url"];
      } else {
        window.alert("資料庫新增訂單失敗");
      }
    });
  });
});

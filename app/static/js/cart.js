function caclTotalPrice() {
  const tableList = document.querySelectorAll("tbody tr");
  let totalPriceElem = document.querySelector(".total-price");
  let totalPrice = 0;

  tableList.forEach((userItem) => {
    let sumNum = userItem.querySelector("td:nth-child(5)");
    let price = Number(userItem.querySelector("td:nth-child(4)").textContent.replace("$", ""));
    let num = Number(userItem.querySelector(".quantity").value);
    const tempNum = Math.round((price * num + Number.EPSILON) * 100) / 100;
    sumNum.textContent = "$" + tempNum;
    totalPrice += tempNum;
  });

  totalPriceElem.textContent = "$" + Math.round((totalPrice + Number.EPSILON) * 100) / 100;
}

function updateTable(_message, DB) {
  let totalPrice = 0;
  let _name = _message["name"];
  let price = _message["price"];

  if (DB[_name].count === 0) {
    DB[_name].count++;

    const el = `<tr data-menu-id=${DB[_name].id}>
                  <td><img class="card-img-top" src="/static/${DB[_name].imgPath}" alt="Card image cap" style="width:50px;"></td>
                  <td data-name=${_name}>${_name}</td>
                  <td><input type="number" class="quantity" value=${DB[_name].count}></td>
                  <td>${DB[_name].price}</td>
                  <td>${totalPrice}</td>
                  <td>
                    <button class="remove-item-btn btn btn-danger btn-sm">
                      <i class="fas fa-trash-alt"></i>
                    </button>
                  </td>
                </tr>`;
    cartList.insertAdjacentHTML("beforeend", el);
  } else {
    DB[_name].count++;

    const tableList = document.querySelectorAll("tbody tr");
    tableList.forEach((userItem) => {
      let checkName = userItem.querySelector("td:nth-child(2)").textContent;
      if (checkName === _name) {
        userItem.querySelector(".quantity").value = DB[_name].count;
      }
    });
  }

  caclTotalPrice();
}

// 取得需要的DOM
let cardList = document.querySelector("#card-list");
let cartList = document.querySelector("tbody");
let delAllBtn = document.querySelector(".empty-cart");
let checkoutBtn = document.querySelector("#checkout");
let orderStatus = document.querySelector("#status");
let linePayBtn = document.querySelector("#linepay");
let newebPayBtn = document.querySelector("#newebpay");
let storeId = document.querySelector("#checkout").dataset.storeId;
let tableId = document.querySelector("#checkout").dataset.tableId;

// 取得頁面上的菜單資料
let fromDataBase = {};
document.addEventListener("addMenus", ({ detail }) => {
  let menus = [].concat(...detail.menus);

  menus.forEach((menu) => {
    let menuId = menu.id;
    let menuName = menu.name;
    let menuImgPath = menu.img_path;
    let menuPrice = "$" + menu.price;

    fromDataBase[menuName] = { id: menuId, price: menuPrice, imgPath: menuImgPath, count: 0 };
  });
});

// Action Cable
document.addEventListener("DOMContentLoaded", () => {
  const socket = io.connect(location.protocol + "//" + document.domain + ":" + location.port);

  socket.on(`changeCart${tableId}`, (message) => {
    if (message["state"] == "add") {
      updateTable(message, fromDataBase);
    } else if (message["state"] == "delete") {
      let name = message["name"];

      let cartItem = cartList.querySelector(`td[data-name=${name}]`).parentElement;
      cartItem.remove();

      fromDataBase[name].count = 0;

      const tableList = document.querySelectorAll("tbody tr");
      if (tableList.length === 0) {
        let totalPriceElem = document.querySelector(".total-price");
        totalPriceElem.textContent = "$" + "0";
      }

      caclTotalPrice();
    } else {
      const table = cartList.querySelectorAll("tr");
      table.forEach((userItem) => {
        const name_ = userItem.querySelector("td:nth-child(2)").textContent;
        fromDataBase[name_].count = 0;
        userItem.remove();
      });

      let totalPriceElem = document.querySelector(".total-price");
      totalPriceElem.textContent = "$" + "0";
    }
  });

  cardList.addEventListener("click", (e) => {
    const targetElem = e.target;

    if (targetElem.nodeName === "BUTTON") {
      var name_ = targetElem.parentElement.querySelector(".card-title").textContent;

      let message = { tableId: tableId, name: name_, state: "add" };
      socket.emit("cart", message);
    } else if (targetElem.nodeName === "I") {
      var name_ = targetElem.parentElement.parentElement.querySelector(".card-title").textContent;

      let message = { tableId: tableId, name: name_, state: "add" };
      socket.emit("cart", message);
    }
  });

  cartList.addEventListener("click", (e) => {
    const targetElem = e.target;

    if (targetElem.nodeName === "BUTTON") {
      const getElem = targetElem.parentElement.parentElement;
      var name_ = getElem.querySelector("td:nth-child(2)").textContent;
    } else if (targetElem.nodeName === "I") {
      const getElem = targetElem.parentElement.parentElement.parentElement;
      var name_ = getElem.querySelector("td:nth-child(2)").textContent;
    }

    let message = { tableId: tableId, name: name_, state: "delete" };
    socket.emit("cart", message);
  });

  delAllBtn.addEventListener("click", (e) => {
    let message = { tableId: tableId, state: "delete_all" };
    socket.emit("cart", message);
  });

  socket.on(`acceptOrderStatus${tableId}`, (message) => {
    if (message["tableStatus"] == "已接受") {
      orderStatus.textContent = "已接受";
      linePayBtn.href = `/order/${message["orderId"]}/pay`;
      newebPayBtn.href = `/order/${message["orderId"]}/blue_pay`;
    } else {
      if (message["msg"] == "") {
        orderStatus.textContent = "已退回";
      } else {
        orderStatus.textContent = "已退回->" + message["msg"];
      }
    }
  });

  checkoutBtn.addEventListener("click", () => {
    let message = { storeId: storeId, tableId: tableId };

    let cartItems = cartList.querySelectorAll("tr");
    if (cartItems.length > 0) {
      cartItems.forEach((cartItem) => {
        let menuId = cartItem.dataset.menuId;
        let menuName = cartItem.querySelector("td:nth-child(2)").textContent;
        let price = Number(cartItem.querySelector("td:nth-child(4)").textContent.replace("$", ""));
        let count = cartItem.querySelector(".quantity").value;

        message[menuId] = { name: menuName, price: price, imgPath: fromDataBase[menuName].imgPath, count: count };
      });

      orderStatus.textContent = "已送出";

      socket.emit("send_order", message);
    } else {
      orderStatus.textContent = "請新增餐點";
    }
  });
});

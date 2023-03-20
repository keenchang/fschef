import { fetchWithParams } from "./lib/fetcher.js";
import { addPagination } from "./lib/pagination.js";

function fetchMenus(userId, storeId, menuTypeId) {
  const data = {
    user_id: userId,
    store_id: storeId,
    menu_type_id: menuTypeId,
  };

  return fetchWithParams(path, "POST", data).then((data) => {
    window.menus = data["menus"];

    add_menu(cardList, window.menus, 0);
    addPagination(pageList, window.menus);

    var event = new CustomEvent("addMenus", {
      detail: {
        menus: data["menus"],
      },
    });
    document.dispatchEvent(event);
  });
}

function add_menu(parents, menuList, index) {
  parents.replaceChildren();

  let options = "";
  menuList[index].forEach((element) => {
    options += `<div class="col-12 col-md-4">
                  <div class="card" data-menu-id=${element["id"]}>
                    <img class="card-img-top" src="/static/${element["img_path"]}" alt="Card image cap">
                    <div class="card-body">
                      <h3 class="card-title">${element["name"]}</h3>
                      <p class="text price">${element["price"]}</p>
                      <button class="btn btn-sm btn-warning fw-light">
                        <i class="fas fa-cart-shopping"></i>
                      </button>
                    </div>
                  </div>
                </div>`;
  });
  parents.insertAdjacentHTML("beforeend", options);
}

let menuTypeList = document.querySelector("#menu-type-list");
let cardList = document.querySelector("#card-list");
let pageList = document.querySelector("#page-list");

let userId = menuTypeList.dataset.userId;
let storeId = menuTypeList.dataset.storeId;
let path = "/api/filter";

fetchMenus(userId, storeId, "0");

menuTypeList.addEventListener("click", (e) => {
  let menuTypeId = e.target.dataset.menuTypeId;

  fetchMenus(userId, storeId, menuTypeId);
});

pageList.addEventListener("click", (e) => {
  if (e.target.nodeName == "LI") {
    let pageIndex = e.target.textContent - 1;

    add_menu(cardList, window.menus, pageIndex);
  }
});

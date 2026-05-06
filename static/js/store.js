function loadCart() {
  try {
    return JSON.parse(sessionStorage.getItem("mediconnect_cart") || "{}");
  } catch {
    return {};
  }
}

function saveCart(cart) {
  sessionStorage.setItem("mediconnect_cart", JSON.stringify(cart));
}

function addToCart(item) {
  const cart = loadCart();
  const id = String(item.id);
  cart[id] = cart[id] || { 
    id, 
    name: item.name, 
    price: Number(item.price), 
    image: item.image || "",
    qty: 0 
  };
  cart[id].qty += 1;
  saveCart(cart);
}

function removeOne(id) {
  const cart = loadCart();
  if (!cart[id]) return;
  cart[id].qty -= 1;
  if (cart[id].qty <= 0) delete cart[id];
  saveCart(cart);
}

function addOne(id) {
  const cart = loadCart();
  if (!cart[id]) return;
  cart[id].qty += 1;
  saveCart(cart);
}

function clearCart() {
  saveCart({});
}

function renderCart() {
  const wrap = document.getElementById("cartWrap");
  if (!wrap) return;

  const cart = loadCart();
  const items = Object.values(cart);
  if (items.length === 0) {
    wrap.innerHTML = `<p class="muted">Cart is empty.</p>`;
    return;
  }

  let total = 0;
  const rows = items
    .map((it) => {
      const line = it.price * it.qty;
      total += line;
      const imageHtml = it.image 
        ? `<img src="${it.image}" alt="${it.name}" style="width:50px; height:50px; object-fit:cover; border:2px solid var(--dark);" onerror="this.style.display='none'; this.parentElement.innerHTML='<div style=\\'width:50px; height:50px; border:2px solid var(--dark); display:flex; align-items:center; justify-content:center; font-size:10px;\\'>No Img</div>';">`
        : `<div style="width:50px; height:50px; border:2px solid var(--dark); display:flex; align-items:center; justify-content:center; font-family:var(--mono); font-size:10px; text-transform:uppercase;">No Img</div>`;
      
      return `
        <tr>
          <td>
            <div style="display:flex; align-items:center; gap:12px;">
              ${imageHtml}
              <span style="font-weight:700;">${it.name}</span>
            </div>
          </td>
          <td>₹${it.price.toFixed(2)}</td>
          <td>
            <div class="qty">
              <button data-qty-dec="${it.id}">−</button>
              <span class="kbd">${it.qty}</span>
              <button data-qty-inc="${it.id}">+</button>
            </div>
          </td>
          <td style="font-weight:800;">₹${line.toFixed(2)}</td>
        </tr>
      `;
    })
    .join("");

  wrap.innerHTML = `
    <table class="cart-table">
      <thead>
        <tr>
          <th>Item</th>
          <th>Price</th>
          <th>Qty</th>
          <th>Line total</th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>
    <div style="display:flex; justify-content:flex-end; margin-top:12px;">
      <div class="total">Total: ₹${total.toFixed(2)}</div>
    </div>
  `;

  wrap.querySelectorAll("[data-qty-dec]").forEach((btn) => {
    btn.addEventListener("click", () => {
      removeOne(btn.getAttribute("data-qty-dec"));
      renderCart();
    });
  });
  wrap.querySelectorAll("[data-qty-inc]").forEach((btn) => {
    btn.addEventListener("click", () => {
      addOne(btn.getAttribute("data-qty-inc"));
      renderCart();
    });
  });
}

// Store page buttons
document.querySelectorAll("[data-add-to-cart]").forEach((btn) => {
  btn.addEventListener("click", () => {
    addToCart({
      id: btn.dataset.id,
      name: btn.dataset.name,
      price: btn.dataset.price,
      image: btn.dataset.image || "",
    });
    btn.textContent = "Added";
    setTimeout(() => (btn.textContent = "Add"), 900);
  });
});

// Cart page actions
const btnClear = document.getElementById("btnClearCart");
if (btnClear) {
  btnClear.addEventListener("click", () => {
    clearCart();
    renderCart();
  });
}

const btnCheckout = document.getElementById("btnCheckout");
if (btnCheckout) {
  btnCheckout.addEventListener("click", () => {
    const msg = document.getElementById("checkoutMsg");
    if (msg) msg.textContent = "Checkout complete. Please contact the pharmacy for payment/delivery.";
  });
}

renderCart();

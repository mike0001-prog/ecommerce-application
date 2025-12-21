// const Cart = document.querySelector("#cart")
// Cart.addEventListener("click",function () {
//      let sideBar = document.querySelector(".side")
//      sideBar.style.width = 20+"%"
// })
// const m = document.querySelector(".main")
// const arr = ["product","product","product","product","product","product","product","product","product","product","product","product"]
// arr.forEach(element => {
//      const ell =document.createElement("div")
//      ell.innerHTML = element
//      m.appendChild(ell)
//      console.log(element)
// });



document.querySelectorAll(".qty").forEach((selector)=>{
     let qtyInputVal = selector.querySelector(".qty input")
     let increaseVal = selector.querySelector(".increment")
     let decreaseVal = selector.querySelector(".decrement")
     let val = parseInt(qtyInputVal.value)
     increaseVal.addEventListener("click",(e)=>{
     if(val < 10){
          val+=1
         qtyInputVal.value = val
     }
     })
     decreaseVal.addEventListener("click",()=>{
     if(val > 1){
          val-=1
          qtyInputVal.value = val
     }
})

})

$(function () {
    const ProductContainer = $(".product-grid")
console.log(ProductContainer)
ProductContainer.on("submit","form",function (e) {
     e.preventDefault()
     console.log($(this).serialize())
     $.ajax({url:$(this).attr("url"),
          type:$(this).attr("action"),
          data: $(this).serialize(),
          success: function (response) {
               console.log("success")
               console.log(response)
          }
     })
}) 
})

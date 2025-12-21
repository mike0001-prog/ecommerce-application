// let link  = document.querySelector("#link")
// link.addEventListener("click",function(e) {
//     e.preventDefault()
//     let url = this.href
//     console.log(url)
//     getData(url)
// })
// // async function getData(URL) {
// //     const data  = await fetch(url)
// //     if data.re
// // }
// function getData(URL) {
//     const xhr  = new XMLHttpRequest()
// xhr.open('GET',URL)
// xhr.onload = function() {
//     if(this.readyState == 4 && this.status == 200){
//         const result  = this.responseText
//         let body  = document.querySelector('body')
//         let main  = document.querySelector('main')
//         main.innerHTML = result
//     }
// }
// xhr.send()
// }
console.log("hello world")
const inputBox = document.getElementById("div_id_password")
const  input = document.getElementById("id_password")

inputBox.innerHTML+=`<input type="checkbox" id="show_pwd"> <label for="show_pwd">Show password<\label>`
const showEl =  document.getElementById("show_pwd")
showEl.addEventListener("check", ()=>{
    
    if (input.type == "password"){
        input.type = "text"
    }else{
        input.type ="password"
    }
},false)


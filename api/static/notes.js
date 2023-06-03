var buttonUp = () => {
    const input = document.querySelector(".searchbox-input");
    const cards = document.getElementsByClassName("cardFrame");
    let filter = input.value.toLowerCase();
    var result = true;
    for (let i = 0; i < cards.length; i++) {
        let title = cards[i].querySelector(".card-body");
        if (title.innerText.toLowerCase().indexOf(filter) > -1) {
            cards[i].classList.remove("d-none")
        } else {
            cards[i].classList.add("d-none")
        }
    }
    var grid = document.querySelector('.grid')
    var msnry = Masonry.data( grid )
    msnry.layout()

    for(let i = 0; i < cards.length; i++){
        if(cards[i].classList.contains("d-none")){
            result = false;
        }else{
            result = true;
            break;
        }
    }
    if (!result) {
        document.querySelector(".no-result").classList.remove("d-none")
    } else {
        document.querySelector(".no-result").classList.add("d-none")
    }
}

document.getElementById('searchInput').addEventListener('input', (e) => {
    const cards = document.getElementsByClassName("cardFrame");
    if (e.currentTarget.value.length == 0 && e.currentTarget.value == "") {
        for(let i = 0; i < cards.length; i++){
            cards[i].classList.remove("d-none")
        }
        var grid = document.querySelector('.grid')
        var msnry = Masonry.data( grid )
        msnry.layout()
        document.querySelector(".no-result").classList.add("d-none")
    }
  })

function deleteDeck(deckId) {
  fetch("/delete-deck", {             //this will execute delete_deck() in views.py
    method: "POST",
    body: JSON.stringify({ deckId: deckId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function deleteFlash(flashId) {
  fetch("/delete-flash", {             //this will execute delete_note() in views.py
    method: "POST",
    body: JSON.stringify({ flashId: flashId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function fetchFlash(flashId){
  fetch("/fetch-flash", {
    method: "POST",
    body: JSON.stringify({flashId: flashId}),
  }).then((_res) => {
    console.log(flashId);
    window.location.href = "/";
  });
}

// USed to toggle show/hide the list of flashcards belonging to referenced deck. 
function fetchDeck(deckTitle){
  
  var flash_list = document.getElementById(deckTitle);
  if(flash_list.style.display === "none"){
    flash_list.style.display = "block"
  } else{
    flash_list.style.display = "none"
  }
 

}

/*
I noticed your function doesn't work well for mobile. 
*/
// //this "flips" the flash card by hiding one side and showing the other
// function flipFlash() {
//   var aside = document.getElementById("inner");
//   var bside = document.getElementById("bside");
//   if (aside.style.display == "none") {
//     aside.style.display = "block";
//     bside.style.display = "none";
//   } else {
//     aside.style.display = "none";
//     bside.style.display = "block";
//   }
//   aside.style.transform = "rotateY(180deg)";
//   bside.style.transform = "rotateY(180deg)";
// }

// cheap way to link to bookstack on port 8080 when I have it running, though there is much better eways to do this. 
function bookstack(){
  window.location.href = "http://localhost:8080";

}
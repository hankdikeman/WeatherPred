// // Parse date in YYYY-MM-DD format as local date
// function parseISOLocal(s) {
//   let [y, m, d] = s.split('-');
//   return new Date(y, m - 1, d);
// }
//
// // Format date as YYYY-MM-DD
// function dateToISOLocal(date) {
//   let z = n => ('0' + n).slice(-2);
//   return date.getFullYear() + '-' + z(date.getMonth() + 1) + '-' + z(date.getDate());
// }
//
// // Convert range slider value to date string
// function range2date(evt) {
//   let dateInput = document.querySelector('#d0');
//   let minDate = parseISOLocal(dateInput.defaultValue);
//   minDate.setDate(minDate.getDate() + Number(this.value));
//   dateInput.value = dateToISOLocal(minDate);
//   var output = document.getElementById("demo");
//   output.innerHTML = dateInput.value;
//   }
//
// // Convert entered date to range
// function date2range(evt) {
//   let date = parseISOLocal(this.value);
//   let numDays = (date - new Date(this.min)) / 8.64e7;
//   document.querySelector('#r0').value = numDays;
// }
//
// window.onload = function() {
//   let rangeInput = document.querySelector('#r0');
//   let dateInput = document.querySelector('#d0');
//   // Get the number of days from the date min and max
//   // Dates in YYYY-MM-DD format are treated as UTC
//   // so will be exact whole days
//   let rangeMax = (new Date(dateInput.max) - new Date(dateInput.min)) / 8.64e7;
//
//
//   // Set the range min and max values
//   rangeInput.min = 0;
//   rangeInput.max = rangeMax;
//   // Add listener to set the date input value based on the slider
//   rangeInput.addEventListener('input', range2date, false);
//   // Add listener to set the range input value based on the date
//   dateInput.addEventListener('change', date2range, false);
//
// }


var slideIndex = 1;
showSlides(slideIndex);


function plusSlides(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
}

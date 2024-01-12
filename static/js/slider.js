const mySlider = document.getElementById("my-slider");
const sliderValue = document.getElementById("slider-value");

function slider(){
    valPercent = (mySlider.value / mySlider.max)*100;
    mySlider.style.background = `linear-gradient(to right, #3264fe ${valPercent}%, #d5d5d5 ${valPercent}%)`;
    sliderValue.textContent = mySlider.value;
}
slider();
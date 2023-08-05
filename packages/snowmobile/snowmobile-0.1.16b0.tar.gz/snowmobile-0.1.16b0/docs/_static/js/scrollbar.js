/* When the user scrolls down, hide the navbar. When the user scrolls up, show the navbar */
var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
  const currentScrollPos = window.pageYOffset;
  const elements = document.getElementsByClassName("md-header");
  const has_elements = elements.length > 0
  const scroll_delta = currentScrollPos - prevScrollpos
  if (prevScrollpos > currentScrollPos) {
    if (has_elements) {
        elements[0].style.top = "0";
      }
  } else {
    if (
        has_elements           /* page has loaded/elements have been found */
        && screen.width < 1100 /* only apply on screen size < 1100 px */
        && scroll_delta >= 20  /* allow for some scrolling down before collapse */
    ) {
        elements[0].style.top = "-2.6rem";
      }
  }
  prevScrollpos = currentScrollPos;
}
